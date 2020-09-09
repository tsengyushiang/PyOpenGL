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
        repeat3 = cv2.cvtColor(depthMap, cv2.COLOR_GRAY2RGB)
        repeat3[:, :, 0] = depthMap >> 16
        repeat3[:, :, 1] = depthMap % (256*256) >> 8
        repeat3[:, :, 2] = depthMap & 256
        print(depthMap)
        return repeat3

    def toBytes(self):
        _, colorencode = cv2.imencode('.png', self.color)

        bigNum2RGB = self.parseBigDepth2RGB(self.depth)
        _, depthencode = cv2.imencode('.png', bigNum2RGB)
        decDepth = cv2.imdecode(depthencode, cv2.IMREAD_COLOR)

        comparison = decDepth == bigNum2RGB
        equal_arrays = comparison.all()
        print(equal_arrays)

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
        decDepth = cv2.imdecode(arr[9], cv2.IMREAD_COLOR)

        self.serial_num = arr[0]
        self.depth_scale = arr[1]
        self.w = arr[2]
        self.h = arr[3]
        self.fx = arr[4]
        self.fy = arr[5]
        self.ppx = arr[6]
        self.ppy = arr[7]
        self.color = decColor
        self.depth = decDepth
        return self
