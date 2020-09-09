import cv2
import sys
from qtLayout.realsenseClient import *
from PyQt5.QtCore import *

from Realsense.device import *

from Network.socket.Client import Client
from Network.data.RealsenseData import RealsenseData


class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.DisplayRole:
            # See below for the nested-list data structure.
            # .row() indexes into the outer list,
            # .column() indexes into the sub-list
            return self._data[index.row()][index.column()]

    def rowCount(self, index):
        # The length of the outer list.
        return len(self._data)

    def columnCount(self, index):
        # The following takes the first sub-list, and returns
        # the length (only works if all rows are an equal length)
        return len(self._data[0])


class RealsenseDevice():
    def __init__(self, hardwareApis=None):
        self.hardwareApis = hardwareApis
        if(hardwareApis != None):
            self.hardwareApis.start()
        self.socket = Client("192.168.50.105", 8002)

    def sendNetWorkData(self):
        data = RealsenseData()

        if(self.hardwareApis != None):

            _, _, _ = self.hardwareApis.getFrames()

            data.serial_num = self.hardwareApis.serial_num
            data.depth_scale = self.hardwareApis.depth_scale
            data.w = self.hardwareApis.w
            data.h = self.hardwareApis.h
            data.fx = self.hardwareApis.intr.fx
            data.fy = self.hardwareApis.intr.fy
            data.ppx = self.hardwareApis.intr.ppx
            data.ppy = self.hardwareApis.intr.ppy
            data.color = self.hardwareApis.color_image
            data.depth = self.hardwareApis.depth_image

        self.socket.send(data)

    def log(self):
        return self.socket.log

    def stop(self):
        self.socket.stop()


# init Qt window
app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)

table = ui.tableView
data = [
    [4, 9, 2],
    [1, 0, 0],
    [3, 5, 0],
    [3, 3, 2],
    [7, 8, 9],
]

model = TableModel(data)
ui.tableView.setModel(model)

# setUp realsense
connected_devices = GetAllRealsenses()
RealsenseDevices = []

# Start streaming from cameras
for device in connected_devices:
    RealsenseDevices.append(RealsenseDevice(device))

ui.statusbar.showMessage(
    "Find {0} realsense(s).".format(len(RealsenseDevices)))


def mainloop():
    for device in RealsenseDevices:
        device.sendNetWorkData()


timer = QTimer(MainWindow)
timer.timeout.connect(mainloop)
timer.start(5)

MainWindow.show()
app.exec_()


def programEnd():
    for device in RealsenseDevices:
        device.stop()


MainWindow.destroyed.connect(programEnd)
