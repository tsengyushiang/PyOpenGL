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
        self.w = 640
        self.h = 480
        self.configPipeLine()

    def configPipeLine(self):
        self.pipeline = rs.pipeline()
        self.config = rs.config()
        self.config.enable_device(self.serial_num)
        self.config.enable_stream(
            rs.stream.depth, self.w, self.h, rs.format.z16, 30)
        self.config.enable_stream(
            rs.stream.color, self.w, self.h, rs.format.bgr8, 30)

        # align color and depth
        align_to = rs.stream.color
        self.align = rs.align(align_to)

    def start(self):
        cfg = self.pipeline.start(self.config)

        # get camera instri
        profile = cfg.get_stream(rs.stream.depth)
        self.intr = profile.as_video_stream_profile().get_intrinsics()
        print(self.intr.ppx, self.intr.ppy, self.intr.fx, self.intr.fy)
        # print(self.intr.coeffs)

        depth_sensor = cfg.get_device().first_depth_sensor()
        self.depth_scale = depth_sensor.get_depth_scale()
        # print("Depth Scale is: ", depth_scale)

    def stop(self):
        self.pipeline.stop()

    def pixel2point(self, coord):

        x = int(coord[0])
        y = int(coord[1])
        return self.points[y][x]

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

        # calc point cloud
        # ref : https://github.com/IntelRealSense/librealsense/blob/6ded42e4f1709acc60bdd42667028f221b9e6094/include/librealsense2/rsutil.h#L46
        self.depthValues = np.asanyarray(
            depth_frame.get_data())*self.depth_scale
        h = (np.arange(self.h, dtype=float)[::-1]-self.intr.ppy)/self.intr.fy
        w = (np.arange(self.w, dtype=float)-self.intr.ppx)/self.intr.fx
        self.points = np.empty((self.h, self.w, 3), dtype=float)
        self.points[:, :, 1] = h[:, None]*self.depthValues
        self.points[:, :, 0] = w*self.depthValues
        self.points[:, :, 2] = self.depthValues

        return self.color_image, self.depth_colormap, self.points.reshape(self.h*self.w, 3)

    def saveFrames(self, imgPath='img'):
        self.getFrames()

        currentTime = datetime.datetime.now()
        currentTimeStr = currentTime.strftime("%Y%m%d_%H%M%S")

        depthImgpostfix = '.depth.'+self.serial_num+'.'+currentTimeStr+'.png'
        colorImgpostfix = '.color.'+self.serial_num+'.'+currentTimeStr+'.png'

        cv2.imwrite(imgPath+depthImgpostfix, self.color_image)
        cv2.imwrite(imgPath+colorImgpostfix, self.depth_colormap)
