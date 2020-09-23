from OpenGL.arrays import vbo
from OpenGL.GL import *
from openmesh import *
import numpy as np


class PointGeometry:
    def __init__(self, points, colors):
        self.vertices = np.array(points, dtype='f')
        self.colors = np.array(colors, dtype='f')

    def init(self):
        # store binding info in vao once, no need to bind in runtime.
        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)

        self.vertexPositions = vbo.VBO(self.vertices)
        self.vertexColors = vbo.VBO(self.colors)

        self.vertexPositions.bind()
        glEnableClientState(GL_VERTEX_ARRAY)
        glVertexPointerf(self.vertexPositions)
        self.vertexPositions.unbind()

        self.vertexColors.bind()
        glEnableClientState(GL_COLOR_ARRAY)
        glColorPointerf(self.vertexColors)
        self.vertexColors.unbind()

    def draw(self):
        glPointSize(1)
        glBindVertexArray(self.vao)
        glDrawArrays(GL_POINTS, 0, len(self.vertices))

    def update(self, points, colors):
        self.vertices = np.array(points, dtype='f')
        self.colors = np.array(colors, dtype='f')
        glDeleteVertexArrays(1, [self.vao])
        self.init()
