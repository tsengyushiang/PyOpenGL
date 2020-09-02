from OpenGL.arrays import vbo
from OpenGL.GL import *
from openmesh import *
import numpy as np


class Geometry:
    def __init__(self, filename):

        self.mesh = self.unpackObjFile(filename)

        self.vertices = np.array(
            self.mesh.points(), dtype='f')
        self.indices = np.array(
            self.mesh.face_vertex_indices(), dtype=np.int32)

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

    def Save(self, filename):
        write_mesh(filename, self.mesh)

    def unpackObjFile(self, filename):

        mesh = TriMesh()

        # Using readlines()
        objfile = open(filename, 'r')
        Lines = objfile.readlines()

        self.vertices_colors = []
        # 初始的第一個為padding,因obj檔中的face_index從1開始
        vertex_handles = [[0, 0, 0]]
        # Strips the newline character
        for line in Lines:
            contents = line.split()

            if contents[0] == 'v':

                vertex_handle = mesh.add_vertex(
                    [float(contents[1]), float(contents[2]), float(contents[3])])
                vertex_handles.append(vertex_handle)
                self.vertices_colors.append(
                    [float(contents[4]), float(contents[5]), float(contents[6])])

            elif contents[0] == 'f':
                mesh.add_face(vertex_handles[int(contents[1])], vertex_handles[int(
                    contents[2])], vertex_handles[int(contents[3])])

        return mesh
