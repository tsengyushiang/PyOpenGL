import sys
import cv2
import datetime
import os

from qtLayout.fourRealsense import *
from PyQt5.QtCore import *

from Aruco.Aruco import ArucoInstance
from Algorithm.vector3D import rotation_matrix_from_vectors

from Realsense.device import *

from opencv.QtcvImage import *

from opengl.Scene.QtGLScene import *
from opengl.Geometry.DepthArrGeometry import *
from opengl.Material.ShaderMaterial import *
from opengl.Mesh import *
from opengl.Uniform import *
from opengl.Texture import *
import opengl.Helper as Glhelper

import FileIO.ply as ply
import FileIO.json as json

import shaders.realsensePointCloud as myShader

from Args.singleModelAndTexture import build_argparser
args = build_argparser().parse_args()


class UIControls():
    def __init__(self, ui, MainWindow):
        self.ui = ui
        self.MainWindow = MainWindow
        self.ui.setupUi(self.MainWindow)

    def getCanvas(self):
        return self.ui.openGLWidget

    def getboundary(self):
        pos = [0, 0, 0]
        neg = [0, 0, 0]
        pos[0] = self.ui.posX.value()/10
        pos[1] = self.ui.posY.value()/10
        pos[2] = self.ui.posZ.value()/10
        neg[0] = self.ui.negX.value()/10
        neg[1] = self.ui.negY.value()/10
        neg[2] = self.ui.negZ.value()/10
        return pos, neg


class DevicesControls():
    def __init__(self, hardware):
        self.device = hardware

        self.imgTexture = []
        self.uniform = None
        self.pointCloudGeo = None

        self.color_image = None
        self.depth_colormap = None
        self.depthValues = None

    def start(self):
        self.device.start()

    def genPointClouds(self):
        h = self.device.h
        w = self.device.w
        intr = self.device.intr

        texColor = Texture(np.full((h, w, 3), 0, dtype="uint8"))
        texDepth = Texture(np.full((h, w, 3), 255, dtype="uint8"))
        self.imgTexture = [texColor, texDepth]

        # add scene
        self.uniform = Uniform()
        self.uniform.addTexture('texColor', texColor)
        self.uniform.addTexture('texDepth', texDepth)
        self.uniform.addFloat('fx', intr.fx)
        self.uniform.addFloat('fy', intr.fy)
        self.uniform.addFloat('ppx', intr.ppx)
        self.uniform.addFloat('ppy', intr.ppy)
        self.uniform.addFloat('w', w)
        self.uniform.addFloat('h', h)
        self.uniform.addvec3('bboxPos', [1, 1, 1])
        self.uniform.addvec3('bboxNeg', [-1, -1, -1])
        self.uniform.addMat4('extrinct', np.array([
            [1.0, 0.0, 0.0, 0.0],
            [0.0, 1.0, 0.0, 0.0],
            [0.0, 0.0, 1.0, 0.0],
            [0.0, 0.0, 0.0, 1.0]
        ]))

        mat = ShaderMaterial(myShader.vertex_shader,
                             myShader.fragment_shader,
                             self.uniform)

        self.pointCloudGeo = DepthArrGeometry(np.ones(w*h))

        return Mesh(mat, self.pointCloudGeo)

    def updateFrames(self):
        color_image, depth_colormap, depthValues = self.device.getFrames()

        self.color_image = color_image
        self.depth_colormap = depth_colormap
        self.depthValues = depthValues

        # update opengl texture
        self.imgTexture[0].update(color_image)
        self.imgTexture[1].update(depth_colormap)

        # print(pointcloud)
        self.pointCloudGeo.update(depthValues)

        return color_image, depth_colormap

    def calibration(self):
        corner1, middle, corner2, middle2, num = ArucoInstance.findMarkers(
            self.color_image)

        def reset():
            self.uniform.setValue('extrinct', np.array([
                [1.0, 0.0, 0.0, 0.0],
                [0.0, 1.0, 0.0, 0.0],
                [0.0, 0.0, 1.0, 0.0],
                [0.0, 0.0, 0.0, 1.0]
            ]))
            # print("calibration error")

        if(num > 0):
            markerPoint1 = self.device.pixel2point(corner1)
            markerPointMiddle = self.device.pixel2point(middle)
            markerPoint2 = self.device.pixel2point(corner2)
            markerPointMiddle2 = self.device.pixel2point(middle2)

            centerPoint = (markerPoint1+markerPointMiddle +
                           markerPoint2+markerPointMiddle2)/4

            edge1 = markerPoint1-markerPointMiddle
            edge2 = markerPoint2-markerPointMiddle

            x = edge1 / np.linalg.norm(edge1)
            z = edge2 / np.linalg.norm(edge2)
            y = np.array([
                x[1]*z[2]-x[2]*z[1],
                x[2]*z[0]-x[0]*z[2],
                x[0]*z[1]-x[1]*z[0],
            ])

            coordMarker = np.array([
                [x[0], -y[0], z[0], centerPoint[0]],
                [x[1], -y[1], z[1], centerPoint[1]],
                [x[2], -y[2], z[2], centerPoint[2]],
                [0, 0, 0, 1.0]
            ])

            try:
                inverCoordMarker = np.linalg.inv(coordMarker)
                self.uniform.setValue('extrinct', inverCoordMarker)
            except:
                reset()
        else:
            reset()

    def updateBoundary(self, pos, neg):
        if(self.uniform):
            self.uniform.setValue('bboxPos', pos)
            self.uniform.setValue('bboxNeg', neg)


class App():
    def __init__(self):
        self.initDevices()
        self.initQtwindow()
        self.pos, self.neg = [1, 1, 1], [-1, -1, -1]

    def initDevices(self):
        # setUp realsense
        connected_devices = GetAllRealsenses()
        self.devicesControls = []

        # Start streaming from cameras
        for device in connected_devices:
            controls = DevicesControls(device)
            self.devicesControls.append(controls)
            controls.start()

    def initQtwindow(self):
        # init Qt window
        app = QtWidgets.QApplication(sys.argv)
        MainWindow = QtWidgets.QMainWindow()
        ui = Ui_MainWindow()
        self.uiControls = UIControls(ui, MainWindow)
        ui.pushButton.clicked.connect(self.save)

        self.scene = QtGLScene(self.uiControls.getCanvas())
        self.scene.customRender.append(self.customPaint)

        self.imgBlocks = [
            [QtcvImage(ui.label00), QtcvImage(ui.label01)],
            [QtcvImage(ui.label10), QtcvImage(ui.label11)],
            [QtcvImage(ui.label20), QtcvImage(ui.label21)],
            [QtcvImage(ui.label30), QtcvImage(ui.label31)]
        ]
        self.calibrationCheckBox = ui.checkBox
        MainWindow.show()

        # window create init opengl
        for device in self.devicesControls:
            self.scene.add(device.genPointClouds())

        timer = QTimer(MainWindow)
        timer.timeout.connect(self.mainloop)
        timer.start(1)

        ui.statusbar.showMessage(
            "Find {0} realsense(s).".format(len(self.devicesControls)))

        app.exec_()

    def monitorScrollBar(self):
        pos, neg = self.uiControls.getboundary()

        for device in self.devicesControls:
            device.updateBoundary(pos, neg)

        return pos, neg

    def customPaint(self):
        Glhelper.drawXYZaxis()
        pos, neg = self.monitorScrollBar()
        Glhelper.drawBbox(pos, neg)
        self.pos, self.neg = pos, neg

    def mainloop(self):
        self.scene.startDraw()
        for device in self.devicesControls:

            color_image, depth_colormap = device.updateFrames()
            if(self.calibrationCheckBox.checkState() != 0):
                device.calibration()

            # update qt image box
            self.imgBlocks[0][0].setImage(color_image)
            self.imgBlocks[0][1].setImage(depth_colormap)

        self.scene.endDraw()

    def save(self):
        currentTime = datetime.datetime.now()
        currentTimeStr = currentTime.strftime("%Y%m%d_%H%M%S_%f")[:-3]
        # print(currentTimeStr)
        path = os.getcwd()
        # print("The current working directory is %s" % path)
        saveRootPath = os.path.join(path, currentTimeStr)
        os.mkdir(saveRootPath)

        for deviceControls in self.devicesControls:
            device = deviceControls.device
            device.saveFrames(saveRootPath)
            serial_num = device.serial_num

            mat4 = deviceControls.uniform.getValue('extrinct')

            clipPoints = []
            for points in device.getPoints().reshape(device.h*device.w, 3):
                vec = np.array([points[0], points[1], points[2], 1.0])
                alignedVec = mat4.dot(vec)

                if(self.pos[0] < alignedVec[0] or
                   self.pos[1] < alignedVec[1] or
                   self.pos[2] < alignedVec[2] or
                   self.neg[0] > alignedVec[0] or
                   self.neg[1] > alignedVec[1] or
                   self.neg[2] > alignedVec[2]):
                    continue

                clipPoints.append(
                    (alignedVec[0], alignedVec[1], alignedVec[2]))

            ply.save(clipPoints, os.path.join(saveRootPath,
                                              serial_num+'.clipPointClouds'+'.ply'))

            config = {
                'intr': {
                    'fx': device.intr.fx,
                    'fy': device.intr.fy,
                    'ppx': device.intr.ppx,
                    'ppy': device.intr.ppy
                },
                'extr': mat4,
            }

            json.write(config, os.path.join(saveRootPath,
                                            serial_num+'.config.json'))


app = App()
