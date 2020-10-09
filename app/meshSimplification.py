import cv2
import sys
import json
from dotmap import DotMap

from qtLayout.twoWindow import *
from PyQt5.QtCore import *

from opengl.Scene.QtGLScene import *
from opengl.Geometry.DepthArrGeometry import *
from opengl.Material.ShaderMaterial import *
from opengl.Texture import *
from opengl.Mesh import *
from opengl.Uniform import *

from opengl.Geometry.OpenMeshGeometry import *
import shaders.PhongLightingTransMat as myShader
import shaders.realsensePointCloud as pcdShader
from Algorithm.open3D.pointCloud import normalEstimate

from Args.medias import build_argparser
args = build_argparser().parse_args()

app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)

scene = QtGLScene(ui.openGLWidget)

# uniform
uniform = Uniform()
uniform.addvec3('viewPos', [0, 0, -1])


def mainloop():
    uniform.setValue('viewPos', [
        scene.camera.position[0],
        scene.camera.position[1],
        scene.camera.position[2]])
    scene.startDraw()
    scene.endDraw()


MainWindow.show()

geo = OpenMeshGeometry(args.highResModel)

normalizeMat = geo.getNormalizeMat()
uniform.addMat4('normalizeMat', normalizeMat)

mat = ShaderMaterial(myShader.vertex_shader,
                     myShader.fragment_shader,
                     uniform)

mesh = Mesh(mat, geo)
scene.add(mesh)

timer = QTimer(MainWindow)
timer.timeout.connect(mainloop)
timer.start(1)

sys.exit(app.exec_())
