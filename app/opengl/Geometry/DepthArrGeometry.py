from OpenGL.arrays import vbo
from OpenGL.GL import *
from openmesh import *
import numpy as np
from array import array

# ref : https://www.itdaan.com/tw/6251861a4618499e4b55cbbcc8393266
# attribute must in code or location will not be found


class DepthArrGeometry:
    def __init__(self, depths):

        self.shader = None
        self.depths = np.array(depths, dtype='f')

    def init(self):
        # store binding info in vao once, no need to bind in runtime.
        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)

        self.depthsVBO = vbo.VBO(self.depths)
        self.depthsVBO.bind()

        self.location = glGetAttribLocation(
            self.shader, 'depthValue',
        )

        if(self.location != -1):
            glEnableVertexAttribArray(self.location)

            glVertexAttribPointer(
                self.location,
                1, GL_FLOAT, False, 0, self.depthsVBO
            )
            glDisableVertexAttribArray(self.location)

        self.depthsVBO.unbind()

    def draw(self):
        glPointSize(1)
        glBindVertexArray(self.vao)

        if(self.location != -1):
            glEnableVertexAttribArray(self.location)

        glDrawArrays(GL_POINTS, 0, len(self.depths))

        if(self.location != -1):
            glDisableVertexAttribArray(self.location)

    def update(self, depths):
        self.depths = np.array(depths, dtype='f')
        glDeleteVertexArrays(1, [self.vao])
        self.init()
