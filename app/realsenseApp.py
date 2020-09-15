import sys
import cv2
import datetime
import os

from qtLayout.RealsenseApp import *
from PyQt5.QtCore import *

from Aruco.Aruco import ArucoInstance

from Network.socket.Server import Server
from Network.data.RealsenseData import RealsenseData

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

from scipy.spatial.transform import Rotation

args = build_argparser().parse_args()


class UIControls():
    def __init__(self, ui, MainWindow):
        self.ui = ui
        self.MainWindow = MainWindow
        self.ui.setupUi(self.MainWindow)

        self.imgBlocks = [
            [QtcvImage(ui.color), QtcvImage(ui.depth)]
        ]

        self.selectDevice = 0
        self.listData = []
        self.camPosData = []
        self.camRotData = []

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

    def setImage(self, maps):

        color = maps[self.selectDevice][0]
        depth = maps[self.selectDevice][1]

        self.imgBlocks[0][0].setImage(color)
        self.imgBlocks[0][1].setImage(depth)

    def getCalibrationMode(self):
        return self.ui.checkBox.checkState() != 0


    def listClicked(self, qModelIndex):
        print(qModelIndex.row())
        self.selectDevice = qModelIndex.row()
        self.setScrollBar()

    def setCamPosData(self,poscamera):
        if(self.camPosData == poscamera):
            return
        self.camPosData = poscamera
    
    def setCamRotData(self,rotcamera):
        if(self.camRotData == rotcamera):
            return
        self.camRotData = rotcamera

    def setList(self, qList):
        if(self.listData == qList):
            return
        self.listData = qList
        # 例項化列表模型，新增資料
        slm = QStringListModel()

        # 設定模型列表檢視，載入資料列表
        slm.setStringList(qList)

        # 設定列表檢視的模型
        self.ui.listView.setModel(slm)
        self.ui.listView.setEditTriggers(
            QtWidgets.QAbstractItemView.NoEditTriggers)

        # 單擊觸發自定義的槽函式
        self.ui.listView.clicked.connect(self.listClicked)

    def setScrollBar(self):
        maximum = self.ui.camPos_X.maximum()
        maxDis = 5

        pos = self.camPosData[self.selectDevice]
        pos[0] = pos[0]*maximum/maxDis
        pos[1] = pos[1]*maximum/maxDis
        pos[2] = pos[2]*maximum/maxDis

        self.ui.camPos_X.setValue(pos[0])
        self.ui.camPos_Y.setValue(pos[1])
        self.ui.camPos_Z.setValue(pos[2])
        
        self.ui.camPosLabel_X.setText(str(pos[0]))
        self.ui.camPosLabel_Y.setText(str(pos[1]))
        self.ui.camPosLabel_Z.setText(str(pos[2]))

        rot = self.camRotData[self.selectDevice]
        self.ui.camRot_X.setValue(rot[0])
        self.ui.camRot_Y.setValue(rot[1])
        self.ui.camRot_Z.setValue(rot[2])

        self.ui.camRotLabel_X.setText(str(rot[0]))
        self.ui.camRotLabel_Y.setText(str(rot[1]))
        self.ui.camRotLabel_Z.setText(str(rot[2]))

    def getUIPos(self):
        maximum = self.ui.camPos_X.maximum()
        maxDis = 5
        pos = [0, 0, 0]
        pos[0] = self.ui.camPos_X.value()/maximum*maxDis
        pos[1] = self.ui.camPos_Y.value()/maximum*maxDis
        pos[2] = self.ui.camPos_Z.value()/maximum*maxDis
        if(pos != self.camPosData[self.selectDevice]):        
            self.ui.camPosLabel_X.setText(str(pos[0]))
            self.ui.camPosLabel_Y.setText(str(pos[1]))
            self.ui.camPosLabel_Z.setText(str(pos[2]))
        return pos

    def getUIRot(self):
        rot = [0, 0, 0]
        rot[0] = self.ui.camRot_X.value()
        rot[1] = self.ui.camRot_Y.value()
        rot[2] = self.ui.camRot_Z.value()
        if(rot != self.camRotData[self.selectDevice]):        
            self.ui.camRotLabel_X.setText(str(rot[0]))
            self.ui.camRotLabel_Y.setText(str(rot[1]))
            self.ui.camRotLabel_Z.setText(str(rot[2]))
        return rot
    
    def log(self, msg):
        self.ui.statusbar.showMessage(msg)


class DevicesControls():
    def __init__(self, hardware):
        self.device = hardware

        self.imgTexture = []
        self.uniform = None
        self.pointCloudGeo = None

        self.color_image = None
        self.depth_colormap = None
        self.depthValues = None
        self.camPos = []
        self.camRot = []

    def getInfo(self):
        return self.device.serial_num

    def start(self):
        self.device.start()

    def genPointClouds(self):
        h = self.device.h
        w = self.device.w
        intr = self.device.intr

        texColor = Texture(np.full((h, w, 3), 0, dtype="uint8"))
        texDepth = Texture(np.full((h, w, 3), 255, dtype="uint8"))
        self.imgTexture = [texColor, texDepth]
        self.camPos = [0,0,0]
        self.camRot = [0,0,0] 

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

    def setData(self, data):
        self.device.setData(data)

    def getCamPos(self):
        return self.camPos

    def getCamRot(self):
        return self.camRot

    def calibration(self, pos,rot):
        #print(pos)

        self.camPos = pos
        self.camRot = rot
        
        rotation = Rotation.from_euler('xyz', rot, degrees=True)

        mat = rotation.as_matrix()
        self.uniform.setValue('extrinct', np.array([
                [mat[0][0], mat[0][1], mat[0][2], pos[0]],
                [mat[1][0], mat[1][1], mat[1][2], pos[1]],
                [mat[2][0], mat[2][1], mat[2][2], pos[2]],
                [0, 0, 0, 1]
            ]))
        # corner1, middle, corner2, middle2, num = ArucoInstance.findMarkers(
        #     self.color_image)

        def reset():
            self.uniform.setValue('extrinct', np.array([
                [1.0, 0.0, 0.0, 0.0],
                [0.0, 1.0, 0.0, 0.0],
                [0.0, 0.0, 1.0, 0.0],
                [0.0, 0.0, 0.0, 1.0]
            ]))
            # print("calibration error")

        # if(num > 0):
        #     markerPoint1 = self.device.pixel2point(corner1)
        #     markerPointMiddle = self.device.pixel2point(middle)
        #     markerPoint2 = self.device.pixel2point(corner2)
        #     markerPointMiddle2 = self.device.pixel2point(middle2)

        #     centerPoint = (markerPoint1+markerPointMiddle +
        #                    markerPoint2+markerPointMiddle2)/4

        #     edge1 = markerPoint1-markerPointMiddle
        #     edge2 = markerPoint2-markerPointMiddle

        #     x = edge1 / np.linalg.norm(edge1)
        #     z = edge2 / np.linalg.norm(edge2)
        #     y = np.array([
        #         x[1]*z[2]-x[2]*z[1],
        #         x[2]*z[0]-x[0]*z[2],
        #         x[0]*z[1]-x[1]*z[0],
        #     ])

        #     coordMarker = np.array([
        #         [x[0], -y[0], z[0], centerPoint[0]],
        #         [x[1], -y[1], z[1], centerPoint[1]],
        #         [x[2], -y[2], z[2], centerPoint[2]],
        #         [0, 0, 0, 1.0]
        #     ])

        #     try:
        #         inverCoordMarker = np.linalg.inv(coordMarker)
        #         self.uniform.setValue('extrinct', inverCoordMarker)
        #     except:
        #         reset()
        # else:
        #     reset()

    def updateBoundary(self, pos, neg):
        if(self.uniform):
            self.uniform.setValue('bboxPos', pos)
            self.uniform.setValue('bboxNeg', neg)


class App():
    def __init__(self):
        self.initDevices()
        self.socket = Server(8002)

        self.initQtwindow()
        self.pos, self.neg = [1, 1, 1], [-1, -1, -1]

    def initDevices(self):
        # setUp realsense
        connected_devices = GetAllRealsenses()
        #connected_devices = []
        self.devicesControls = {}

        # Start streaming from cameras
        for device in connected_devices:
            controls = DevicesControls(device)
            self.devicesControls[device.serial_num] = controls
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

        MainWindow.show()
        MainWindow.destroyed.connect(self.programEnd)

        # window create init opengl
        for key in self.devicesControls:
            device = self.devicesControls[key]
            self.scene.add(device.genPointClouds())

        timer = QTimer(MainWindow)
        timer.timeout.connect(self.mainloop)
        timer.start(1)

        app.exec_()

    def programEnd(self):

        for key in self.devicesControls:
            device = self.devicesControls[key]
            device.device.stop()

        self.socket.stop()

    def monitorScrollBar(self):

        pos, neg = self.uiControls.getboundary()

        for key in self.devicesControls:
            device = self.devicesControls[key]
            device.updateBoundary(pos, neg)

        return pos, neg

    def customPaint(self):
        Glhelper.drawXYZaxis()
        pos, neg = self.monitorScrollBar()
        Glhelper.drawBbox(pos, neg)
        self.pos, self.neg = pos, neg

    def onClientDataRecv(self, dataBytes):
        try:
            data = RealsenseData().fromBytes(dataBytes)
            if(data.serial_num not in self.devicesControls):
                device = Device(data.serial_num, False)
                controls = DevicesControls(device)
                self.devicesControls[device.serial_num] = controls

                self.devicesControls[device.serial_num].setData(data)

                self.scene.add(controls.genPointClouds())
            else:
                self.devicesControls[data.serial_num].setData(data)
        except:
            # packgae decode error
            pass

    def mainloop(self):
        latestBytes = self.socket.getLatestBytes()
        for dataBytes in latestBytes:
            self.onClientDataRecv(dataBytes)

        self.scene.startDraw()

        maps = []
        allcamPos = []
        allcamRot = []

        for key in self.devicesControls:
            device = self.devicesControls[key]
            color_image, depth_colormap = device.updateFrames()
            maps.append([color_image, depth_colormap])
            
            allcamPos.append(device.getCamPos());
            allcamRot.append(device.getCamRot());

        if(self.uiControls.getCalibrationMode()):
            device = self.devicesControls[list(self.devicesControls)[self.uiControls.selectDevice]]
            pos = self.uiControls.getUIPos()
            rot = self.uiControls.getUIRot()
            device.calibration(pos,rot)

        if(len(self.devicesControls.keys()) > 0):
            self.uiControls.setImage(maps)
            self.uiControls.setList(self.devicesControls.keys())
            self.uiControls.setCamPosData(allcamPos)
            self.uiControls.setCamRotData(allcamRot)

        self.scene.endDraw()
        self.uiControls.log("Find {0} realsense(s).".format(
            len(self.devicesControls)))

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
