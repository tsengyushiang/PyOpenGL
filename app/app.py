import sys
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from OpenGL.GL import shaders
import shaders.basic as myShader

from MyTriMesh import *

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
        glTranslatef(0.0, 0.0, -2.0)

        # use shader and bind vbo
        shaders.glUseProgram(self.shader)
        self.mesh.Draw()
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
        gluPerspective(60.0, float(width)/float(height), 0.01, 100.0)
        glMatrixMode(GL_MODELVIEW)

        # init shader
        VERTEX_SHADER = shaders.compileShader(
            myShader.vertex_shader, GL_VERTEX_SHADER)
        FRAGMENT_SHADER = shaders.compileShader(
            myShader.fragment_shader, GL_FRAGMENT_SHADER)
        self.shader = shaders.compileProgram(VERTEX_SHADER, FRAGMENT_SHADER)

        # read obj file
        self.mesh = MyTriMesh(args.model)

    def MainLoop(self):
        glutMainLoop()


window = OpenGLWindow()
window.MainLoop()
