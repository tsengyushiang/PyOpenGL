import cv2
import sys
import json
import os
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

from FileIO.ply import savePcd,save

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

vL = 250
depth1 = cv2.imread(args.depth1, cv2.IMREAD_UNCHANGED)
sampleDepth = cv2.resize(depth1, (vL,vL), interpolation=cv2.INTER_NEAREST)
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

depthvalues = np.tile(sampleDepth.flatten(),vL)*data['depth_scale']

pointCloudGeo = DepthArrGeometry(depthvalues)
mesh = Mesh(mat, pointCloudGeo)

scene2.add(mesh)

depth16 = cv2.imread(args.depth1, cv2.IMREAD_UNCHANGED)
color1 = cv2.imread(args.color1, cv2.IMREAD_UNCHANGED)
intr = DotMap()
intr.fx = data['depth_fx']
intr.fy = data['depth_fy']
intr.ppx = data['depth_cx']
intr.ppy = data['depth_cy']
pcds = genPointCloudMesh(
    data['depth_height'], data['depth_width'], intr, color1, depth16.flatten()*data['depth_scale'], data['calibrateMat'])
scene2.add(pcds)

vertices = []
color = []

fx=data['depth_fx']
fy=data['depth_fy']
ppx=data['depth_cx']
ppy=data['depth_cy']
w=data['depth_width']
h=data['depth_height']

def point2pixel(point,depthValue):
    u = (point.x/depthValue*fx+ppx)/w
    v = (point.y/depthValue*fy+ppy)/h
    return u,v

def convertIndex2xyz(gl_VertexID):
    z = ((gl_VertexID/(vL*vL)))/vL
    zRemain = gl_VertexID%(vL*vL)
    y = vL- zRemain/vL
    x = zRemain%vL
    return x,y,z

for gl_VertexID,depthValue in enumerate(depthvalues):
    x,y,z = convertIndex2xyz(gl_VertexID)
    
    point = DotMap()
    point.x = x/vL-0.5
    point.y = y/vL-0.5
    point.z = z

    depthvalues[gl_VertexID]=0

    if depthValue!=0 :
        u,v = point2pixel(point,depthValue)
        if u>0 and u<1.0 and v>0 and v<1.0 :

            c = color1[int((1-v)*h)][int(u*w)]
            d = depth16[int((1-v)*h)][int(u*w)]

            if d*data['depth_scale'] < z and d>0:
                vertices.append([point.x,point.y,point.z])
                color.append([c[2]/255.0,c[1]/255.0,c[1]/255.0])
                depthvalues[gl_VertexID]=1    

savePcd(vertices,color,os.path.join(args.output,'depthhull.ply'))

#verts, faces, normals = marchingCube(depthvalues.reshape((vL,vL,vL)))

sys.exit(app.exec_())
