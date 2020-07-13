from OpenGL.arrays import vbo
from OpenGL.GL import *

from openmesh import *

import numpy as np


class MyTriMesh:
    def __init__(self, filename):
        self.mesh = read_trimesh(filename)

        self.vertices = np.array(
            self.mesh.points(), dtype='f')
        self.indices = np.array(
            self.mesh.face_vertex_indices(), dtype=np.int32)

        self.vertexPositions = vbo.VBO(self.vertices)
        self.indexPositions = vbo.VBO(
            self.indices, target=GL_ELEMENT_ARRAY_BUFFER)

    def Draw(self):
        self.indexPositions.bind()
        self.vertexPositions.bind()

        glEnableClientState(GL_VERTEX_ARRAY)

        # draw setting
        glVertexPointerf(self.vertexPositions)
        glDrawElements(GL_TRIANGLES, len(self.indices)*3, GL_UNSIGNED_INT,
                       None)  # This line does work too!

        self.vertexPositions.unbind()
        self.indexPositions.unbind()

        glDisableClientState(GL_VERTEX_ARRAY)

    def Save(self, filename):
        write_mesh(filename, self.mesh)
