import os
from os.path import isfile, join
from os import listdir
import numpy as np
from Algorithm.open3D.pointCloud import normalEstimate
from Realsense.device import depth2points

import FileIO.ply as ply
import FileIO.json as json

import cv2

from dotmap import DotMap
import scipy.misc as smi

from scipy.spatial.transform import Rotation as R

from Args.medias import build_argparser
args = build_argparser().parse_args()


def main():

    mypath = args.folder
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

    dicts = DotMap()
    for filename in onlyfiles:
        filenameBlock = filename.split('.')
        fullpath = join(args.folder, filename)
        if(filenameBlock[-2] == 'depth16'):
            dicts[filenameBlock[0]][filenameBlock[1]]['depth16'] = cv2.imread(
                fullpath, cv2.IMREAD_UNCHANGED)
        elif(filenameBlock[-2] == 'color'):
            dicts[filenameBlock[0]][filenameBlock[1]]['color'] = cv2.imread(
                fullpath, cv2.IMREAD_UNCHANGED)
        elif(filenameBlock[-2] == 'config'):
            dicts[filenameBlock[0]][filenameBlock[1]
                                    ]['config'] = json.read(fullpath)

    dataPath = join(args.folder, 'data')
    maskfoder = dataPath+'/Output_Binary_Mask/'
    pcdfolder = dataPath+'/Output/'
    shrinkedfolder = dataPath+'/Output_AP1_Shrinked/'
    uvfolder = dataPath+'/Output_UV_PointCloud/'
    camerafolder = dataPath+'/Output_Camera_1080/'
    slamfolder = dataPath+'/Output_SLAM/'
    transfolder = dataPath+'/ICP/'
    cameraTrajectory = slamfolder+'CameraTrajectory_withScale.txt'
    cameraPosStrArr = []
    if not os.path.exists(dataPath):
        os.makedirs(dataPath)

        os.makedirs(maskfoder)
        os.makedirs(pcdfolder)
        os.makedirs(shrinkedfolder)
        os.makedirs(uvfolder)
        os.makedirs(camerafolder)
        os.makedirs(transfolder)
        os.makedirs(slamfolder)
    else:
        print('Delete output folder first. none empty folder : ', dataPath)
        return

    for time in dicts.keys():
        for rs in dicts[time].keys():

            # downscale datas
            config = dicts[time][rs]['config']

            targetX = 640
            targetY = 480
            scaleX = config['depth_width']/targetX
            scaleY = config['depth_height']/targetY

            iw = int(config['depth_width']/scaleX)
            ih = int(config['depth_height']/scaleY)

            ppx = config['depth_cx']/scaleX
            ppy = config['depth_cy']/scaleY
            fx = config['depth_fx']/scaleX
            fy = config['depth_fy']/scaleY
            depthscale = config['depth_scale']

            downsampleDepth = cv2.resize(
                dicts[time][rs]['depth16'], (targetX, targetY), interpolation=cv2.INTER_NEAREST)
            downsampleColor = cv2.resize(
                dicts[time][rs]['color'], (targetX, targetY), interpolation=cv2.INTER_NEAREST)

            depthvalues = downsampleDepth*depthscale

            colorArr = downsampleColor.flatten().reshape(iw*ih, 3)
            pointArr = depth2points(iw, ih, ppx, ppy, fx, fy, depthvalues)

            mat4 = np.array(config['calibrateMat'])
            pos = config['positiveBoundaryCorner']
            neg = config['negativeBoundaryCorner']

            # gen point cloud with input data
            clipPoints, colors, transPoints,nomrals, uvs, mask = genPly(
                iw, ih, colorArr, pointArr, mat4, pos, neg)

            savePrefix = time+"_"+rs

            # save reconstruction format
            ply.save(transPoints, colors,nomrals, transfolder+savePrefix+'.ply')
            ply.saveWOnomals(clipPoints, colors, pcdfolder+savePrefix+'.ply')
            ply.saveWOnomals(clipPoints, uvs, uvfolder+savePrefix+'.ply')
            cv2.imwrite(maskfoder+savePrefix+'.png', mask)

            camera1080 = cv2.resize(
                dicts[time][rs]['color'], (1440, 1080), interpolation=cv2.INTER_NEAREST)

            cv2.imwrite(camerafolder+savePrefix+'.png', camera1080)

            r = R.from_matrix([[mat4[0][0], mat4[0][1], mat4[0][2]],
                               [mat4[1][0], mat4[1][1], mat4[1][2]],
                               [mat4[2][0], mat4[2][1], mat4[2][2]]])

            q = r.as_quat()
            cameraPosStrArr.append(
                "{0}.{1} {2} {3} {4} {5} {6} {7} {8}".format(
                    time, rs, mat4[0][3], mat4[1][3], mat4[2][3], q[0], q[1], q[2], q[3]
                )
            )

    outF = open(cameraTrajectory, "w")

    # write camera poses
    for line in cameraPosStrArr:
        outF.write(line)
        outF.write("\n")

    outF.close()

def genPly(iw, ih, colorArr, pointArr, mat4, pos, neg):
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


main()
