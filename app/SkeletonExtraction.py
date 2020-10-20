import cv2
import sys
import json
from dotmap import DotMap

from qtLayout.MeshSimplifacation import *
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

from Args.medias import build_argparser
args = build_argparser().parse_args()

app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)

scene = QtGLScene(ui.openGLWidget)

# uniform
uniform = Uniform()

MainWindow.show()

uniform.addvec3('viewPos', [0, 0, -1])
geo = OpenMeshGeometry(args.highResModel)

def onHandleSlider(value):
    range = ui.horizontalScrollBar.maximum()-ui.horizontalScrollBar.minimum()
    geo.setLevel(float(value)/range)
        
ui.horizontalScrollBar.valueChanged.connect(onHandleSlider)

normalizeMat = geo.getNormalizeMat()
uniform.addMat4('normalizeMat', normalizeMat)

mat = ShaderMaterial(myShader.vertex_shader,
                     myShader.fragment_shader,
                     uniform)

mesh = Mesh(mat, geo)
scene.add(mesh)

updateSimplification = True
def mainloop():
    global i,updateSimplification
    uniform.setValue('viewPos', [
        scene.camera.position[0],
        scene.camera.position[1],
        scene.camera.position[2]])
    scene.startDraw()

    start = time.time()    
    if updateSimplification:
        try:
            updateSimplification = geo.contraction()
            geo.init()
            print('success')
        except:
            updateSimplification=False
    #print('collapse a edge cost ',time.time()-start)
    
    scene.endDraw()
timer = QTimer(MainWindow)
timer.timeout.connect(mainloop)
timer.start(1)

sys.exit(app.exec_())
