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

from Algorithm.marchingCube import *

import shaders.visuallhull as visualhullShader
import shaders.realsensePointCloud as pcdShader

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

with open(args.config1) as f:
    data = json.load(f)

with open(args.config2) as f:
    data2 = json.load(f)

vL = 100
depth1 = cv2.imread(args.depth1, cv2.IMREAD_UNCHANGED)
sampleDepth = cv2.resize(depth1, (vL,vL), interpolation=cv2.INTER_NEAREST).flatten()
depth1 = depth1.astype('uint8')
depth2 = cv2.imread(args.depth2, cv2.IMREAD_UNCHANGED).astype('uint8')
depth1 = cv2.cvtColor(depth1, cv2.COLOR_GRAY2BGR)
depth2 = cv2.cvtColor(depth2, cv2.COLOR_GRAY2BGR)
color1 = cv2.imread(args.color1)

scale=2
# add scene
uniform = Uniform()

tex1 = Texture(color1)
tex2 = Texture(depth1)

uniform.addTexture('texDepth1', tex1)
uniform.addTexture('texDepth2', tex2)
uniform.addFloat('fx', data['depth_fx'])
uniform.addFloat('fy', data['depth_fy'])
uniform.addFloat('ppx', data['depth_cx'])
uniform.addFloat('ppy', data['depth_cy'])
uniform.addFloat('w', data['depth_width'])
uniform.addFloat('h', data['depth_height'])
uniform.addFloat('vL', vL)
uniform.addFloat('scale', scale)
uniform.addMat4('extrinct1', np.linalg.inv(np.array(data['calibrateMat'])))
uniform.addMat4('extrinct2', np.linalg.inv(np.array(data2['calibrateMat'])))

mat = ShaderMaterial(visualhullShader.vertex_shader,
                        visualhullShader.fragment_shader,
                        uniform)

pointCloudGeo = DepthArrGeometry(np.tile(sampleDepth,vL)*data['depth_scale'])
mesh = Mesh(mat, pointCloudGeo)

scene2.add(mesh)

depth1 = cv2.imread(args.depth1, cv2.IMREAD_UNCHANGED)
color1 = cv2.imread(args.color1, cv2.IMREAD_UNCHANGED)
intr = DotMap()
intr.fx = data['depth_fx']
intr.fy = data['depth_fy']
intr.ppx = data['depth_cx']
intr.ppy = data['depth_cy']
pcds = genPointCloudMesh(
    data['depth_height'], data['depth_width'], intr, color1, depth1.flatten()*data['depth_scale'], data['calibrateMat'])
scene2.add(pcds)
'''
depth2 = cv2.imread(args.depth2, cv2.IMREAD_UNCHANGED)
color2 = cv2.imread(args.color2, cv2.IMREAD_UNCHANGED)
intr2 = DotMap()
intr2.fx = data2['depth_fx']
intr2.fy = data2['depth_fy']
intr2.ppx = data2['depth_cx']
intr2.ppy = data2['depth_cy']
pcds = genPointCloudMesh(
    data2['depth_height'], data2['depth_width'], intr2, color2, depth2.flatten()*data2['depth_scale'], data2['calibrateMat'])
scene2.add(pcds)
'''
'''
a1 = np.ones(5*5*3)
a2 = np.zeros(5*5*2)
k =  np.concatenate((a1,a2))
k=k.reshape((5,5,5))
marchingCube(k,visualize=True)
'''
sys.exit(app.exec_())
