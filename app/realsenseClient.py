import cv2
import sys
from qtLayout.realsenseClient import *
from PyQt5.QtCore import *

from Network.socket.Client import Client
from Network.data.RealsenseData import RealsenseData

# init Qt window
app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)

socket = Client("192.168.50.105", 8002)
ui.statusbar.showMessage(socket.log)
capture = cv2.VideoCapture(0)


def mainloop():
    ret, frame = capture.read()

    data = RealsenseData()
    data.color = frame
    socket.send(data)


timer = QTimer(MainWindow)
timer.timeout.connect(mainloop)
timer.start(1)

MainWindow.show()
app.exec_()


def programEnd():
    socket.stop()


MainWindow.destroyed.connect(programEnd)
