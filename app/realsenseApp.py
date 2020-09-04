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

import shaders.basic as myShader

from Args.singleModelAndTexture import build_argparser
args = build_argparser().parse_args()

# init Qt window
app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)

# setup QtWidgets and openGL, opencv
scene = QtGLScene(ui.openGLWidget)

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


timer = QTimer(MainWindow)
timer.timeout.connect(mainLoop)
timer.start(1)

# add scene
uniform = Uniform()
mat = ShaderMaterial(myShader.vertex_shader,
                     myShader.fragment_shader,
                     uniform)

# read obj file
geo = ObjGeometry(args.model)
mesh = Mesh(mat, geo)
scene.add(mesh)

sys.exit(app.exec_())
