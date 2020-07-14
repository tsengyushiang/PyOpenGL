import sys
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from OpenGL.GL import shaders
import shaders.basic as myShader

from Geometry import *
from Algorithm.coordinate import Spherical2Cartesian

from args import build_argparser
args = build_argparser().parse_args()


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

        coord = Spherical2Cartesian((3, self.v, 1))
        gluLookAt(coord[0], coord[2], coord[1],  0.0,0.0,0.0,  0.0,1.0,0.0)

        # use shader and bind vbo
        shaders.glUseProgram(self.shader)
        self.mesh.Draw()
        shaders.glUseProgram(0)

        
        self.v += 0.5
        '''
        if self.v > 360:
            self.v = 0
            self.h += 5
        '''
        glutSwapBuffers()

        # refresh as fast as possible
        glutPostRedisplay()

    def InitGL(self, width, height):
        glClearColor(0.0, 0.0, 0.0, 0.0)
        glClearDepth(1.0)
        glDepthFunc(GL_LESS)
        glEnable(GL_DEPTH_TEST)
        glShadeModel(GL_SMOOTH)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(60.0, float(width)/float(height), 0.01, 100.0)
        glMatrixMode(GL_MODELVIEW)

        # init shader
        VERTEX_SHADER = shaders.compileShader(
            myShader.vertex_shader, GL_VERTEX_SHADER)
        FRAGMENT_SHADER = shaders.compileShader(
            myShader.fragment_shader, GL_FRAGMENT_SHADER)
        self.shader = shaders.compileProgram(VERTEX_SHADER, FRAGMENT_SHADER)

        # read obj file
        self.mesh = Geometry(args.model)

        self.v = 0
        self.h = 0

    def MainLoop(self):
        glutMainLoop()


window = OpenGLWindow()
window.MainLoop()
