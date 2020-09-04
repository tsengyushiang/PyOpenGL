import cv2
import sys
from qtLayout.twoWindow import *
from PyQt5.QtCore import *

from opengl.Scene.QtGLScene import *
from opengl.Geometry.ObjGeometry import *
from opengl.Material.ShaderMaterial import *
from opengl.Texture import *
from opengl.Mesh import *
from opengl.Uniform import *

import shaders.cvTexture2D as myShader

from Args.singleModelAndTexture import build_argparser
args = build_argparser().parse_args()

app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)

scene = QtGLScene(ui.openGLWidget)
scene2 = QtGLScene(ui.openGLWidget_2)

MainWindow.show()
timer = QTimer(MainWindow)
timer.timeout.connect(scene.update)
timer.timeout.connect(scene2.update)
timer.start(1)

# uniform
img = cv2.imread(args.texture)
tex = Texture(img)
tex2 = Texture('./medias/chess.png')

uniform = Uniform()
uniform.addTexture('texColor', tex)
uniform.addTexture('texDepth', tex2)

# read shader
mat = ShaderMaterial(myShader.vertex_shader,
                     myShader.fragment_shader,
                     uniform)

# read obj file
geo = ObjGeometry(args.model)

mesh = Mesh(mat, geo)

scene.add(mesh)
scene2.add(mesh)

sys.exit(app.exec_())
