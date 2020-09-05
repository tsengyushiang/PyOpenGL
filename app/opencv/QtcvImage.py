import cv2
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class QtcvImage():
    def __init__(self, qtLabel):
        self.qtLabel = qtLabel
        self.qtLabel.setVisible(False)

    def setImage(self, cvmat):

        w = self.qtLabel.size().width()
        h = self.qtLabel.size().height()
        resizedMat = cv2.resize(cvmat, (w, h), interpolation=cv2.INTER_CUBIC)
        height, width, channel = resizedMat.shape
        bytesPerline = 3 * width

        qImg = QImage(resizedMat.data, w, h, bytesPerline,
                      QImage.Format_RGB888).rgbSwapped()

        self.qtLabel.setPixmap(QPixmap.fromImage(qImg))
        self.qtLabel.setVisible(True)