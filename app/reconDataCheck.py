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
from opengl.Geometry.PointGeometry import *

import shaders.cvTexture2D as myShader
import shaders.basic as basic
import shaders.realsensePointCloud as pcdShader

import FileIO.ply as ply
from scipy.spatial.transform import Rotation as R

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

points46, colors46 = ply.readPlyPoints('./medias/recon/1577709670_46000.ply')
points114, colors114 = ply.readPlyPoints('./medias/recon/1577709924_11400.ply')
q_and_v46 = [- 0.49379623692040214, - 0.550592046995946,
             0.9752177656522548, 0.04823144684779833, 0.9757893847046863, 0.17369432305950616, 0.1238510652740531]

q_and_v114 = [- 1.2133381930260743, - 0.5428483836758571, -
              0.2998904051026752, - 0.1396203104004467, 0.587638359290595, 0.07663134903207569, 0.7932937438045662]

geo1 = PointGeometry(points46, colors46)
uniform1 = Uniform()
r1 = R.from_quat(q_and_v46[3:])
m1 = r1.as_matrix()
uniform1.addMat4('extrinct', np.array([
    [m1[0][0], m1[0][1], m1[0][2], q_and_v46[0]],
    [m1[1][0], m1[1][1], m1[1][2], q_and_v46[1]],
    [m1[2][0], m1[2][1], m1[2][2], q_and_v46[2]],
    [0.0, 0.0, 0.0, 1.0]
]))
basicMat1 = ShaderMaterial(basic.vertex_shader,
                           basic.fragment_shader,
                           uniform1)
mesh1 = Mesh(basicMat1, geo1)
scene2.add(mesh1)

geo2 = PointGeometry(points114, colors114)
uniform2 = Uniform()
r2 = R.from_quat(q_and_v114[3:])
m2 = r2.as_matrix()
uniform2.addMat4('extrinct', np.array([
    [m2[0][0], m2[0][1], m2[0][2], q_and_v114[0]],
    [m2[1][0], m2[1][1], m2[1][2], q_and_v114[1]],
    [m2[2][0], m2[2][1], m2[2][2], q_and_v114[2]],
    [0.0, 0.0, 0.0, 1.0]
]))
basicMat2 = ShaderMaterial(basic.vertex_shader,
                           basic.fragment_shader,
                           uniform2)

mesh2 = Mesh(basicMat2, geo2)
scene2.add(mesh2)

sys.exit(app.exec_())
