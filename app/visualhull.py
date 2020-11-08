import cv2
import sys
import json
import os
import time
from dotmap import DotMap

from qtLayout.twoWindow import *
from PyQt5.QtCore import *
from Algorithm.marchingCube import *
from FileIO.ply import savePcd,save,saveMesh
from Args.medias import build_argparser

args = build_argparser().parse_args()

def convertIndex2xyz(gl_VertexID,vL):
    z = ((gl_VertexID/(vL*vL)))/vL
    zRemain = gl_VertexID%(vL*vL)
    y = vL- zRemain/vL
    x = zRemain%vL
    point = DotMap()
    point.x = (x/vL-0.5)*3
    point.y = (y/vL-0.5)*3
    point.z = z
    return point

def getDepthHull(depth,color,config,tsdf,vL=150):
    with open(config) as f:
        data = json.load(f)
    
    # depth and color map
    depthMat = cv2.imread(depth, cv2.IMREAD_UNCHANGED)
    colorMat = cv2.imread(color, cv2.IMREAD_UNCHANGED)
    sampleDepth = cv2.resize(depthMat, (vL,vL), interpolation=cv2.INTER_NEAREST)
    depthvalues = np.tile(sampleDepth.flatten(),vL)*data['depth_scale']

    # camera infos
    invCameraMat = np.linalg.inv(np.array(data['calibrateMat']))
    fx=data['depth_fx']
    fy=data['depth_fy']
    ppx=data['depth_cx']
    ppy=data['depth_cy']
    w=data['depth_width']
    h=data['depth_height']

    def point2pixel(point,depthValue):
        u = (point.x/depthValue*fx+ppx)/w
        v = (point.y/depthValue*fy+ppy)/h
        return u,v
    
    vertices = []
    color = []
    for gl_VertexID,depthValue in enumerate(depthvalues):
        if depthValue!=0 :

            point = convertIndex2xyz(gl_VertexID,vL)

            inverPoint = invCameraMat@np.array([point.x,point.y,point.z,1.0]).T
            transPoint = DotMap()
            transPoint.x = inverPoint[0]
            transPoint.y = inverPoint[1]
            transPoint.z = inverPoint[2]
            onverThrehold = invCameraMat@np.array([point.x,point.y,depthValue,1.0]).T

            u,v = point2pixel(transPoint,onverThrehold[2])
            if u>0 and u<1.0 and v>0 and v<1.0 :

                c = colorMat[int((1-v)*h)][int(u*w)]
                d = depthMat[int((1-v)*h)][int(u*w)]

                if d>0:
                    if d*data['depth_scale'] <= transPoint.z:
                        vertices.append([point.x,point.y,point.z])
                        color.append([c[2]/255.0,c[1]/255.0,c[1]/255.0])
                        tsdf[gl_VertexID] += 1
                    '''
                    else:
                        vertices.append([point.x,point.y,point.z])
                        color.append([1.0,0.0,0.0])
                    '''    
    
    return vertices,color

def tsdf2pcd(tsdf,vL,threshold=2):
    vertices = []
    color = []
    for gl_VertexID,value in enumerate(tsdf):
        point = convertIndex2xyz(gl_VertexID,vL)

        if value == 2 :
            vertices.append([point.x,point.y,point.z])
            color.append([1.0,0.0,0.0])
            tsdf[gl_VertexID]=0
        else:
            tsdf[gl_VertexID]=1
        
        '''
        elif value ==1 :
            vertices.append([point.x,point.y,point.z])
            color.append([1.0,1.0,1.0])
        '''

    return vertices,color


def depthHullApp(vL):
    
    tsdf = np.zeros(vL*vL*vL)

    startTime = time.time()
    vertices,color = getDepthHull(args.depth1,args.color1,args.config1,tsdf,vL)
    savePcd(vertices,color,os.path.join(args.output,'occupyField1.ply'))
    print('finish 1st hull',time.time()-startTime)
    startTime = time.time()
    vertices,color = getDepthHull(args.depth2,args.color2,args.config2,tsdf,vL)
    savePcd(vertices,color,os.path.join(args.output,'occupyField2.ply'))
    print('finish 2nd hull',time.time()-startTime)
    startTime = time.time()
    vertices,color = tsdf2pcd(tsdf,vL,2)
    print('finish depthhull',time.time()-startTime)
    startTime = time.time()
    savePcd(vertices,color,os.path.join(args.output,'depthhull.ply'))
    print('save',time.time()-startTime)

    verts, faces, normals = marchingCube(tsdf.reshape((vL,vL,vL)))

    verts[:,1] *= -1
    verts[:,1] += vL

    verts/=vL
    x = np.array(verts[:,0])
    verts[:,0] = verts[:,2]
    verts[:,2] = x

    verts[:,0] -= 0.5 
    verts[:,1] -= 0.5
    verts[:,0] *= 3 
    verts[:,1] *= 3

    saveMesh(verts, faces,os.path.join(args.output,'mesh.ply'))
    savePcd(verts, normals, os.path.join(args.output,'mesh.point.ply'),normals)


from Realsense.device import depth2points
from Algorithm.open3D.pointCloud import normalEstimate
def genPly(depth,color,config):

    with open(config) as f:
        data = json.load(f)

    targetX = 640
    targetY = 480
    scaleX = data['depth_width']/targetX
    scaleY = data['depth_height']/targetY
    
    ppx = data['depth_cx']/scaleX
    ppy = data['depth_cy']/scaleY
    fx = data['depth_fx']/scaleX
    fy = data['depth_fy']/scaleY

    iw = int(data['depth_width']/scaleX)
    ih = int(data['depth_height']/scaleY)

    depthscale = data['depth_scale']

    depth = cv2.imread(depth, cv2.IMREAD_UNCHANGED)
    color = cv2.imread(color, cv2.IMREAD_UNCHANGED)

    downsampleDepth = cv2.resize(
        depth, (targetX, targetY), interpolation=cv2.INTER_NEAREST)
    downsampleColor = cv2.resize(
    color, (targetX, targetY), interpolation=cv2.INTER_NEAREST)
    
    depthvalues = downsampleDepth*depthscale

    colorArr = downsampleColor.flatten().reshape(iw*ih, 3)
    pointArr = depth2points(iw, ih, ppx, ppy, fx, fy, depthvalues)

    mat4 = np.array(data['calibrateMat'])
    pos = data['positiveBoundaryCorner']
    neg = data['negativeBoundaryCorner']

    clipPoints = []
    colors = []
    nomrals = []
    uvs = []

    mask = np.zeros((ih, iw, 3), dtype=float)
    transPoints = []
    # save pointcloud and vertexcolor
    for index, points in enumerate(pointArr):

        row = index / iw
        col = index % iw
        #print(index, iw, ih, row, col)

        vec = np.array([points[0], points[1], points[2], 1.0])

        alignedVec = mat4.dot(vec)

        if(pos[0] < alignedVec[0] or
                pos[1] < alignedVec[1] or
                pos[2] < alignedVec[2] or
                neg[0] > alignedVec[0] or
                neg[1] > alignedVec[1] or
                neg[2] > alignedVec[2]):
            continue

        mask[int(row)][int(col)][0] = 255
        mask[int(row)][int(col)][1] = 255
        mask[int(row)][int(col)][2] = 255

        color = (colorArr[index][2], colorArr[index]
                 [1], colorArr[index][1], 255)

        colors.append(color)
        uvs.append((
            col/iw,(ih-row)/ih , 0, 0
        ))

        transPoints.append([
            alignedVec[0], alignedVec[1], alignedVec[2]
        ])

        clipPoints.append(
            (points[0], points[1], points[2]))

    # calc vertex normal
    nomralArr = normalEstimate(transPoints, [
        mat4[0][3], mat4[1][3], mat4[2][3]
    ])
    for n in nomralArr:
        normal = (n[0], n[1], n[2])
        nomrals.append(normal)

    return clipPoints, colors, transPoints,nomrals, uvs, mask

def pointCloudApp():

    clipPoints, colors1, transPoints1,nomrals1, uvs, mask = genPly(args.depth1,args.color1,args.config1)
    clipPoints, colors2, transPoints2,nomrals2, uvs, mask = genPly(args.depth2,args.color2,args.config2)

    points = np.concatenate((transPoints1,transPoints2))
    colors = np.concatenate((colors1,colors2))
    normals = np.concatenate((nomrals1,nomrals2))
    
    save(points, colors,normals, os.path.join(args.output,'hand.point.ply'))

#pointCloudApp()
depthHullApp(150)