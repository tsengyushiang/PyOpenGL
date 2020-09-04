import sys
import cv2
from qtLayout.fourRealsense import *
from PyQt5.QtCore import *

from Realsense.device import *

from opencv.QtcvImage import *

from opengl.Scene.QtGLScene import *
from opengl.Geometry.ObjGeometry import *
from opengl.Material.ShaderMaterial import *
from opengl.Mesh import *
from opengl.Uniform import *
from opengl.Texture import *

import shaders.cvTexture2D as myShader

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

imgs = []


def addPointClouds(w, h):
    texColor = Texture(np.full((w, h, 3), 0, dtype="uint8"))
    texDepth = Texture(np.full((w, h, 3), 255, dtype="uint8"))
    imgs.append([texColor, texDepth])

    # add scene
    uniform = Uniform()
    uniform.addTexture('texColor', texColor)
    uniform.addTexture('texDepth', texDepth)

    mat = ShaderMaterial(myShader.vertex_shader,
                         myShader.fragment_shader,
                         uniform)

    # read obj file
    geo = ObjGeometry(args.model)
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

# render loop

def mainLoop():
    scene.update()
    for index, device in enumerate(connected_devices):
        color_image, depth_colormap = device.getFrames()
        imgBlocks[index][0].setImage(color_image)
        imgBlocks[index][1].setImage(depth_colormap)
        imgs[index][0].update(color_image)
        imgs[index][1].update(depth_colormap)

    scene.updateDone()


timer = QTimer(MainWindow)
timer.timeout.connect(mainLoop)
timer.start(1)

addPointClouds(720, 1280)

app.exec_()
