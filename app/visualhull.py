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

with open(args.config1) as f:
    data = json.load(f)

with open(args.config2) as f:
    data2 = json.load(f)


depth1 = cv2.imread(args.depth1, cv2.IMREAD_UNCHANGED).astype('uint8')
depth2 = cv2.imread(args.depth2, cv2.IMREAD_UNCHANGED).astype('uint8')

w = 512
h = 512
d = 512

# add scene
uniform = Uniform()
uniform.addTexture('texDepth1', depth1)
uniform.addTexture('texDepth2', depth2)
uniform.addFloat('fx', data['depth_fx'])
uniform.addFloat('fy', data['depth_fy'])
uniform.addFloat('ppx', data['depth_cx'])
uniform.addFloat('ppy', data['depth_cy'])
uniform.addFloat('w', w)
uniform.addFloat('h', h)
uniform.addFloat('d', d)
uniform.addMat4('extrinct1', np.array(data['calibrateMat']))
uniform.addMat4('extrinct2', np.array(data2['calibrateMat']))

mat = ShaderMaterial(pcdShader.vertex_shader,
                        pcdShader.fragment_shader,
                        uniform)

print(np.ones(w*h*d))
pointCloudGeo = DepthArrGeometry(np.ones(w*h*d))
scene2.add(pointCloudGeo)

sys.exit(app.exec_())
