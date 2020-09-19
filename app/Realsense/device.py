import pyrealsense2 as rs
import numpy as np
import cv2
import os
from dotmap import DotMap


def GetAllRealsenses(index=None):
    connected_devices = []
    realsense_ctx = rs.context()
    # get all devices serial numbers
    for i in range(len(realsense_ctx.devices)):

        if(index != None and i != index):
            continue

        detected_camera = realsense_ctx.devices[i].get_info(
            rs.camera_info.serial_number)
        connected_devices.append(Device(detected_camera))

    return connected_devices


class Device:
    def __init__(self, serial_num, isPhysic=True):
        print('create Realsense', serial_num)
        self.serial_num = serial_num

        self.depthW = 640
        self.depthH = 480
        self.colorW = 640
        self.colorH = 480

        self.pipeline = None
        if(isPhysic):
            self.configPipeLine()

    def configPipeLine(self):
        self.pipeline = rs.pipeline()
        self.config = rs.config()
        self.config.enable_device(self.serial_num)
        self.config.enable_stream(
            rs.stream.depth, self.depthW, self.depthH, rs.format.z16, 30)
        self.config.enable_stream(
            rs.stream.color, self.colorW, self.colorH, rs.format.bgr8, 30)

        # align color and depth
        align_to = rs.stream.color
        self.align = rs.align(align_to)

    def start(self):
        if(self.pipeline):
            cfg = self.pipeline.start(self.config)

            # get camera instri
            profile = cfg.get_stream(rs.stream.depth)
            self.intr = profile.as_video_stream_profile().get_intrinsics()
            # print(self.intr.ppx, self.intr.ppy, self.intr.fx, self.intr.fy)
            # print(self.intr.coeffs)
            profileColor = cfg.get_stream(rs.stream.color)
            self.colorIntr = profileColor.as_video_stream_profile().get_intrinsics()

            depth_sensor = cfg.get_device().first_depth_sensor()
            self.depth_scale = depth_sensor.get_depth_scale()
            # print("Depth Scale is: ", depth_scale)

    def stop(self):
        if(self.pipeline):
            self.pipeline.stop()

    def pixel2point(self, coord):

        depth = self.depthValues[int(coord[1])][int(coord[0])]

        pointX = (coord[0]-self.colorIntr.ppx)/self.colorIntr.fx*depth
        pointY = (self.colorH-coord[1] -
                  self.colorIntr.ppy)/self.colorIntr.fy*depth

        return np.array([pointX, pointY, depth])

    def setData(self, data):
        self.depth_scale = data.depth_scale
        self.intr = DotMap()
        self.intr.ppx = data.ppx
        self.intr.ppy = data.ppy
        self.intr.fx = data.fx
        self.intr.fy = data.fy
        self.colorIntr = DotMap()
        self.colorIntr.ppx = data.ppx
        self.colorIntr.ppy = data.ppy
        self.colorIntr.fx = data.fx
        self.colorIntr.fy = data.fy
        self.depthW = data.w
        self.depthH = data.h
        self.color_image = data.color
        self.depth_colormap = data.depthMap
        self.depthValues = data.depth*data.depth_scale

    def getFrames8bits(self, maxMeter):
        if(self.pipeline):
            frames = self.pipeline.wait_for_frames()
            frames = self.align.process(frames)
            depth_frame = frames.get_depth_frame()
            color_frame = frames.get_color_frame()

            if not depth_frame or not color_frame:
                print(self.serial_num, 'retrieve frame error !!')
                return None, None, None

            self.color_image = np.asanyarray(color_frame.get_data())

            self.depth_image = np.asanyarray(
                depth_frame.get_data())*self.depth_scale

            depth_image8bit = cv2.convertScaleAbs(
                self.depth_image, alpha=255/maxMeter)

            self.depth_colormap = cv2.applyColorMap(
                depth_image8bit, cv2.COLORMAP_JET)

            self.depthValues = depth_image8bit/(255/maxMeter)

        return self.color_image, self.depth_colormap, self.depthValues.flatten()

    def getFrames(self):

        if(self.pipeline):
            frames = self.pipeline.wait_for_frames()
            aligned_frames = self.align.process(frames)

            # aligned_depth_frame is a 640x480 depth image
            depth_frame = aligned_frames.get_depth_frame()
            color_frame = aligned_frames.get_color_frame()

            #depth_frame = frames.get_depth_frame()
            #color_frame = frames.get_color_frame()

            if not depth_frame or not color_frame:
                print(self.serial_num, 'retrieve frame error !!')
                return None, None, None

            self.color_image = np.asanyarray(color_frame.get_data())
            colorizer = rs.colorizer()
            self.depth_colormap = np.asanyarray(
                colorizer.colorize(depth_frame).get_data())

            self.depth_image = np.asanyarray(depth_frame.get_data())
            self.depthValues = self.depth_image*self.depth_scale

        return self.color_image, self.depth_colormap, self.depthValues.flatten()

    def getPoints(self):
        # calc point cloud
        h = (np.arange(self.colorH, dtype=float)
             [::-1]-self.colorIntr.ppy)/self.colorIntr.fy
        w = (np.arange(self.colorW, dtype=float) -
             self.colorIntr.ppx)/self.colorIntr.fx
        points = np.empty((self.colorH, self.colorW, 3), dtype=float)
        points[:, :, 1] = h[:, None]*self.depthValues
        points[:, :, 0] = w*self.depthValues
        points[:, :, 2] = self.depthValues
        return points

    def saveFrames(self, path):
        self.getFrames()

        cv2.imwrite(
            os.path.join(path, self.serial_num+'.depth16'+'.png'), self.depth_image.astype(np.uint16))
        cv2.imwrite(
            os.path.join(path, self.serial_num+'.color'+'.png'), self.color_image)
        cv2.imwrite(
            os.path.join(path, self.serial_num+'.depth'+'.png'), self.depth_colormap)
