import cv2
import numpy as np


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

    def toArr(self):
        _, colorencode = cv2.imencode('.jpg', self.color)
        #_, depthencode = cv2.imencode('.jpg', self.depth)

        return [self.serial_num,
                self.depth_scale,
                self.w,
                self.h,
                self.fx,
                self.fy,
                self.ppx,
                self.ppy,
                colorencode,
                self.depth]

    def fromArr(self, arr):
        decColor = cv2.imdecode(arr[8], 1)
        #decDepth = cv2.imdecode(arr[9], 1)

        self.serial_num = arr[0]
        self.depth_scale = arr[1]
        self.w = arr[2]
        self.h = arr[3]
        self.fx = arr[4]
        self.fy = arr[5]
        self.ppx = arr[6]
        self.ppy = arr[7]
        self.color = decColor
        self.depth = arr[9]
        return self
