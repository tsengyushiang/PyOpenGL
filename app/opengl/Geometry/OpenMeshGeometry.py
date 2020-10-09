from OpenGL.arrays import vbo
from OpenGL.GL import *
from openmesh import *
import numpy as np


class OpenMeshGeometry:
    def __init__(self, filename):

        self.mesh = read_trimesh(filename, vertex_normal=True)
        #self.mesh = read_trimesh(filename)
        #         
        self.vertices = np.array(
            self.mesh.points(), dtype='f')
        self.indices = np.array(
            self.mesh.face_vertex_indices(), dtype=np.int32)
        self.vertices_colors = np.array(
            self.mesh.vertex_normals(), dtype='f')

    def getNormalizeMat(self):

        # 找points boundingbox對角線長度,做scale
        upperbound = np.amax(self.vertices, 0)
        lowerbound = np.amin(self.vertices, 0)
        dist = np.linalg.norm(upperbound - lowerbound)
        scale = 1/dist

        # 找找points重心,做offset
        length = self.vertices.shape[0]
        center_x = np.sum(self.vertices[:, 0])/length
        center_y = np.sum(self.vertices[:, 1])/length
        center_z = np.sum(self.vertices[:, 2])/length

        return [
            [scale, 0.0, 0.0, -center_x*scale],
            [0.0, scale, 0.0, -center_y*scale],
            [0.0, 0.0, scale, -center_z*scale],
            [0.0, 0.0, 0.0, 1.0]
        ]

    def init(self):

        # store binding info in vao once, no need to bind in runtime.
        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)

        self.vertexPositions = vbo.VBO(self.vertices)
        self.indexPositions = vbo.VBO(
            self.indices, target=GL_ELEMENT_ARRAY_BUFFER)
        self.verticesColors = vbo.VBO(
            np.array(self.vertices_colors, dtype='f'))

        self.vertexPositions.bind()
        glEnableClientState(GL_VERTEX_ARRAY)
        glVertexPointerf(self.vertexPositions)
        self.vertexPositions.unbind()

        self.verticesColors.bind()
        glEnableClientState(GL_COLOR_ARRAY)
        glColorPointerf(self.verticesColors)
        self.verticesColors.unbind()

        self.indexPositions.bind()

    def draw(self):

        glBindVertexArray(self.vao)
        glDrawElements(GL_TRIANGLES, len(self.indices)*3, GL_UNSIGNED_INT,
                None)  # This line does work too!

