import sys
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from opengl.Camera import *

class GlutScene:
    def __init__(self, width=640, height=480, title=b'PyOpenGL'):
        # Initialization
        glutInit(sys.argv)
        glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
        glutInitWindowSize(width, height)
        self.window = glutCreateWindow(title)

        # render function
        glutDisplayFunc(self.draw)

        # mouse event
        glutMouseFunc(self.mouseClick)
        glutMotionFunc(self.mouseMove)

        # render setting
        self.InitGL(width, height)
        self.meshes = []

    def add(self, mesh):
        mesh.init()
        self.meshes.append(mesh)

    def draw(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.camera.update()

        for mesh in self.meshes:
            mesh.draw()

        glutSwapBuffers()

        # refresh as fast as possible
        glutPostRedisplay()

    def InitGL(self, width, height):
        glClearColor(0.0, 0.0, 0.0, 0.0)
        glClearDepth(1.0)
        glDepthFunc(GL_LESS)
        glEnable(GL_DEPTH_TEST)
        glShadeModel(GL_SMOOTH)
        self.camera = Camera(width, height)

    def mouseClick(self, button, state, x, y):
        self.camera.handlGLUTMouseClick(button, state, x, y)

    def mouseMove(self, x, y):
        self.camera.handleGLUTMouseMove(x, y)

    def MainLoop(self):
        glutMainLoop()
