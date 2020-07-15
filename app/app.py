import sys
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from OpenGL.GL import shaders
import shaders.basic as myShader

from Geometry import *
from Camera import *

from args import build_argparser
args = build_argparser().parse_args()

class OpenGLWindow:
    def __init__(self, width=640, height=480, title=b'PyOpenGL'):
        # Initialization
        glutInit(sys.argv)
        glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
        glutInitWindowSize(width, height)
        self.window = glutCreateWindow(title)
        
        # render function
        glutDisplayFunc(self.Draw)

        # mouse event
        glutMouseFunc(self.mouseClick)
        glutMotionFunc(self.mouseMove)

        # render setting
        self.InitGL(width, height)

    def Draw(self):

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.camera.update()

        # use shader and bind vbo
        shaders.glUseProgram(self.shader)
        self.mesh.Draw()
        shaders.glUseProgram(0)

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

        # init shader
        VERTEX_SHADER = shaders.compileShader(
            myShader.vertex_shader, GL_VERTEX_SHADER)
        FRAGMENT_SHADER = shaders.compileShader(
            myShader.fragment_shader, GL_FRAGMENT_SHADER)
        self.shader = shaders.compileProgram(VERTEX_SHADER, FRAGMENT_SHADER)

        # read obj file
        self.mesh = Geometry(args.model)

    def mouseClick(self, button, state, x, y):
        self.camera.handlMouseClick(button, state, x, y)

    def mouseMove(self, x, y):
        self.camera.handleMouseMove(x, y)

    def MainLoop(self):
        glutMainLoop()


window = OpenGLWindow()
window.MainLoop()
