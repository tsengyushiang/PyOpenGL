import cv2
import sys
import json
import os
import time
from dotmap import DotMap

from qtLayout.twoWindow import *
from PyQt5.QtCore import *
from Algorithm.marchingCube import *
from FileIO.ply import savePcd,save
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
                    if d*data['depth_scale'] < transPoint.z:
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
            tsdf[gl_VertexID]=1
        else:
            tsdf[gl_VertexID]=0
        '''
        elif value ==1 :
            vertices.append([point.x,point.y,point.z])
            color.append([1.0,1.0,1.0])
        '''

    return vertices,color


vL=250
tsdf = np.zeros(vL*vL*vL)

startTime = time.time()
_,_ = getDepthHull(args.depth1,args.color1,args.config1,tsdf,vL)
print('finish 1st hull',time.time()-startTime)
startTime = time.time()
_,_ = getDepthHull(args.depth2,args.color2,args.config2,tsdf,vL)
print('finish 2nd hull',time.time()-startTime)
startTime = time.time()
vertices,color = tsdf2pcd(tsdf,vL,2)
print('finish depthhull',time.time()-startTime)
startTime = time.time()
savePcd(vertices,color,os.path.join(args.output,'depthhull.ply'))
print('save',time.time()-startTime)

#verts, faces, normals = marchingCube(depthvalues.reshape((vL,vL,vL)))