import sys
import cv2
from qtLayout.fourRealsense import *
from PyQt5.QtCore import *

from Aruco.Aruco import Aruco
from Algorithm.vector3D import rotation_matrix_from_vectors

from Realsense.device import *

from opencv.QtcvImage import *

from opengl.Scene.QtGLScene import *
from opengl.Geometry.PointGeometry import *
from opengl.Geometry.ObjGeometry import *
from opengl.Material.ShaderMaterial import *
from opengl.Mesh import *
from opengl.Uniform import *
from opengl.Texture import *

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
    uniform.addvec3('offset', [0, 0, 0])
    uniform.addvec3('maker2', [0, 0, 0])
    uniform.addMat4('extrinct', [
        [1.0, 0.0, 0.0, 0.0],
        [0.0, 1.0, 0.0, 0.0],
        [0.0, 0.0, 1.0, 0.0],
        [0.0, 0.0, 0.0, 1.0]
    ])

    uniforms.append(uniform)

    mat = ShaderMaterial(myShader.vertex_shader,
                         myShader.fragment_shader,
                         uniform)

    geo = PointGeometry(np.empty((w*h, 3), dtype=float))
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
        #print("calibration error")

    if(num > 0):
        markerPoint1 = device.pixel2point(corner1)
        markerPointMiddle = device.pixel2point(middle)
        markerPoint2 = device.pixel2point(corner2)
        markerPointMiddle2 = device.pixel2point(middle2)

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
            uniforms[index].setValue('extrinct', inverCoordMarker)
        except:
            reset()
    else:
        reset()


def mainLoop():
    scene.update()
    for index, device in enumerate(connected_devices):
        color_image, depth_colormap, pointcloud = device.getFrames()

        if(calibrationCheckBox.checkState() != 0):
            calibration(color_image, index)

            # update qt image box
        imgBlocks[index][0].setImage(color_image)
        imgBlocks[index][1].setImage(depth_colormap)

        # update opengl texture
        imgsTextures[index][0].update(color_image)
        imgsTextures[index][1].update(depth_colormap)

        # print(pointcloud)
        pointCloudGeos[index].update(pointcloud)

    scene.updateDone()


timer = QTimer(MainWindow)
timer.timeout.connect(mainLoop)
timer.start(1)

for device in connected_devices:
    addPointClouds(device.w, device.h, device.intr)

ui.statusbar.showMessage(
    "Find {0} realsense(s).".format(len(connected_devices)))

app.exec_()
