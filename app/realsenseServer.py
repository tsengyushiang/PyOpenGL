import cv2
import sys
from qtLayout.realsenseClient import *
from PyQt5.QtCore import *

from Network.socket.Server import Server
from Network.data.RealsenseData import RealsenseData

from opencv.QtcvImage import QtcvImage

# init Qt window
app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)

socket = Server(8002)
ui.statusbar.showMessage(socket.log)

colorBox = QtcvImage(ui.label)
depthBox = QtcvImage(ui.label_2)


def mainloop():
    data = socket.getInputs()

    if(data != None):
        dataFromated = RealsenseData().fromArr(data)
        colorBox.setImage(dataFromated.color)
        depthBox.setImage(dataFromated.depth)
    pass


timer = QTimer(MainWindow)
timer.timeout.connect(mainloop)
timer.start(1)

MainWindow.show()
app.exec_()


def programEnd():
    socket.stop()


MainWindow.destroyed.connect(programEnd)
