from OpenGL.arrays import vbo
from OpenGL.GL import *
from openmesh import *
import numpy as np
import time
import math 
from scipy import sparse
from scipy.sparse.linalg import spsolve
import sys
import bisect 
import numpy as np

def DEBUG_SHOWATTRIBUTE(obj):
    for att in dir(obj):
        print (att, getattr(obj,att))

class BufferGeometry:
    def __init__(self):       

        self.mesh=None
        
    def isNotVaild(self):
        return self.mesh is None or self.vao is None

    def readObj(self,filename):

        # read uv        
        self.mesh = read_trimesh(filename, vertex_tex_coord=True)
        self.mesh.update_normals()
        self.init()
        DEBUG_SHOWATTRIBUTE(self.mesh)
        return True

    def getNormalizeMat(self):
        vertices = np.array(
            self.mesh.points(), dtype='f')
        # 找points boundingbox對角線長度,做scale
        upperbound = np.amax(vertices, 0)
        lowerbound = np.amin(vertices, 0)
        dist = np.linalg.norm(upperbound - lowerbound)
        scale = 1/dist

        # 找找points重心,做offset
        length = vertices.shape[0]
        center_x = np.sum(vertices[:, 0])/length
        center_y = np.sum(vertices[:, 1])/length
        center_z = np.sum(vertices[:, 2])/length

        return [
            [scale, 0.0, 0.0, -center_x*scale],
            [0.0, scale, 0.0, -center_y*scale],
            [0.0, 0.0, scale, -center_z*scale],
            [0.0, 0.0, 0.0, 1.0]
        ]       

    def genMeshVAO(self):

        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)
        
        vertices = np.array(
            self.mesh.points(), dtype='f')
        self.indices = np.array(
            self.mesh.face_vertex_indices(), dtype=np.int32)
        vertices_normals = np.array(
            self.mesh.vertex_normals(), dtype='f')
        vertices_uvs = np.array(
            self.mesh.vertex_texcoords2D(), dtype='f')

        vertexPositions = vbo.VBO(vertices)
        indexPositions = vbo.VBO(
            self.indices, target=GL_ELEMENT_ARRAY_BUFFER)
        verticesNormals = vbo.VBO(
            np.array(vertices_normals, dtype='f'))
        verticesUvs = vbo.VBO(
            np.array(vertices_uvs, dtype='f'))

        vertexPositions.bind()
        glEnableClientState(GL_VERTEX_ARRAY)
        glVertexPointerf(vertexPositions)
        vertexPositions.unbind()

        verticesNormals.bind()
        glEnableClientState(GL_COLOR_ARRAY)
        glColorPointerf(verticesNormals)
        verticesNormals.unbind()

        verticesUvs.bind()
        glClientActiveTexture(GL_TEXTURE0)
        glEnableClientState(GL_TEXTURE_COORD_ARRAY)
        glTexCoordPointerf(verticesUvs)
        verticesUvs.unbind()

        indexPositions.bind()

        glBindVertexArray(0)
            
    def init(self):
        if self.mesh is not None:        
            self.genMeshVAO()

    def draw(self):
        if self.isNotVaild():
            return

        glBindVertexArray(self.vao)        
        glDrawElements(GL_TRIANGLES, len(self.indices)*3, GL_UNSIGNED_INT,None)