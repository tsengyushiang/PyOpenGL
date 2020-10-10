from OpenGL.arrays import vbo
from OpenGL.GL import *
from openmesh import *
import numpy as np
import time

# log all member function
def DEBUG_SHOWATTRIBUTE(obj):
    for att in dir(obj):
        print (att, getattr(obj,att))

class OpenMeshGeometry:
    def __init__(self, filename):
        self.level = 0
        self.LODvaos = []

        #self.mesh = read_trimesh(filename, vertex_normal=True)
        self.mesh = read_trimesh(filename)
        #DEBUG_SHOWATTRIBUTE(self.mesh)
        self.updateVertexNormals()

    def collapseFirstEdge(self):

        i = 3000
        for eh in self.mesh.edges():
            self.collapseEdge(eh,useMidPoint=True)
            
            i=i-1
            if i<0:
                break
        
        self.mesh.garbage_collection()
        self.init()

    def collapseEdge(self,edgehandle,useMidPoint=True,position=[0,0,0]):

        he0 = self.mesh.halfedge_handle(edgehandle,0)
        vh0 = self.mesh.to_vertex_handle(he0)

        he1 = self.mesh.halfedge_handle(edgehandle,1)
        vh1 = self.mesh.to_vertex_handle(he1)
        
        if useMidPoint:
            midPoint = (self.mesh.point(vh0)+self.mesh.point(vh1))/2

        if self.mesh.is_collapse_ok(he0):
            self.mesh.collapse(he0)
            vh0 = self.mesh.to_vertex_handle(he0)
            self.mesh.update_normal(vh0)

            if useMidPoint:
                self.mesh.set_point(vh0,midPoint)
            else:
                self.mesh.set_point(vh0,position)
       
    def deleteVertices(self):
        readyToDelete = []
        for vh in self.mesh.vertices():
            if vh.idx()%3==0:
                readyToDelete.append(vh)
        for vh in readyToDelete:
            self.mesh.delete_vertex(vh)
        
        self.mesh.garbage_collection()

    def updateVertexNormals(self):
        self.mesh.update_normals()
        '''
        # iteractive update 
        for vh in self.mesh.vertices():
            self.mesh.update_normal(vh)
        '''

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
        vao = glGenVertexArrays(1)
        glBindVertexArray(vao)
        
        vertices = np.array(
            self.mesh.points(), dtype='f')
        indices = np.array(
            self.mesh.face_vertex_indices(), dtype=np.int32)
        vertices_normals = np.array(
            self.mesh.vertex_normals(), dtype='f')
        
        vertexPositions = vbo.VBO(vertices)
        indexPositions = vbo.VBO(
            indices, target=GL_ELEMENT_ARRAY_BUFFER)
        verticesNormals = vbo.VBO(
            np.array(vertices_normals, dtype='f'))

        vertexPositions.bind()
        glEnableClientState(GL_VERTEX_ARRAY)
        glVertexPointerf(vertexPositions)
        vertexPositions.unbind()

        verticesNormals.bind()
        glEnableClientState(GL_COLOR_ARRAY)
        glColorPointerf(verticesNormals)
        verticesNormals.unbind()

        indexPositions.bind()

        glBindVertexArray(0)

        return vao,len(indices)*3

    def init(self):
        vao,faces = self.genMeshVAO()
        self.LODvaos.append((vao,faces))
        self.level = len(self.LODvaos)-1

    def draw(self):

        vao,faces = self.LODvaos[self.level]

        glBindVertexArray(vao)
        glEnable(GL_CULL_FACE)
        glCullFace(GL_FRONT)
        glPolygonMode( GL_FRONT_AND_BACK, GL_LINE )
        glDrawElements(GL_TRIANGLES, faces, GL_UNSIGNED_INT,
                None)  # This line does work too!

    def setLevel(self,zero2one):
        self.level = int((len(self.LODvaos)-1)*zero2one)
        print(len(self.LODvaos)-1,self.level)