import cv2
import sys
import json
from dotmap import DotMap

from qtLayout.MeshSimplifacation import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QFileDialog

from opengl.Scene.QtGLScene import *
from opengl.Geometry.DepthArrGeometry import *
from opengl.Material.ShaderMaterial import *
from opengl.Texture import *
from opengl.Mesh import *
from opengl.Uniform import *

from opengl.Geometry.OpenMeshGeometry import *
import shaders.PhongLightingTransMat as myShader
import shaders.realsensePointCloud as pcdShader

from Args.medias import build_argparser
args = build_argparser().parse_args()

app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)

# setup scene
scene = QtGLScene(ui.openGLWidget)
MainWindow.show()

# skeleton extration mesh
uniformSkeleton = Uniform()
uniformSkeleton.addvec3('viewPos', [0, 0, -1])
uniformSkeleton.addMat4('normalizeMat', np.identity(4))
matSkeleton = ShaderMaterial(myShader.vertex_shader,
                     myShader.fragment_shader,
                     uniformSkeleton)
geoSkeleton = OpenMeshGeometry()
skeletonMesh = Mesh(matSkeleton, geoSkeleton)
skeletonMesh.visible = False
scene.add(skeletonMesh)

# QEM simplification mesh
uniformSimplify = Uniform()
uniformSimplify.addvec3('viewPos', [0, 0, -1])
uniformSimplify.addMat4('normalizeMat', np.identity(4))
matSimplify = ShaderMaterial(myShader.vertex_shader,
                     myShader.fragment_shader,
                     uniformSimplify)
geoSimplify = OpenMeshGeometry()
simplifyMesh = Mesh(matSimplify, geoSimplify)
simplifyMesh.visible = False
scene.add(simplifyMesh)

# midpoint simplification
uniformMidSimplify = Uniform()
uniformMidSimplify.addvec3('viewPos', [0, 0, -1])
uniformMidSimplify.addMat4('normalizeMat', np.identity(4))
matMidSimplify = ShaderMaterial(myShader.vertex_shader,
                     myShader.fragment_shader,
                     uniformMidSimplify)
geoMidSimplify = OpenMeshGeometry()
midSimplifyMesh = Mesh(matMidSimplify, geoMidSimplify)
midSimplifyMesh.visible = True
scene.add(midSimplifyMesh)


# setup UI
def importObj():
    filename,_ = QFileDialog.getOpenFileName()

    print(filename)
    scene.startDraw()
    sucess = geoSkeleton.readObj(filename)
    if sucess:
        uniformSkeleton.setValue('normalizeMat',geoSkeleton.getNormalizeMat())
    
    sucess = geoSimplify.readObj(filename)
    if sucess:
        uniformSimplify.setValue('normalizeMat',geoSimplify.getNormalizeMat())
    
    sucess = geoMidSimplify.readObj(filename)
    if sucess:
        uniformMidSimplify.setValue('normalizeMat',geoMidSimplify.getNormalizeMat())

    scene.endDraw()
ui.pushButton_2.clicked.connect(importObj)

updateSkeleton = False
def enableSkeletonExtraction():
    global updateSkeleton
    updateSkeleton = True
ui.pushButton_4.clicked.connect(enableSkeletonExtraction)

updateSimplify = False
def enableSimplify():
    global updateSimplify
    geoSimplify.quadric_Init()
    updateSimplify = True
ui.pushButton_3.clicked.connect(enableSimplify)

updateMidSimplify = False
def enableMidSimplify():
    global updateMidSimplify
    updateMidSimplify = True
ui.pushButton.clicked.connect(enableMidSimplify)

def onHandleSkeletonSlider(value):
    skeletonMesh.visible = True
    simplifyMesh.visible = False
    midSimplifyMesh.visible = False


    range = ui.horizontalScrollBar_2.maximum()-ui.horizontalScrollBar_2.minimum()
    geoSkeleton.setLevel(float(value)/range)        
ui.horizontalScrollBar_2.valueChanged.connect(onHandleSkeletonSlider)

def onHandleSimplifySlider(value):
    skeletonMesh.visible = False
    simplifyMesh.visible = True
    midSimplifyMesh.visible = False

    range = ui.horizontalScrollBar_3.maximum()-ui.horizontalScrollBar_3.minimum()
    geoSimplify.setLevel(float(value)/range)        
ui.horizontalScrollBar_3.valueChanged.connect(onHandleSimplifySlider)

def onHandleMidSimplifySlider(value):
    skeletonMesh.visible = False
    simplifyMesh.visible = False
    midSimplifyMesh.visible = True

    range = ui.horizontalScrollBar.maximum()-ui.horizontalScrollBar.minimum()
    geoMidSimplify.setLevel(float(value)/range)        
ui.horizontalScrollBar.valueChanged.connect(onHandleMidSimplifySlider)


# render
def mainloop():
    global updateSkeleton,updateSimplify,updateMidSimplify
    uniformSkeleton.setValue('viewPos', [
        scene.camera.position[0],
        scene.camera.position[1],
        scene.camera.position[2]])
    
    uniformSimplify.setValue('viewPos', [
        scene.camera.position[0],
        scene.camera.position[1],
        scene.camera.position[2]])
    
    uniformMidSimplify.setValue('viewPos', [
        scene.camera.position[0],
        scene.camera.position[1],
        scene.camera.position[2]]) 

    scene.startDraw()


    start = time.time()
    if updateSkeleton:
        try:
            updateSkeleton = geoSkeleton.contraction()
            geoSkeleton.init()
        except:
            updateSkeleton = False
    
    if updateSimplify:
        try:
            updateSimplify = geoSimplify.errorQuadrics()
            geoSimplify.init()
        except:
            updateSimplify = False
    
    if updateMidSimplify:
        try:
            print('simplify')
            updateMidSimplify = geoMidSimplify.collapseFirstEdge()
            geoMidSimplify.init()
        except:
            updateMidSimplify = False

    scene.endDraw()

timer = QTimer(MainWindow)
timer.timeout.connect(mainloop)
timer.start(1)

sys.exit(app.exec_())
