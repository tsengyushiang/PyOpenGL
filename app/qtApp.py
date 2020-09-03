import sys
from qtLayout.twoWindow import *
from opengl.QtGLScene import *
from PyQt5.QtCore import *

from opengl.WxGLScene import *
from opengl.GlutScene import *
from opengl.Geometry import *
from opengl.Texture import *
from opengl.ShaderMaterial import *
from opengl.Mesh import *
from opengl.Uniform import *
import shaders.texture2D as myShader

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
tex = Texture(args.texture)
tex2 = Texture('./medias/chess.png')

uniform = Uniform()
uniform.addTexture('tex', tex)
uniform.addTexture('tex2', tex2)

# read shader
mat = ShaderMaterial(myShader.vertex_shader,
                     myShader.fragment_shader,
                     uniform)

# read obj file
geo = Geometry(args.model)

mesh = Mesh(mat, geo)

scene.add(mesh)
scene2.add(mesh)

sys.exit(app.exec_())
