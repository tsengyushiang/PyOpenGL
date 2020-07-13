import sys
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from OpenGL.arrays import vbo
from OpenGL.GL import shaders
import shaders.basic as myShader

import numpy as np

class OpenGLWindow:
    def __init__(self, width=640, height=480, title=b'PyOpenGL'):
        # Initialization
        glutInit(sys.argv)
        glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
        glutInitWindowSize(width, height)
        self.window = glutCreateWindow(title)
        glutDisplayFunc(self.Draw)
        self.InitGL(width, height)

    def Draw(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        glTranslatef(0.0, 0.0, -1.0)
        glColor3f(0.0, 1.0, 0.0)
        glRasterPos2f(0.0, 0.0)
        self.DrawText('PyOpenGL')

        # use shader and bind vbo
        shaders.glUseProgram(self.shader)
        self.vbo.bind()
        glEnableClientState(GL_VERTEX_ARRAY)

        #draw setting
        glVertexPointerf(self.vbo)
        glDrawArrays(GL_TRIANGLES, 0, 9)

        self.vbo.unbind()
        glDisableClientState(GL_VERTEX_ARRAY)
        shaders.glUseProgram(0)

        glutSwapBuffers()

    def DrawText(self, string):
        for c in string:
            glutBitmapCharacter(GLUT_BITMAP_8_BY_13, ord(c))

    def InitGL(self, width, height):
        glClearColor(0.0, 0.0, 0.0, 0.0)
        glClearDepth(1.0)
        glDepthFunc(GL_LESS)
        glEnable(GL_DEPTH_TEST)
        glShadeModel(GL_SMOOTH)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45.0, float(width)/float(height), 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)

        # init shader
        VERTEX_SHADER = shaders.compileShader(
            myShader.vertex_shader, GL_VERTEX_SHADER)
        FRAGMENT_SHADER = shaders.compileShader(
            myShader.fragment_shader, GL_FRAGMENT_SHADER)
        self.shader = shaders.compileProgram(VERTEX_SHADER, FRAGMENT_SHADER)

        # create vertices
        self.vbo = vbo.VBO(
            np.array([
                [0, 1, 0],
                [-1, -1, 0],
                [1, -1, 0],
                [2, -1, 0],
                [4, -1, 0],
                [4, 1, 0],
                [2, -1, 0],
                [4, 1, 0],
                [2, 1, 0],
            ], 'f')
        )

    def MainLoop(self):
        glutMainLoop()


window = OpenGLWindow()
window.MainLoop()
