from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from Algorithm.coordinate import Spherical2Cartesian

import math


class Camera:
    def __init__(self, width, height):
        self.setViewport(width, height)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        gluPerspective(60.0, float(width)/float(height), 0.01, 100.0)

        self.minAzimuthangle = 0
        self.maxAzimuthangle = 180
        self.zoomSensitivity = 0.1

        self.polarAngle = 0
        self.azimuthangle = 1
        self.radius = 3

        self.center = (0.0, 0.0, 0.0)

        self.mouseCoord = None

    def setViewport(self, width, height):
        glViewport(0, 0, width, height)

    def update(self):

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        coord = Spherical2Cartesian(
            (self.radius, self.polarAngle, self.azimuthangle))
        gluLookAt(coord[0], coord[2], coord[1],  self.center[0],
                  self.center[1], self.center[2],  0.0, 1.0, 0.0)

    def handlGLUTMouseClick(self, button, x, y):
        if(button == GLUT_LEFT_BUTTON):
            if(self.mouseCoord == None):
                self.mouseCoord = (x, y)
            else:
                self.mouseCoord = None

        if(button == 3):
            self.zoom(-1)

        if(button == 4):
            self.zoom(1)

    def handleGLUTMouseMove(self, x, y):
        #print(x, y, self.mouseCoord)
        if(self.mouseCoord != None):

            deltaX = x-self.mouseCoord[0]
            deltaY = self.mouseCoord[1]-y

            self.dragCamera(deltaX, deltaY)

            self.mouseCoord = (x, y)

    def zoom(self, deltaZoom):
        self.radius += self.zoomSensitivity * math.copysign(1, deltaZoom)

    def dragCamera(self, deltaX, deltaY):
        self.polarAngle += deltaX

        if(self.azimuthangle+deltaY > self.minAzimuthangle and self.azimuthangle+deltaY < self.maxAzimuthangle):
            self.azimuthangle += deltaY
