import sys
import cv2
import datetime
import os

from qtLayout.fourRealsense import *
from PyQt5.QtCore import *

from Aruco.Aruco import Aruco
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

# init Qt window
app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)

# setup QtWidgets and openGL, opencv
scene = QtGLScene(ui.openGLWidget)
scene.update()

imgsTextures = []
pointCloudGeos = []
uniforms = []
pos = [1, 1, 1]
neg = [-1, -1, -1]


def addPointClouds(w, h, intr):
    texColor = Texture(np.full((h, w, 3), 0, dtype="uint8"))
    texDepth = Texture(np.full((h, w, 3), 255, dtype="uint8"))
    imgsTextures.append([texColor, texDepth])

    # add scene
    uniform = Uniform()
    uniform.addTexture('texColor', texColor)
    uniform.addTexture('texDepth', texDepth)
    uniform.addFloat('fx', intr.fx)
    uniform.addFloat('fy', intr.fy)
    uniform.addFloat('ppx', intr.ppx)
    uniform.addFloat('ppy', intr.ppy)
    uniform.addFloat('w', w)
    uniform.addFloat('h', h)
    uniform.addvec3('bboxPos', pos)
    uniform.addvec3('bboxNeg', neg)
    uniform.addMat4('extrinct', np.array([
        [1.0, 0.0, 0.0, 0.0],
        [0.0, 1.0, 0.0, 0.0],
        [0.0, 0.0, 1.0, 0.0],
        [0.0, 0.0, 0.0, 1.0]
    ]))

    uniforms.append(uniform)

    mat = ShaderMaterial(myShader.vertex_shader,
                         myShader.fragment_shader,
                         uniform)

    geo = DepthArrGeometry(np.ones(w*h))
    pointCloudGeos.append(geo)

    mesh = Mesh(mat, geo)
    scene.add(mesh)


imgBlocks = [
    [QtcvImage(ui.label00), QtcvImage(ui.label01)],
    [QtcvImage(ui.label10), QtcvImage(ui.label11)],
    [QtcvImage(ui.label20), QtcvImage(ui.label21)],
    [QtcvImage(ui.label30), QtcvImage(ui.label31)]


]

calibrationCheckBox = ui.checkBox

# setUp realsense
connected_devices = GetAllRealsenses()

# Start streaming from cameras
for device in connected_devices:
    device.start()

MainWindow.show()

aruco = Aruco()
# aruco.saveMarkers()

# render loop


def calibration(color_image, index):
    # Aruco test
    corner1, middle, corner2, middle2, num = aruco.findMarkers(
        color_image)

    def reset():
        uniforms[index].setValue('extrinct', np.array([
                [1.0, 0.0, 0.0, 0.0],
                [0.0, 1.0, 0.0, 0.0],
                [0.0, 0.0, 1.0, 0.0],
                [0.0, 0.0, 0.0, 1.0]
        ]))
        # print("calibration error")

    if(num > 0):
        markerPoint1 = connected_devices[index].pixel2point(corner1)
        markerPointMiddle = connected_devices[index].pixel2point(middle)
        markerPoint2 = connected_devices[index].pixel2point(corner2)
        markerPointMiddle2 = connected_devices[index].pixel2point(middle2)

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

        '''
        coordMarker = np.array([
            [x[0], -y[0], z[0], centerPoint[0]],
            [x[1], -y[1], z[1], centerPoint[1]],
            [x[2], -y[2], z[2], centerPoint[2]],
            [0, 0, 0, 1.0]
        ])
        '''
        coordMarker = np.array([
            [1.0, 0, 0, markerPoint1[0]],
            [0, 1.0, 0, markerPoint1[1]],
            [0, 0, 1.0, markerPoint1[2]],
            [0, 0, 0, 1.0]
        ])

        try:
            inverCoordMarker = np.linalg.inv(coordMarker)
            uniforms[index].setValue('extrinct', inverCoordMarker)
        except:
            reset()
    else:
        reset()


def monitorScrollBar():
    pos[0] = ui.posX.value()/10
    pos[1] = ui.posY.value()/10
    pos[2] = ui.posZ.value()/10
    neg[0] = ui.negX.value()/10
    neg[1] = ui.negY.value()/10
    neg[2] = ui.negZ.value()/10

    for uniform in uniforms:
        uniform.setValue('bboxPos', pos)
        uniform.setValue('bboxNeg', neg)


def customPaint():
    Glhelper.drawXYZaxis()
    Glhelper.drawBbox(pos, neg)
    monitorScrollBar()


scene.customRender.append(customPaint)


def save():
    currentTime = datetime.datetime.now()
    currentTimeStr = currentTime.strftime("%Y%m%d_%H%M%S_%f")[:-3]
    # print(currentTimeStr)
    path = os.getcwd()
    # print("The current working directory is %s" % path)
    saveRootPath = os.path.join(path, currentTimeStr)
    os.mkdir(saveRootPath)

    for index, device in enumerate(connected_devices):
        device.saveFrames(saveRootPath)
        serial_num = device.serial_num

        mat4 = uniforms[index].getValue('extrinct')

        clipPoints = []
        for points in device.getPoints().reshape(device.h*device.w, 3):
            vec = np.array([points[0], points[1], points[2], 1.0])
            alignedVec = mat4.dot(vec)

            if(pos[0] < alignedVec[0] or
               pos[1] < alignedVec[1] or
               pos[2] < alignedVec[2] or
               neg[0] > alignedVec[0] or
               neg[1] > alignedVec[1] or
               neg[2] > alignedVec[2]):
                continue

            clipPoints.append((alignedVec[0], alignedVec[1], alignedVec[2]))

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


ui.pushButton.clicked.connect(save)


def mainLoop():
    scene.update()
    for index, device in enumerate(connected_devices):
        color_image, depth_colormap, depthValues = device.getFrames()

        if(calibrationCheckBox.checkState() != 0):
            calibration(color_image, index)

        # update qt image box
        imgBlocks[index][0].setImage(color_image)
        imgBlocks[index][1].setImage(depth_colormap)

        # update opengl texture
        imgsTextures[index][0].update(color_image)
        imgsTextures[index][1].update(depth_colormap)

        # print(pointcloud)
        pointCloudGeos[index].update(depthValues)

    scene.updateDone()


timer = QTimer(MainWindow)
timer.timeout.connect(mainLoop)
timer.start(1)

for device in connected_devices:
    addPointClouds(device.w, device.h, device.intr)

ui.statusbar.showMessage(
    "Find {0} realsense(s).".format(len(connected_devices)))

app.exec_()
