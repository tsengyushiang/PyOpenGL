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

uniform = Uniform()
uniform.addvec3('viewPos', [0, 0, -1])
uniform.addMat4('normalizeMat', np.identity(4))
mat = ShaderMaterial(myShader.vertex_shader,
                     myShader.fragment_shader,
                     uniform)
geo = OpenMeshGeometry()
mesh = Mesh(mat, geo)
scene.add(mesh)

# setup UI
def importObj():
    filename,_ = QFileDialog.getOpenFileName()

    print(filename)
    scene.startDraw()
    sucess = geo.readObj(filename)
    if sucess:
        uniform.setValue('normalizeMat',geo.getNormalizeMat())
    scene.endDraw()

ui.pushButton_2.clicked.connect(importObj)

def onHandleSlider(value):
    range = ui.horizontalScrollBar.maximum()-ui.horizontalScrollBar.minimum()
    geo.setLevel(float(value)/range)        
ui.horizontalScrollBar.valueChanged.connect(onHandleSlider)
'''
def onHandleSlider(value):
    range = ui.horizontalScrollBar.maximum()-ui.horizontalScrollBar.minimum()
    geo.setLevel(float(value)/range)        
ui.horizontalScrollBar.valueChanged.connect(onHandleSlider)

def onHandleSlider(value):
    range = ui.horizontalScrollBar.maximum()-ui.horizontalScrollBar.minimum()
    geo.setLevel(float(value)/range)        
ui.horizontalScrollBar.valueChanged.connect(onHandleSlider)
'''

# render
updateSimplification = True
def mainloop():
    global i,updateSimplification
    uniform.setValue('viewPos', [
        scene.camera.position[0],
        scene.camera.position[1],
        scene.camera.position[2]])
    scene.startDraw()

    start = time.time()
    '''
    if updateSimplification:
        try:
            updateSimplification = geo.contraction()
            geo.init()
            print('success')
        except:
            updateSimplification=False
    '''
    #print('collapse a edge cost ',time.time()-start)    
    scene.endDraw()

timer = QTimer(MainWindow)
timer.timeout.connect(mainloop)
timer.start(1)

sys.exit(app.exec_())
