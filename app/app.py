import sys
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

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
    def MainLoop(self):
        glutMainLoop()

window = OpenGLWindow()
window.MainLoop()