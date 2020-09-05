import sys
import cv2
from qtLayout.fourRealsense import *
from PyQt5.QtCore import *

from Aruco.Aruco import Aruco

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
    uniform.addvec3('maker1', [0, 0, 0])
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

# setUp realsense
connected_devices = GetAllRealsenses()

# Start streaming from cameras
for device in connected_devices:
    device.start()

MainWindow.show()

aruco = Aruco()
#aruco.saveMarkers()

# render loop


def mainLoop():
    scene.update()
    for index, device in enumerate(connected_devices):
        color_image, depth_colormap, pointcloud = device.getFrames()

        # Aruco test
        markerPixel1, markerPixel2 = aruco.findMarkers(color_image)
        markerPoint1 = device.pixel2point(markerPixel1)
        markerPoint2 = device.pixel2point(markerPixel2)

        uniforms[index].setValue('maker1', markerPoint1)
        uniforms[index].setValue('maker2', markerPoint2)

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
