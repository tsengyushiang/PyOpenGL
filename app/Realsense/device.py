import pyrealsense2 as rs
import numpy as np
import cv2
import datetime


def GetAllRealsenses():
    connected_devices = []
    realsense_ctx = rs.context()
    # get all devices serial numbers
    for i in range(len(realsense_ctx.devices)):
        detected_camera = realsense_ctx.devices[i].get_info(
            rs.camera_info.serial_number)
        connected_devices.append(Device(detected_camera))

    return connected_devices


class Device:
    def __init__(self, serial_num):
        self.serial_num = serial_num
        self.w = 1280
        self.h = 720
        self.configPipeLine()

    def configPipeLine(self):
        self.pipeline = rs.pipeline()
        self.config = rs.config()
        self.config.enable_device(self.serial_num)
        self.config.enable_stream(
            rs.stream.depth, self.w, self.h, rs.format.z16, 30)
        self.config.enable_stream(
            rs.stream.color, self.w, self.h, rs.format.bgr8, 30)

        align_to = rs.stream.color
        self.align = rs.align(align_to)

    def start(self):
        self.pipeline.start(self.config)

    def stop(self):
        self.pipeline.stop()

    def getFrames(self):

        frames = self.pipeline.wait_for_frames()
        frames = self.align.process(frames)
        depth_frame = frames.get_depth_frame()
        color_frame = frames.get_color_frame()

        if not depth_frame or not color_frame:
            print(self.serial_num, 'retrieve frame error !!')
            return null, null

        self.color_image = np.asanyarray(color_frame.get_data())
        colorizer = rs.colorizer()
        self.depth_colormap = np.asanyarray(
            colorizer.colorize(depth_frame).get_data())

        return self.color_image, self.depth_colormap

    def saveFrames(self, imgPath='img'):
        self.getFrames()

        currentTime = datetime.datetime.now()
        currentTimeStr = currentTime.strftime("%Y%m%d_%H%M%S")

        depthImgpostfix = '.depth.'+self.serial_num+'.'+currentTimeStr+'.png'
        colorImgpostfix = '.color.'+self.serial_num+'.'+currentTimeStr+'.png'

        cv2.imwrite(imgPath+depthImgpostfix, self.color_image)
        cv2.imwrite(imgPath+colorImgpostfix, self.depth_colormap)
