import cv2
import numpy as np


class RealsenseData():
    def __init__(self):
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
        _, colorencode = cv2.imencode('.png', self.color)
        _, depthencode = cv2.imencode('.png', self.depth)

        return [self.w,
                self.h,
                self.fx,
                self.fy,
                self.ppx,
                self.ppy,
                colorencode,
                depthencode]

    def fromArr(self, arr):

        decColor = cv2.imdecode(arr[6], 1)
        decDepth = cv2.imdecode(arr[7], 1)

        self.w = arr[0]
        self.h = arr[1]
        self.fx = arr[2]
        self.fy = arr[3]
        self.ppx = arr[4]
        self.ppy = arr[5]
        self.color = decColor
        self.depth = decDepth
        return self
