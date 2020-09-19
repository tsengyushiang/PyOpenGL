import pyrealsense2 as rs
import numpy as np
import cv2
import os
from dotmap import DotMap
from .NetworkData import RealsenseData


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

        self.colorW = 1920
        self.colorH = 1080
        self.acutlaDepthW = 1280
        self.actualDepthH = 720

        # after alignment depth map will have the same resolution as color
        self.downSampleFactor = 5
        self.depthW = int(self.colorW/self.downSampleFactor)
        self.depthH = int(self.colorH/self.downSampleFactor)

        self.pipeline = None
        if(isPhysic):
            self.configPipeLine()

    def configPipeLine(self):
        self.pipeline = rs.pipeline()
        self.config = rs.config()
        self.config.enable_device(self.serial_num)
        self.config.enable_stream(
            rs.stream.depth, self.acutlaDepthW, self.actualDepthH, rs.format.z16, 30)
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
            self.actualDepthIntr = profile.as_video_stream_profile().get_intrinsics()

            profileColor = cfg.get_stream(rs.stream.color)
            self.colorIntr = profileColor.as_video_stream_profile().get_intrinsics()

            self.depthIntr = DotMap()
            self.depthIntr.fx = self.colorIntr.fx/self.downSampleFactor
            self.depthIntr.fy = self.colorIntr.fy/self.downSampleFactor
            self.depthIntr.ppx = self.colorIntr.ppx/self.downSampleFactor
            self.depthIntr.ppy = self.colorIntr.ppy/self.downSampleFactor

            depth_sensor = cfg.get_device().first_depth_sensor()
            self.depth_scale = depth_sensor.get_depth_scale()

    def stop(self):
        if(self.pipeline):
            self.pipeline.stop()

    def pixel2point(self, coord):

        depth = (self.depth_image_downSampled *
                 self.depth_scale)[int(coord[1]/self.downSampleFactor)
                                   ][int(coord[0]/self.downSampleFactor)]

        pointX = (coord[0]/self.downSampleFactor -
                  self.depthIntr.ppx)/self.depthIntr.fx*depth
        pointY = (self.depthH-coord[1]/self.downSampleFactor -
                  self.depthIntr.ppy)/self.depthIntr.fy*depth

        return np.array([pointX, pointY, depth])

    def getData(self):
        data = RealsenseData()
        data.serial_num = self.serial_num
        data.depth_scale = self.depth_scale
        data.w = self.depthW
        data.h = self.depthH
        data.fx = self.depthIntr.fx
        data.fy = self.depthIntr.fy
        data.ppx = self.depthIntr.ppx
        data.ppy = self.depthIntr.ppy
        data.color = self.color_image
        data.depth = self.depth_image_downSampled
        return data

    def setData(self, data):
        self.depth_scale = data.depth_scale
        self.depthIntr = DotMap()
        self.depthIntr.ppx = data.ppx
        self.depthIntr.ppy = data.ppy
        self.depthIntr.fx = data.fx
        self.depthIntr.fy = data.fy
        self.colorIntr = DotMap()
        self.colorIntr.ppx = data.ppx
        self.colorIntr.ppy = data.ppy
        self.colorIntr.fx = data.fx
        self.colorIntr.fy = data.fy
        self.depthW = data.w
        self.depthH = data.h
        self.color_image = data.color
        self.depth_colormap = data.depthMap
        self.depth_image = data.depth
        self.depth_image_downSampled = data.depth
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

    def getFrames(self, visualize=False):

        if(self.pipeline):
            frames = self.pipeline.wait_for_frames()
            aligned_frames = self.align.process(frames)

            depth_frame = aligned_frames.get_depth_frame()
            color_frame = aligned_frames.get_color_frame()

            if not depth_frame or not color_frame:
                print(self.serial_num, 'retrieve frame error !!')
                return None, None, None

            self.color_image = np.asanyarray(color_frame.get_data())
            self.depth_image = np.asanyarray(depth_frame.get_data())
            self.depth_image_downSampled = self.depth_image[::self.downSampleFactor,
                                                            ::self.downSampleFactor]
            self.depthValues = self.depth_image_downSampled*self.depth_scale

            if(visualize == False):
                return self.color_image, self.color_image, self.depthValues.flatten()

            colorizer = rs.colorizer()
            self.depth_colormap = np.asanyarray(
                colorizer.colorize(depth_frame).get_data())

        return self.color_image, self.depth_colormap, self.depthValues.flatten()

    def getPointsColors(self):

        downSample = self.color_image[::self.downSampleFactor,
                                      ::self.downSampleFactor]

        return downSample.flatten().reshape(self.depthW*self.depthH, 3)

    def getPoints(self):
        # calc point cloud
        h = (np.arange(self.depthH, dtype=float)
             [::-1]-self.depthIntr.ppy)/self.depthIntr.fy
        w = (np.arange(self.depthW, dtype=float) -
             self.depthIntr.ppx)/self.depthIntr.fx
        points = np.empty((self.depthH, self.depthW, 3), dtype=float)
        points[:, :, 1] = h[:, None]*self.depthValues
        points[:, :, 0] = w*self.depthValues
        points[:, :, 2] = self.depthValues
        return np.reshape(points, (self.depthH*self.depthW, 3))

    def saveFrames(self, path):
        self.getFrames()

        cv2.imwrite(
            os.path.join(path, self.serial_num+'.depth16'+'.png'), self.depth_image.astype(np.uint16))
        cv2.imwrite(
            os.path.join(path, self.serial_num+'.color'+'.png'), self.color_image)
