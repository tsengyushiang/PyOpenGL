from OpenGL.arrays import vbo
from OpenGL.GL import *
from openmesh import *
import numpy as np
import time
import math 
from scipy import sparse
from scipy.sparse.linalg import spsolve

class SparseMat:
    def __init__(self):
        self.row=[]
        self.col=[]
        self.data=[]
    
    def insert(self,row,col,data):
        self.row.append(row)
        self.col.append(col)
        self.data.append(data)

    def mat(self,shape):
        return sparse.csr_matrix((self.data, (self.row, self.col)), shape)
        


def DEBUG_MESH():
    mesh = TriMesh()
    vh0 = mesh.add_vertex([0, 1, 0])
    vh1 = mesh.add_vertex([1, 0.2, 0])
    vh2 = mesh.add_vertex([1.5, 1, 0])
    vh3 = mesh.add_vertex([0,-1, 0])
    vh4 = mesh.add_vertex([2,-1, 0])
    #convex
    vh5 = mesh.add_vertex([3,0.5, 0])    
    # not convex
    #vh5 = mesh.add_vertex([1.3,0, 0])

    vh6  = mesh.add_vertex([1, -0.2, 0])

    fh4 = mesh.add_face(vh1, vh6, vh5)
    fh0 = mesh.add_face(vh0, vh1, vh2)
    fh2 = mesh.add_face(vh0, vh3, vh1)
    fh3 = mesh.add_face(vh2, vh1, vh5)

    fh5 = mesh.add_face(vh1, vh3, vh6)
    fh6 = mesh.add_face(vh6, vh3, vh4)
    fh7 = mesh.add_face(vh6, vh4, vh5)
    return mesh

# log all member function
def DEBUG_SHOWATTRIBUTE(obj):
    for att in dir(obj):
        print (att, getattr(obj,att))

def calcAngle(vector_1,vector_2):
    unit_vector_1 = vector_1 / np.linalg.norm(vector_1)
    unit_vector_2 = vector_2 / np.linalg.norm(vector_2)
    dot_product = np.dot(unit_vector_1, unit_vector_2)
    return  math.degrees(np.arccos(dot_product))

def area(x1, y1, z1, x2, y2, z2): 
    area = math.sqrt((y1 * z2 - y2 * z1) ** 2 
           + (x1 * z2 - x2 * z1) ** 2 + 
           (x1 * y2 - x2 * y1) ** 2) 
    area = area / 2
    return area 

class OpenMeshGeometry:
    def __init__(self, filename):
        self.level = 0
        self.LODvaos = []

        #self.mesh = read_trimesh(filename, vertex_normal=True)
        self.mesh = read_trimesh(filename)

        #self.mesh = DEBUG_MESH()
        #DEBUG_SHOWATTRIBUTE(self.mesh)

        self.updateVertexNormals()

        #contractionEnergy
        self.WL = 1e-3*self.getAverageFaceArea()
        self.sL = 2.0

    def isConvexMesh(self,mesh):

        boundaryhalfEdge = None
        # get first boundary vertex       
        for eh in mesh.halfedges():
            isBoundary = mesh.is_boundary(eh)
            if isBoundary :
                boundaryhalfEdge = eh
                break
        
        # go through every boundary halfedge
        orderedPoints = []
        startEdgeId = boundaryhalfEdge.idx()
        while(True):
            vh = mesh.from_vertex_handle(boundaryhalfEdge)
            p1 = mesh.point(vh)

            # out halfedge to get neighbor vertex for calc angle
            neighborVecs = []
            for heh in mesh.voh(vh):
                vh = mesh.to_vertex_handle(heh)
                p2 = mesh.point(vh)
                neighborVecs.append(p2-p1)
            
            innerAngle = 0
            for i in range(1,len(neighborVecs)):
                v1 = neighborVecs[i-1]
                v2 = neighborVecs[i]
                innerAngle += calcAngle(v1,v2)

            # inner angel > 180 mean is not convex polygon
            if innerAngle>180:
                return False

            # check next boundary vertex untill loop end
            boundaryhalfEdge = mesh.next_halfedge_handle(boundaryhalfEdge)
            if boundaryhalfEdge.idx() == startEdgeId:
                break
        
        return True

    def getAverageFaceArea(self):
        mat4 = self.getNormalizeMat()
        areaSum = 0
        count = 0
        for fh in self.mesh.faces():
            tri = []
            for vh in self.mesh.fv(fh):
                tri.append(self.mesh.point(vh))
            
            # calc area
            count = count+1

            a = tri[0]-tri[2]
            b = tri[1]-tri[2]
            areaSum = areaSum + area(a[0],a[1],a[2],b[0],b[1],b[2])
        
        return areaSum/count

    def contraction(self):       
    
        verticesNumber = self.mesh.n_vertices()

        # solve least-sqare ax=b to find optimal x for each vertex
        # Skeleton Extraction ref : http://graphics.csie.ncku.edu.tw/Skeleton/skeleton-paperfinal.pdf
        # Least-squares Meshes ref : https://igl.ethz.ch/projects/Laplacian-mesh-processing/ls-meshes/ls-meshes.pdf
        
        # topolog weight sarse matrix
        weightConstain = SparseMat()   
        targetPoint = SparseMat()

        for vh in self.mesh.vertices():

            oneRingArea = 0
            for fh in self.mesh.vf(vh):
                tri = []
                for vfh in self.mesh.fv(fh):
                    tri.append(self.mesh.point(vfh))                    
                # calc area
                a = tri[0]-tri[2]
                b = tri[1]-tri[2]
                oneRingArea = oneRingArea + area(a[0],a[1],a[2],b[0],b[1],b[2])
            
            origionArea = self.mesh.vertex_property('one-ring-area',vh)
            if origionArea==None:
                self.mesh.set_vertex_property('one-ring-area',vh,oneRingArea)
                origionArea = oneRingArea
            
            WH = self.mesh.vertex_property('WH',vh)
            if WH==None:
                WH = 1.0

            if oneRingArea!=0:
                self.mesh.set_vertex_property('WH',vh, WH * math.sqrt(origionArea/oneRingArea))

            p0 = self.mesh.point(vh)
            sumWeights = 0
            # calc conformal weight cotA+cotB
            oneRingVertexHandles = []
            for vvh in self.mesh.vv(vh):
                oneRingVertexHandles.append((
                    vvh,self.mesh.point(vvh)
                ))

            variant = len(oneRingVertexHandles)
            for index in range(variant):
                _,p1 = oneRingVertexHandles[(index+1)%variant]
                vh0,p = oneRingVertexHandles[index]
                _,p_1 = oneRingVertexHandles[(index-1)%variant]
                angleA = calcAngle(p0-p1,p-p1)
                angleB = calcAngle(p0-p_1,p-p_1)
                cotA = 1/math.tan(math.radians(angleA))
                cotB =1/math.tan(math.radians(angleB))

                # add topology weight
                weightConstain.insert(vh.idx(),vh0.idx(),(cotA + cotB)*self.WL)
                sumWeights = sumWeights + cotA + cotB
            
            #add weight balance
            weightConstain.insert(vh.idx(),vh.idx(),-sumWeights*self.WL)

            # add constrains
            weightConstain.insert(vh.idx()+verticesNumber,vh.idx(),1*WH)
            targetPoint.insert(vh.idx()+verticesNumber,0,p0[0]*WH)
            targetPoint.insert(vh.idx()+verticesNumber,1,p0[1]*WH)
            targetPoint.insert(vh.idx()+verticesNumber,2,p0[2]*WH)
        
        b = targetPoint.mat((2*verticesNumber,3))
        A = weightConstain.mat((2*verticesNumber,verticesNumber))

        #print(A.toarray().shape,b.shape)
        x = spsolve(A.T*A,A.T*b).toarray()

        self.WL = self.WL * self.sL

        # update vertex position
        for vh in self.mesh.vertices():
            self.mesh.set_point(vh,x[vh.idx()])
        return True            
    

    def collapseFirstEdge(self):

        for eh in self.mesh.edges():
            isConvex = self.mesh.edge_property('convex',eh)

            if(isConvex == False):
                continue

            success = self.collapseEdge(eh,useMidPoint=True)    
            
            if success:
                #print(self.mesh.n_edges(),self.mesh.n_vertices())
                self.mesh.garbage_collection()
                return True

        return False

    def is_merge_ok(self,edgehandle):
        # create submesh for convex polygon checking
        he0 = self.mesh.halfedge_handle(edgehandle,0)
        vh0 = self.mesh.to_vertex_handle(he0)
        vh1 = self.mesh.from_vertex_handle(he0)
        
        fhs = []
        for fh in self.mesh.vf(vh0):
            fhs.append(fh)      

        # don't add duplicate face
        for fh in self.mesh.vf(vh1):

            hasVh0 = False
            for vh in self.mesh.fv(fh):
                if(vh.idx()==vh0.idx()):
                    hasVh0 = True
                    break

            if not hasVh0:
                fhs.append(fh)

        vhs = {}
        submesh = TriMesh()
        for fh in fhs:
            fvhs = []            
            for vh in self.mesh.fv(fh):
                id = str(vh.idx())
                if id not in vhs:
                    p = self.mesh.point(vh)
                    vhs[id] = submesh.add_vertex(p)
                fvhs.append(vhs[id])

            submesh.add_face(fvhs)

        isConvexMesh = self.isConvexMesh(submesh)
        return isConvexMesh

    def collapseEdge(self,edgehandle,useMidPoint=True,position=[0,0,0]):

        he0 = self.mesh.halfedge_handle(edgehandle,0)
        vh0 = self.mesh.to_vertex_handle(he0)

        he1 = self.mesh.halfedge_handle(edgehandle,1)
        vh1 = self.mesh.to_vertex_handle(he1)
        
        if useMidPoint:
            midPoint = (self.mesh.point(vh0)+self.mesh.point(vh1))/2

        if self.mesh.is_collapse_ok(he0) and self.is_merge_ok(edgehandle):
            self.mesh.collapse(he0)
            vh0 = self.mesh.to_vertex_handle(he0)
            self.mesh.update_normal(vh0)

            if useMidPoint:
                self.mesh.set_point(vh0,midPoint)
            else:
                self.mesh.set_point(vh0,position)
            
            # recompute affect edges
            for vh in self.mesh.vv(vh0):
                for eh in self.mesh.ve(vh):
                    self.mesh.set_edge_property('convex',eh,None)


            return True

        else:
            self.mesh.set_edge_property('convex',edgehandle,False)
            return False

       
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

    def draw(self):

        level = int((len(self.LODvaos)-1)*self.level)
        vao,faces = self.LODvaos[level]

        glBindVertexArray(vao)
        glEnable(GL_CULL_FACE)
        glCullFace(GL_FRONT)
        glPolygonMode( GL_FRONT_AND_BACK, GL_LINE )
        glDrawElements(GL_TRIANGLES, faces, GL_UNSIGNED_INT,
                None)  # This line does work too!

    def setLevel(self,zero2one):
        self.level = zero2one