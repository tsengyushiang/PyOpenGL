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

from opengl.Geometry.ObjGeometry import *
import shaders.cvTexture2D as myShader
import shaders.visuallhull as pcdShader

from Args.medias import build_argparser
args = build_argparser().parse_args()

app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)

scene = QtGLScene(ui.openGLWidget)
scene2 = QtGLScene(ui.openGLWidget_2)


def mainloop():
    scene.startDraw()
    scene.endDraw()
    scene2.startDraw()
    scene2.endDraw()


MainWindow.show()
timer = QTimer(MainWindow)
timer.timeout.connect(mainloop)
timer.start(1)


def genPointCloudMesh(h, w, intr, color, depth, transform):
    texColor = Texture(color)
    texDepth = Texture(color)

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
    uniform.addvec3('bboxPos', [1, 1, 1])
    uniform.addvec3('bboxNeg', [-1, -1, -1])
    uniform.addMat4('extrinct', np.array(transform))

    mat = ShaderMaterial(pcdShader.vertex_shader,
                         pcdShader.fragment_shader,
                         uniform)

    pointCloudGeo = DepthArrGeometry(depth)

    return Mesh(mat, pointCloudGeo)


# uniform
img = cv2.imread(args.texture)
tex = Texture(img)
tex2 = Texture(args.texture2)

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

with open(args.config) as f:
    data = json.load(f)

depth16 = cv2.imread(args.depth, cv2.IMREAD_UNCHANGED)
color = cv2.imread(args.color, cv2.IMREAD_UNCHANGED)
intr = DotMap()
intr.fx = data['depth_fx']
intr.fy = data['depth_fy']
intr.ppx = data['depth_cx']
intr.ppy = data['depth_cy']
pcds = genPointCloudMesh(
    data['depth_height'], data['depth_width'], intr, color, depth16.flatten()*data['depth_scale'], data['calibrateMat'])
scene2.add(pcds)

sys.exit(app.exec_())
