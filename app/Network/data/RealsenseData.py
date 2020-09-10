import cv2
import numpy as np
from _pickle import dumps, loads
import struct


class RealsenseData():
    def __init__(self):
        self.serial_num = 0
        self.depth_scale = 0
        self.w = 0
        self.h = 0
        self.fx = 0
        self.fy = 0
        self.ppx = 0
        self.ppy = 0
        self.color = np.array([[0]])
        self.depth = np.array([[0]])
        pass

    def parseBigDepth2RGB(self, depthMap):
        rgb = np.empty((depthMap.shape[0], depthMap.shape[1], 3))
        rgb[:, :, 0] = depthMap % 256
        rgb[:, :, 1] = depthMap // 256
        rgb[:, :, 2] = 0
        return rgb

    def rgb2BigDepth(self, rgb):
        depthMap = np.empty((rgb.shape[0], rgb.shape[1]))
        depthMap = rgb[:, :, 0]+rgb[:, :, 1]*256
        return depthMap

    def toBytes(self):
        _, colorencode = cv2.imencode(
            '.jpg', self.color, [int(cv2.IMWRITE_JPEG_QUALITY), 30])

        bigNum2RGB = self.parseBigDepth2RGB(self.depth)
        _, depthencode = cv2.imencode('.png', bigNum2RGB)

        bytestotal = dumps([self.serial_num,
                            self.depth_scale,
                            self.w,
                            self.h,
                            self.fx,
                            self.fy,
                            self.ppx,
                            self.ppy,
                            colorencode,
                            depthencode])
        return bytestotal

    def fromBytes(self, Bytes):
        arr = loads(Bytes)
        decColor = cv2.imdecode(arr[8], cv2.IMREAD_COLOR)
        decDepth3 = cv2.imdecode(arr[9], cv2.IMREAD_COLOR)
        decDepth = self.rgb2BigDepth(decDepth3)

        self.serial_num = arr[0]
        self.depth_scale = arr[1]
        self.w = arr[2]
        self.h = arr[3]
        self.fx = arr[4]
        self.fy = arr[5]
        self.ppx = arr[6]
        self.ppy = arr[7]
        self.color = decColor
        self.depthMap = decDepth3
        self.depth = decDepth
        return self