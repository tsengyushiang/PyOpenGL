# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'app/qtLayout/realsenseApp.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(666, 427)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.openGLWidget = QtWidgets.QOpenGLWidget(self.centralwidget)
        self.openGLWidget.setObjectName("openGLWidget")
        self.verticalLayout_3.addWidget(self.openGLWidget)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.verticalLayout_6.addWidget(self.label)
        self.posX = QtWidgets.QScrollBar(self.centralwidget)
        self.posX.setMinimum(-30)
        self.posX.setMaximum(30)
        self.posX.setSingleStep(1)
        self.posX.setPageStep(1)
        self.posX.setProperty("value", 10)
        self.posX.setOrientation(QtCore.Qt.Horizontal)
        self.posX.setObjectName("posX")
        self.verticalLayout_6.addWidget(self.posX)
        self.negX = QtWidgets.QScrollBar(self.centralwidget)
        self.negX.setMinimum(-30)
        self.negX.setMaximum(30)
        self.negX.setProperty("value", -10)
        self.negX.setOrientation(QtCore.Qt.Horizontal)
        self.negX.setObjectName("negX")
        self.verticalLayout_6.addWidget(self.negX)
        self.horizontalLayout_6.addLayout(self.verticalLayout_6)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_5.addWidget(self.label_2)
        self.negY = QtWidgets.QScrollBar(self.centralwidget)
        self.negY.setMinimum(-100)
        self.negY.setMaximum(-1)
        self.negY.setProperty("value", -10)
        self.negY.setOrientation(QtCore.Qt.Horizontal)
        self.negY.setObjectName("negY")
        self.verticalLayout_5.addWidget(self.negY)
        self.posY = QtWidgets.QScrollBar(self.centralwidget)
        self.posY.setMinimum(-30)
        self.posY.setMaximum(30)
        self.posY.setProperty("value", 10)
        self.posY.setOrientation(QtCore.Qt.Horizontal)
        self.posY.setObjectName("posY")
        self.verticalLayout_5.addWidget(self.posY)
        self.horizontalLayout_6.addLayout(self.verticalLayout_5)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_4.addWidget(self.label_3)
        self.posZ = QtWidgets.QScrollBar(self.centralwidget)
        self.posZ.setMinimum(-30)
        self.posZ.setMaximum(30)
        self.posZ.setProperty("value", 10)
        self.posZ.setOrientation(QtCore.Qt.Horizontal)
        self.posZ.setObjectName("posZ")
        self.verticalLayout_4.addWidget(self.posZ)
        self.negZ = QtWidgets.QScrollBar(self.centralwidget)
        self.negZ.setMinimum(-30)
        self.negZ.setMaximum(-1)
        self.negZ.setProperty("value", -10)
        self.negZ.setOrientation(QtCore.Qt.Horizontal)
        self.negZ.setObjectName("negZ")
        self.verticalLayout_4.addWidget(self.negZ)
        self.horizontalLayout_6.addLayout(self.verticalLayout_4)
        self.verticalLayout_3.addLayout(self.horizontalLayout_6)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout_3.addWidget(self.pushButton)
        self.verticalLayout_3.setStretch(0, 9)
        self.verticalLayout_3.setStretch(1, 1)
        self.verticalLayout_3.setStretch(2, 1)
        self.horizontalLayout.addLayout(self.verticalLayout_3)
        self.horizontalLayout.setStretch(0, 5)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.checkBox = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox.setObjectName("checkBox")
        self.gridLayout.addWidget(self.checkBox, 2, 0, 1, 1)
        self.verticalWidget = QtWidgets.QWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.verticalWidget.sizePolicy().hasHeightForWidth())
        self.verticalWidget.setSizePolicy(sizePolicy)
        self.verticalWidget.setObjectName("verticalWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalWidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_6 = QtWidgets.QLabel(self.verticalWidget)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_3.addWidget(self.label_6)
        self.lineEdit = QtWidgets.QLineEdit(self.verticalWidget)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout_3.addWidget(self.lineEdit)
        self.label_4 = QtWidgets.QLabel(self.verticalWidget)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_3.addWidget(self.label_4)
        self.lineEdit_2 = QtWidgets.QLineEdit(self.verticalWidget)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.horizontalLayout_3.addWidget(self.lineEdit_2)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.radioButton_2 = QtWidgets.QRadioButton(self.verticalWidget)
        self.radioButton_2.setObjectName("radioButton_2")
        self.horizontalLayout_4.addWidget(self.radioButton_2)
        self.radioButton = QtWidgets.QRadioButton(self.verticalWidget)
        self.radioButton.setObjectName("radioButton")
        self.horizontalLayout_4.addWidget(self.radioButton)
        self.radioButton_3 = QtWidgets.QRadioButton(self.verticalWidget)
        self.radioButton_3.setChecked(True)
        self.radioButton_3.setObjectName("radioButton_3")
        self.horizontalLayout_4.addWidget(self.radioButton_3)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)
        self.color = QtWidgets.QLabel(self.verticalWidget)
        self.color.setObjectName("color")
        self.verticalLayout_2.addWidget(self.color)
        self.depth = QtWidgets.QLabel(self.verticalWidget)
        self.depth.setObjectName("depth")
        self.verticalLayout_2.addWidget(self.depth)
        self.verticalLayout_2.setStretch(0, 5)
        self.verticalLayout_2.setStretch(1, 5)
        self.verticalLayout_2.setStretch(2, 20)
        self.verticalLayout_2.setStretch(3, 20)
        self.horizontalLayout_2.addLayout(self.verticalLayout_2)
        self.verticalLayout_7 = QtWidgets.QVBoxLayout()
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.listView = QtWidgets.QListView(self.verticalWidget)
        self.listView.setObjectName("listView")
        self.verticalLayout_7.addWidget(self.listView)
        self.horizontalLayout_2.addLayout(self.verticalLayout_7)
        self.horizontalLayout_2.setStretch(0, 5)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_8 = QtWidgets.QLabel(self.verticalWidget)
        self.label_8.setObjectName("label_8")
        self.verticalLayout_10.addWidget(self.label_8)
        self.camPosLabel_X = QtWidgets.QLineEdit(self.verticalWidget)
        self.camPosLabel_X.setObjectName("camPosLabel_X")
        self.verticalLayout_10.addWidget(self.camPosLabel_X)
        self.camPos_X = QtWidgets.QScrollBar(self.verticalWidget)
        self.camPos_X.setMinimum(-100)
        self.camPos_X.setMaximum(100)
        self.camPos_X.setProperty("value", 0)
        self.camPos_X.setOrientation(QtCore.Qt.Horizontal)
        self.camPos_X.setObjectName("camPos_X")
        self.verticalLayout_10.addWidget(self.camPos_X)
        self.horizontalLayout_5.addLayout(self.verticalLayout_10)
        self.verticalLayout_9 = QtWidgets.QVBoxLayout()
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.label_7 = QtWidgets.QLabel(self.verticalWidget)
        self.label_7.setObjectName("label_7")
        self.verticalLayout_9.addWidget(self.label_7)
        self.camPosLabel_Y = QtWidgets.QLineEdit(self.verticalWidget)
        self.camPosLabel_Y.setObjectName("camPosLabel_Y")
        self.verticalLayout_9.addWidget(self.camPosLabel_Y)
        self.camPos_Y = QtWidgets.QScrollBar(self.verticalWidget)
        self.camPos_Y.setMinimum(-100)
        self.camPos_Y.setMaximum(100)
        self.camPos_Y.setProperty("value", 0)
        self.camPos_Y.setOrientation(QtCore.Qt.Horizontal)
        self.camPos_Y.setObjectName("camPos_Y")
        self.verticalLayout_9.addWidget(self.camPos_Y)
        self.horizontalLayout_5.addLayout(self.verticalLayout_9)
        self.verticalLayout_8 = QtWidgets.QVBoxLayout()
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.label_5 = QtWidgets.QLabel(self.verticalWidget)
        self.label_5.setObjectName("label_5")
        self.verticalLayout_8.addWidget(self.label_5)
        self.camPosLabel_Z = QtWidgets.QLineEdit(self.verticalWidget)
        self.camPosLabel_Z.setObjectName("camPosLabel_Z")
        self.verticalLayout_8.addWidget(self.camPosLabel_Z)
        self.camPos_Z = QtWidgets.QScrollBar(self.verticalWidget)
        self.camPos_Z.setMinimum(-100)
        self.camPos_Z.setMaximum(100)
        self.camPos_Z.setProperty("value", 0)
        self.camPos_Z.setOrientation(QtCore.Qt.Horizontal)
        self.camPos_Z.setObjectName("camPos_Z")
        self.verticalLayout_8.addWidget(self.camPos_Z)
        self.horizontalLayout_5.addLayout(self.verticalLayout_8)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.verticalLayout_13 = QtWidgets.QVBoxLayout()
        self.verticalLayout_13.setObjectName("verticalLayout_13")
        self.label_11 = QtWidgets.QLabel(self.verticalWidget)
        self.label_11.setObjectName("label_11")
        self.verticalLayout_13.addWidget(self.label_11)
        self.camRotLabel_X = QtWidgets.QLineEdit(self.verticalWidget)
        self.camRotLabel_X.setObjectName("camRotLabel_X")
        self.verticalLayout_13.addWidget(self.camRotLabel_X)
        self.camRot_X = QtWidgets.QScrollBar(self.verticalWidget)
        self.camRot_X.setMaximum(360)
        self.camRot_X.setOrientation(QtCore.Qt.Horizontal)
        self.camRot_X.setObjectName("camRot_X")
        self.verticalLayout_13.addWidget(self.camRot_X)
        self.horizontalLayout_7.addLayout(self.verticalLayout_13)
        self.verticalLayout_12 = QtWidgets.QVBoxLayout()
        self.verticalLayout_12.setObjectName("verticalLayout_12")
        self.label_10 = QtWidgets.QLabel(self.verticalWidget)
        self.label_10.setObjectName("label_10")
        self.verticalLayout_12.addWidget(self.label_10)
        self.camRotLabel_Y = QtWidgets.QLineEdit(self.verticalWidget)
        self.camRotLabel_Y.setObjectName("camRotLabel_Y")
        self.verticalLayout_12.addWidget(self.camRotLabel_Y)
        self.camRot_Y = QtWidgets.QScrollBar(self.verticalWidget)
        self.camRot_Y.setMaximum(360)
        self.camRot_Y.setOrientation(QtCore.Qt.Horizontal)
        self.camRot_Y.setObjectName("camRot_Y")
        self.verticalLayout_12.addWidget(self.camRot_Y)
        self.horizontalLayout_7.addLayout(self.verticalLayout_12)
        self.verticalLayout_11 = QtWidgets.QVBoxLayout()
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.label_9 = QtWidgets.QLabel(self.verticalWidget)
        self.label_9.setObjectName("label_9")
        self.verticalLayout_11.addWidget(self.label_9)
        self.camRotLabel_Z = QtWidgets.QLineEdit(self.verticalWidget)
        self.camRotLabel_Z.setObjectName("camRotLabel_Z")
        self.verticalLayout_11.addWidget(self.camRotLabel_Z)
        self.camRot_Z = QtWidgets.QScrollBar(self.verticalWidget)
        self.camRot_Z.setMaximum(360)
        self.camRot_Z.setOrientation(QtCore.Qt.Horizontal)
        self.camRot_Z.setObjectName("camRot_Z")
        self.verticalLayout_11.addWidget(self.camRot_Z)
        self.horizontalLayout_7.addLayout(self.verticalLayout_11)
        self.verticalLayout.addLayout(self.horizontalLayout_7)
        self.gridLayout.addWidget(self.verticalWidget, 0, 1, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 666, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Realsense volcapture"))
        self.label.setText(_translate("MainWindow", "bbox X axis"))
        self.label_2.setText(_translate("MainWindow", "bbox Y axis"))
        self.label_3.setText(_translate("MainWindow", "bbox Z axis"))
        self.pushButton.setText(_translate("MainWindow", "capture pointClouds,colorMap,depthMap,transMat"))
        self.checkBox.setText(_translate("MainWindow", "calibration mode"))
        self.label_6.setText(_translate("MainWindow", "IP:"))
        self.label_4.setText(_translate("MainWindow", "Port:"))
        self.radioButton_2.setText(_translate("MainWindow", "server+local"))
        self.radioButton.setText(_translate("MainWindow", "client+local"))
        self.radioButton_3.setText(_translate("MainWindow", "local"))
        self.color.setText(_translate("MainWindow", "TextLabel"))
        self.depth.setText(_translate("MainWindow", "TextLabel"))
        self.label_8.setText(_translate("MainWindow", "Position X"))
        self.label_7.setText(_translate("MainWindow", "Position Y"))
        self.label_5.setText(_translate("MainWindow", "Position Z"))
        self.label_11.setText(_translate("MainWindow", "Rotation X"))
        self.label_10.setText(_translate("MainWindow", "Rotation Y"))
        self.label_9.setText(_translate("MainWindow", "Rotation Z"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
