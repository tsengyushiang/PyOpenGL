import cv2
import sys
from qtLayout.realsenseClient import *
from PyQt5.QtCore import *

from Realsense.device import *

from Network.socket.Client import Client
from Network.data.RealsenseData import RealsenseData

# init Qt window
app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)

socket = Client("192.168.50.105", 8002)
capture = cv2.VideoCapture(0)

# setUp realsense
connected_devices = GetAllRealsenses()

# Start streaming from cameras
for device in connected_devices:
    device.start()


def mainloop():
    ui.statusbar.showMessage(socket.log)

    color_image, depth_colormap, depthValues = device.getFrames()

    data = RealsenseData()
    data.color = color_image
    data.depth = depth_colormap
    socket.send(data)


timer = QTimer(MainWindow)
timer.timeout.connect(mainloop)
timer.start(1)

MainWindow.show()
app.exec_()


def programEnd():
    socket.stop()


MainWindow.destroyed.connect(programEnd)
