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
uniformModel.addTexture('projectTex',tex1)
uniformModel.addMat4('normalizeMat', np.identity(4))

# camera pose test
uniformModel.addvec3('cam_pose',np.array([
    0.2259568470999498,0.2199078677298788,0.6171844022035089
]))
uniformModel.addMat4('inverTransMat',np.linalg.inv(
    np.array([
        [
            -0.9851929601511762,
            -0.0784819093900398,
            -0.1862612434970548,
            0.2259568470999498
        ],
        [
            -0.0627784000287267,
            0.999779405221067,
            -0.089206743285779,
            0.2199078677298788
        ],
        [
            0.0861751728916132,
            -0.08368264341086802,
            -0.9985133371322,
            0.6171844022035089
        ],
        [
            0.0,
            0.0,
            0.0,
            1.0
        ]
    ])
))

uniformModel.addFloat('ppx',953.74)
uniformModel.addFloat('ppy',560.38)
uniformModel.addFloat('fx',1387.60)
uniformModel.addFloat('fy',1388.31)
uniformModel.addFloat('w',1920)
uniformModel.addFloat('h',1080)

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
UvPlane.addTexture('projectTex',tex1)

# camera pose test
UvPlane.addvec3('cam_pose',np.array([
    0.2259568470999498,0.2199078677298788,0.6171844022035089
]))
UvPlane.addMat4('inverTransMat',np.linalg.inv(
    np.array([
        [
            -0.9851929601511762,
            -0.0784819093900398,
            -0.1862612434970548,
            0.2259568470999498
        ],
        [
            -0.0627784000287267,
            0.999779405221067,
            -0.089206743285779,
            0.2199078677298788
        ],
        [
            0.0861751728916132,
            -0.08368264341086802,
            -0.9985133371322,
            0.6171844022035089
        ],
        [
            0.0,
            0.0,
            0.0,
            1.0
        ]
    ])
))

UvPlane.addFloat('ppx',953.74)
UvPlane.addFloat('ppy',560.38)
UvPlane.addFloat('fx',1387.60)
UvPlane.addFloat('fy',1388.31)
UvPlane.addFloat('w',1920)
UvPlane.addFloat('h',1080)

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
            with open(filename) as f:
                data = json.load(f)
            
            UvPlane.setValue('cam_pose',np.array([data['calibrateMat'][0][3],data['calibrateMat'][1][3],data['calibrateMat'][2][3]]))
            UvPlane.setValue('inverTransMat',np.linalg.inv(
                np.array(data['calibrateMat'])
            ))

            UvPlane.setValue('ppx',data['rgb_cx'])
            UvPlane.setValue('ppy',data['rgb_cy'])
            UvPlane.setValue('fx',data['rgb_fx'])
            UvPlane.setValue('fy',data['rgb_fy'])
            UvPlane.setValue('w',data['rgb_width'])
            UvPlane.setValue('h',data['rgb_height'])
            uniformModel.setValue('cam_pose',np.array([data['calibrateMat'][0][3],data['calibrateMat'][1][3],data['calibrateMat'][2][3]]))
            uniformModel.setValue('inverTransMat',np.linalg.inv(
                np.array(data['calibrateMat'])
            ))

            uniformModel.setValue('ppx',data['rgb_cx'])
            uniformModel.setValue('ppy',data['rgb_cy'])
            uniformModel.setValue('fx',data['rgb_fx'])
            uniformModel.setValue('fy',data['rgb_fy'])
            uniformModel.setValue('w',data['rgb_width'])
            uniformModel.setValue('h',data['rgb_height'])

        elif '.color.png' in filename:
            img = cv2.imread(filename)
            newTex = Texture(img) 

            scene.startDraw()
            newTex.init()
            scene.endDraw()

            scene.startDraw()
            newTex.init()
            scene.endDraw()

            uniformModel.setValue('projectTex',newTex)
            UvPlane.setValue('projectTex',newTex)
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
    ui.openGLWidget_2.grabFramebuffer().save('./texture.png')

ui.actionscreenshot.triggered.connect(savePannelAsImage)


sys.exit(app.exec_())
