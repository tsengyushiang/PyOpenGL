from Args.realsense import build_argparser
import sys
import cv2
import os
import copy

from qtLayout.RealsenseApp import *
from PyQt5.QtCore import *

from Aruco.Aruco import ArucoInstance

from Network.socket.Server import Server
from Network.socket.Client import Client
from Network.socket.Enum import Socket

from Realsense.device import *
from Realsense.NetworkData import RealsenseData

from opencv.QtcvImage import *

from opengl.Scene.QtGLScene import *
from opengl.Geometry.DepthArrGeometry import *
from opengl.Material.ShaderMaterial import *
from opengl.Mesh import *
from opengl.Uniform import *
from opengl.Texture import *
import opengl.Helper as Glhelper

import FileIO.json as json

import shaders.realsensePointCloud as myShader

from scipy.spatial.transform import Rotation
args = build_argparser().parse_args()


class UIControls():
    def __init__(self, ui, MainWindow):
        self.ui = ui
        self.MainWindow = MainWindow
        self.ui.setupUi(self.MainWindow)

        self.imgBlocks = [
            [QtcvImage(ui.color), QtcvImage(ui.depth)]
        ]

        self.selectDevice = 0
        self.listData = []
        self.camPosData = []
        self.camRotData = []

        self.ui.radioButton.clicked.connect(
            self.radioButtonChecked(Socket.CLIENT))
        self.ui.radioButton_2.clicked.connect(
            self.radioButtonChecked(Socket.SERVER))
        self.ui.radioButton_3.clicked.connect(
            self.radioButtonChecked(Socket.LOCAL))

        def doNothing():
            pass

        def setIpPort(ip, port):
            return ip, port

        def getIpPort(port):
            return '127.0.0.1', port
        self.onServerButtonClick = getIpPort
        self.onClientButtonClick = setIpPort
        self.onLocalButtonClick = doNothing

    def getCanvas(self):
        return self.ui.openGLWidget

    def getboundary(self):
        pos = [0, 0, 0]
        neg = [0, 0, 0]
        scale = 100
        pos[0] = self.ui.posX.value()/scale
        pos[1] = self.ui.posY.value()/scale
        pos[2] = self.ui.posZ.value()/scale
        neg[0] = self.ui.negX.value()/scale
        neg[1] = self.ui.negY.value()/scale
        neg[2] = self.ui.negZ.value()/scale
        return pos, neg

    def setImage(self, maps):

        color = maps[self.selectDevice][0]
        depth = maps[self.selectDevice][1]

        self.imgBlocks[0][0].setImage(color)
        self.imgBlocks[0][1].setImage(depth)

    def getCalibrationMode(self):
        return self.ui.checkBox.checkState() != 0

    def listClicked(self, qModelIndex):
        self.selectDevice = qModelIndex.row()
        self.setScrollBar()

    def setCamPosData(self, poscamera):
        if(self.camPosData == poscamera):
            return
        self.camPosData = poscamera

    def setCamRotData(self, rotcamera):
        if(self.camRotData == rotcamera):
            return
        self.camRotData = rotcamera

    def setList(self, deviceDictKeys):
        qList = list(deviceDictKeys)
        if(self.listData == qList):
            return
        self.listData = qList
        # 例項化列表模型，新增資料
        slm = QStringListModel()

        # 設定模型列表檢視，載入資料列表
        slm.setStringList(qList)

        # 設定列表檢視的模型
        self.ui.listView.setModel(slm)
        self.ui.listView.setEditTriggers(
            QtWidgets.QAbstractItemView.NoEditTriggers)

        # 單擊觸發自定義的槽函式
        self.ui.listView.clicked.connect(self.listClicked)

    def setScrollBar(self):
        maximum = self.ui.camPos_X.maximum()
        maxDis = 5

        pos = self.camPosData[self.selectDevice]
        pos[0] = pos[0]*maximum/maxDis
        pos[1] = pos[1]*maximum/maxDis
        pos[2] = pos[2]*maximum/maxDis

        self.ui.camPos_X.setValue(pos[0])
        self.ui.camPos_Y.setValue(pos[1])
        self.ui.camPos_Z.setValue(pos[2])

        self.ui.camPosLabel_X.setText(str(pos[0]))
        self.ui.camPosLabel_Y.setText(str(pos[1]))
        self.ui.camPosLabel_Z.setText(str(pos[2]))

        rot = self.camRotData[self.selectDevice]
        self.ui.camRot_X.setValue(rot[0])
        self.ui.camRot_Y.setValue(rot[1])
        self.ui.camRot_Z.setValue(rot[2])

        self.ui.camRotLabel_X.setText(str(rot[0]))
        self.ui.camRotLabel_Y.setText(str(rot[1]))
        self.ui.camRotLabel_Z.setText(str(rot[2]))

    def getUIPos(self):
        maximum = self.ui.camPos_X.maximum()
        maxDis = 5
        pos = [0, 0, 0]
        pos[0] = self.ui.camPos_X.value()/maximum*maxDis
        pos[1] = self.ui.camPos_Y.value()/maximum*maxDis
        pos[2] = self.ui.camPos_Z.value()/maximum*maxDis
        if(pos != self.camPosData[self.selectDevice]):
            self.ui.camPosLabel_X.setText(str(pos[0]))
            self.ui.camPosLabel_Y.setText(str(pos[1]))
            self.ui.camPosLabel_Z.setText(str(pos[2]))
        return pos

    def getUIRot(self):
        rot = [0, 0, 0]
        rot[0] = self.ui.camRot_X.value()
        rot[1] = self.ui.camRot_Y.value()
        rot[2] = self.ui.camRot_Z.value()
        if(rot != self.camRotData[self.selectDevice]):
            self.ui.camRotLabel_X.setText(str(rot[0]))
            self.ui.camRotLabel_Y.setText(str(rot[1]))
            self.ui.camRotLabel_Z.setText(str(rot[2]))
        return rot

    def log(self, msg):
        self.ui.statusbar.showMessage(msg)

    def radioButtonChecked(self, index):

        def click():

            try:
                if index == Socket.SERVER:
                    port = int(self.ui.lineEdit_2.text())
                    ip, port = self.onServerButtonClick(port)
                    self.ui.lineEdit.setText(ip)
                    self.ui.lineEdit_2.setText(port)
                elif index == Socket.CLIENT:
                    ip = self.ui.lineEdit.text()
                    port = int(self.ui.lineEdit_2.text())
                    self.onClientButtonClick(ip, port)
                elif index == Socket.LOCAL:
                    self.onLocalButtonClick()
            except:
                pass
                # input error

        return click


class DevicesControls():
    def __init__(self, hardware):
        self.device = hardware

        self.imgTexture = []
        self.uniform = None
        self.pointCloudGeo = None

        self.time = 0
        self.color_image = None
        self.depth_colormap = None
        self.depthValues = None
        self.camPos = []
        self.camRot = []

    def getInfo(self):
        return self.device.serial_num

    def start(self):
        self.device.start()

    def genPointClouds(self):
        h = self.device.depthH
        w = self.device.depthW
        intr = self.device.depthIntr

        texColor = Texture(np.ones((h, w, 3)))
        texDepth = Texture(np.ones((h, w, 3)))
        self.imgTexture = [texColor, texDepth]
        self.camPos = [0, 0, 0]
        self.camRot = [0, 0, 0]

        # add scene
        self.uniform = Uniform()
        self.uniform.addTexture('texColor', texColor)
        self.uniform.addTexture('texDepth', texDepth)
        self.uniform.addFloat('fx', intr.fx)
        self.uniform.addFloat('fy', intr.fy)
        self.uniform.addFloat('ppx', intr.ppx)
        self.uniform.addFloat('ppy', intr.ppy)
        self.uniform.addFloat('w', w)
        self.uniform.addFloat('h', h)
        self.uniform.addvec3('bboxPos', [1, 1, 1])
        self.uniform.addvec3('bboxNeg', [-1, -1, -1])
        self.uniform.addMat4('extrinct', np.array([
            [1.0, 0.0, 0.0, 0.0],
            [0.0, 1.0, 0.0, 0.0],
            [0.0, 0.0, 1.0, 0.0],
            [0.0, 0.0, 0.0, 1.0]
        ]))

        mat = ShaderMaterial(myShader.vertex_shader,
                             myShader.fragment_shader,
                             self.uniform)

        self.pointCloudGeo = DepthArrGeometry(np.ones(w*h))

        return Mesh(mat, self.pointCloudGeo)

    def updateFrames(self, visualize):
        color_image, depth_colormap, depthValues = self.device.getFrames(
            visualize)

        if(visualize == True):
            self.color_image = color_image
            self.depth_colormap = depth_colormap
            self.depthValues = depthValues

            # update opengl texture
            self.imgTexture[0].update(color_image)
            self.imgTexture[1].update(depth_colormap)

            # print(pointcloud)
            self.pointCloudGeo.update(depthValues)

        return color_image, depth_colormap

    def setData(self, data):
        self.time = time.time()-data.time
        self.device.setData(data)

    def getCamPos(self):
        return self.camPos

    def getData(self):
        data = RealsenseData()

        if(self.device != None):

            _, _, _ = self.device.getFrames()
            data = self.device.getData()

        return data

    def getCamRot(self):
        return self.camRot

    def ArucoCalibration(self, nothing1, nothing2):
        corner1, middle, corner2, middle2, num = ArucoInstance.findMarkers(
            self.color_image)

        def reset():
            self.uniform.setValue('extrinct', np.array([
                [1.0, 0.0, 0.0, 0.0],
                [0.0, 1.0, 0.0, 0.0],
                [0.0, 0.0, 1.0, 0.0],
                [0.0, 0.0, 0.0, 1.0]
            ]))
            # print("calibration error")

        if(num > 0):
            markerPoint1 = self.device.pixel2point(corner1)
            markerPointMiddle = self.device.pixel2point(middle)
            markerPoint2 = self.device.pixel2point(corner2)
            markerPointMiddle2 = self.device.pixel2point(middle2)

            centerPoint = (markerPoint1+markerPointMiddle +
                           markerPoint2+markerPointMiddle2)/4

            edge1 = markerPoint1-markerPointMiddle
            edge2 = markerPoint2-markerPointMiddle

            x = edge1 / np.linalg.norm(edge1)
            z = edge2 / np.linalg.norm(edge2)
            y = np.array([
                x[1]*z[2]-x[2]*z[1],
                x[2]*z[0]-x[0]*z[2],
                x[0]*z[1]-x[1]*z[0],
            ])

            coordMarker = np.array([
                [x[0], -y[0], z[0], centerPoint[0]],
                [x[1], -y[1], z[1], centerPoint[1]],
                [x[2], -y[2], z[2], centerPoint[2]],
                [0, 0, 0, 1.0]
            ])

            try:
                inverCoordMarker = np.linalg.inv(coordMarker)
                self.uniform.setValue('extrinct', inverCoordMarker)
            except:
                reset()
        else:
            reset()

    def calibration(self, pos, rot):

        self.camPos = pos
        self.camRot = rot

        rotation = Rotation.from_euler('xyz', rot, degrees=True)

        mat = rotation.as_matrix()
        self.uniform.setValue('extrinct', np.array([
            [mat[0][0], mat[0][1], mat[0][2], pos[0]],
            [mat[1][0], mat[1][1], mat[1][2], pos[1]],
            [mat[2][0], mat[2][1], mat[2][2], pos[2]],
            [0, 0, 0, 1]
        ]))

    def updateBoundary(self, pos, neg):
        if(self.uniform):
            self.uniform.setValue('bboxPos', pos)
            self.uniform.setValue('bboxNeg', neg)


class App():
    def __init__(self):
        self.initDevices()

        self.socket = None

        self.initQtwindow()

        self.pos, self.neg = [1, 1, 1], [-1, -1, -1]

    def stopSocket(self):
        if(self.socket != None):
            self.socket.stop()
            self.socket = None

    def startServer(self, port):
        self.stopSocket()
        self.socket = Server(port)
        return self.socket.ip, self.socket.port

    def startClient(self, ip, port):
        self.stopSocket()
        self.socket = Client(ip, port)

    def initSocketBtns(self):
        self.uiControls.onServerButtonClick = self.startServer
        self.uiControls.onClientButtonClick = self.startClient
        self.uiControls.onLocalButtonClick = self.stopSocket

    def initDevices(self):
        # setUp realsense
        if(args.device > 0):
            connected_devices = GetAllRealsenses(args.device-1)
        elif(args.device == 0):
            connected_devices = GetAllRealsenses()
        else:
            connected_devices = []
        self.devicesControls = {}

        # Start streaming from cameras
        for device in connected_devices:
            controls = DevicesControls(device)
            self.devicesControls[device.serial_num] = controls
            controls.start()

    def initQtwindow(self):
        # init Qt window
        app = QtWidgets.QApplication(sys.argv)
        MainWindow = QtWidgets.QMainWindow()
        ui = Ui_MainWindow()

        self.uiControls = UIControls(ui, MainWindow)
        ui.pushButton.clicked.connect(self.save)

        self.scene = QtGLScene(self.uiControls.getCanvas())
        self.scene.customRender.append(self.customPaint)

        MainWindow.show()
        MainWindow.destroyed.connect(self.programEnd)

        self.initSocketBtns()

        # window create init opengl
        pointclouds = []
        for key in self.devicesControls:
            device = self.devicesControls[key]
            pointclouds.append(device.genPointClouds())

        # error occur if create after shader compile? !!
        for pointcloud in pointclouds:
            self.scene.add(pointcloud)

        timer = QTimer(MainWindow)
        timer.timeout.connect(self.mainloop)
        timer.start(1)

        app.exec_()

    def programEnd(self):

        for key in self.devicesControls:
            device = self.devicesControls[key]
            device.device.stop()

        self.stopSocket()

    def monitorScrollBar(self):

        pos, neg = self.uiControls.getboundary()

        for key in self.devicesControls:
            device = self.devicesControls[key]
            device.updateBoundary(pos, neg)

        return pos, neg

    def customPaint(self):
        Glhelper.drawXYZaxis()
        pos, neg = self.monitorScrollBar()
        Glhelper.drawBbox(pos, neg)
        self.pos, self.neg = pos, neg

    def onClientDataRecv(self, dataBytes):
        try:
            data = RealsenseData().fromBytes(dataBytes)
            print('network delay : ', time.time()-data.time)
            if(data.serial_num not in self.devicesControls):
                device = Device(data.serial_num, False)
                controls = DevicesControls(device)
                self.devicesControls[device.serial_num] = controls

                self.devicesControls[device.serial_num].setData(data)

                self.scene.add(controls.genPointClouds())
            else:
                self.devicesControls[data.serial_num].setData(data)
        except:
            # packgae decode error
            pass

    def sendData2Socket(self, data):
        self.socket.send(data)

    def mainloop(self):

        if(self.socket != None):
            if(self.socket.type == Socket.SERVER):
                latestBytes = self.socket.getLatestBytes()
                for dataBytes in latestBytes:
                    self.onClientDataRecv(dataBytes)
            elif(self.socket.type == Socket.CLIENT):
                for key in self.devicesControls:
                    device = self.devicesControls[key]
                    self.sendData2Socket(device.getData())

        self.scene.startDraw()

        saveComputePower = not (
            self.socket != None and self.socket.type == Socket.CLIENT)

        maps = []
        allcamPos = []
        allcamRot = []

        for key in self.devicesControls:
            device = self.devicesControls[key]
            color_image, depth_colormap = device.updateFrames(saveComputePower)
            maps.append([color_image, depth_colormap])

            allcamPos.append(device.getCamPos())
            allcamRot.append(device.getCamRot())

        if(self.uiControls.getCalibrationMode()):
            device = self.devicesControls[list(self.devicesControls)[
                self.uiControls.selectDevice]]
            pos = self.uiControls.getUIPos()
            rot = self.uiControls.getUIRot()
            device.ArucoCalibration(pos, rot)

        if(len(self.devicesControls.keys()) > 0 and saveComputePower):
            self.uiControls.setImage(maps)
            listInfo = []
            for key in self.devicesControls:
                device = self.devicesControls[key]
                listInfo.append(device.getInfo())
            self.uiControls.setList(listInfo)
            self.uiControls.setCamPosData(allcamPos)
            self.uiControls.setCamRotData(allcamRot)

        self.scene.endDraw()
        self.uiControls.log("Find {0} realsense(s).".format(
            len(self.devicesControls)))

    def save(self):

        saveRootPath = os.path.join(args.output, './')
        if not os.path.exists(saveRootPath):
            os.makedirs(saveRootPath)

        # save image and info
        for keys in self.devicesControls:

            deviceControls = self.devicesControls[keys]
            device = deviceControls.device
            device.saveFrames(saveRootPath)

            mat4 = deviceControls.uniform.getValue('extrinct')

            config = device.getConfig()
            config['calibrateMat'] = mat4
            config['positiveBoundaryCorner'] = self.pos
            config['negativeBoundaryCorner'] = self.neg

            json.write(config,  os.path.join(
                saveRootPath, config['time']+"."+config['realsense_serial_num']+'.config.json'))


app = App()
