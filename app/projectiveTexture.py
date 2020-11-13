import cv2
import sys
import json
from dotmap import DotMap

from qtLayout.twoWindow import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QFileDialog

from opengl.Scene.QtGLScene import *
from opengl.Material.ShaderMaterial import *
from opengl.Texture import *
from opengl.Mesh import *
from opengl.Uniform import *

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

# projective texture model 
uniformModel = Uniform()
tex1 = Texture(np.zeros((2,2)))
uniformModel.addTexture('tex1',tex1)
uniformModel.addMat4('normalizeMat', np.identity(4))
import shaders.projectiveTexture as projectiveTextureShader
matModel = ShaderMaterial(projectiveTextureShader.vertex_shader,
                     projectiveTextureShader.fragment_shader,
                     uniformModel)

from opengl.Geometry.BufferGeometry import *
geoModel = BufferGeometry()
model = Mesh(matModel, geoModel)
model.wireframe = False
scene.add(model)

# texture uv plane
UvPlane = Uniform()
UvPlane.addMat4('normalizeMat', np.identity(4))
UvPlane.addTexture('tex1',tex1)
import shaders.uvTexture as uvTextureShader
matUvPlane = ShaderMaterial(uvTextureShader.vertex_shader,
                     uvTextureShader.fragment_shader,
                     UvPlane)
uvPlane = Mesh(matUvPlane, geoModel)
uvPlane.wireframe = False
scene2.add(uvPlane)

def importResource():
    qfd = QFileDialog()
    filter = "(*.config.json *.color.png *.obj *.png)"
    filenames,_ = QFileDialog.getOpenFileNames(qfd,'import', './', filter)

    for filename in filenames:

        if '.config.json' in filename:
            print('config : ',filename)
        elif '.color.png' in filename:
            print('color : ',filename)
        elif '.png' in filename:

            img = cv2.imread(filename)
            newTex = Texture(img) 

            scene.startDraw()
            newTex.init()
            scene.endDraw()

            scene.startDraw()
            newTex.init()
            scene.endDraw()

            uniformModel.setValue('tex1',newTex)
            UvPlane.setValue('tex1',newTex)

        elif '.obj' in filename:
            scene.startDraw()
            sucess = geoModel.readObj(filename)
            if sucess:
                uniformModel.setValue('normalizeMat',geoModel.getNormalizeMat()) 
                scene2.startDraw()
                geoModel.init()
                scene2.endDraw()
                UvPlane.setValue('normalizeMat',geoModel.getNormalizeMat())       
            
            scene.endDraw()




ui.actionimport.triggered.connect(importResource)

def savePannelAsImage():
    ui.openGLWidget_2.grabFramebuffer().save('./img1.jpg')
    ui.openGLWidget.grabFramebuffer().save('./img2.jpg')

ui.actionscreenshot.triggered.connect(savePannelAsImage)


sys.exit(app.exec_())
