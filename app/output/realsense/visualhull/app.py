import os
import cv2 as cv
import numpy as np

def is_float(value):
  try:
    float(value)
    return True
  except:
    return False

DEBUG = False
def ComputeVisaulhull(imgFolder):

    InstrisicParam = [
        [1386.903564453125,0.0,948.6588745117188],
        [0.0,1383.8934326171875,535.3060913085938],
        [0.0,0.0,1.0]
    ] # 3 * 3

    matrix = np.array([
        [
            0.031781489086497014,
            0.8891655910562317,
            -0.4569244949440145,
            0.33334336621930843
        ],
        [
            -0.36988290909546123,
            -0.41425393119555887,
            -0.8318568503624165,
            0.4758937801885053
        ],
        [
            -0.9292045776611076,
            0.17746534276198708,
            0.3247928731034423,
            -0.1002935547680947
        ],
        [
            0.0,
            0.0,
            0.0,
            1.0
        ]
    ])
    e = np.linalg.inv(matrix)

    matrix2 = np.array([
        [
            0.25045862126316204,
            0.5792983982219013,
            0.7760272217284363,
            -0.514156332448194
        ],
        [
            -0.17381904770402767,
            0.8154357054787459,
            -0.5526173657212605,
            0.4761588604089298
        ],
        [
            -0.9582100324232633,
            -0.00987057745995687,
            0.2868283623965319,
            -0.0815365204250147
        ],
        [
            0.0,
            0.0,
            0.0,
            1.0
        ]
    ])
    e2 = np.linalg.inv(matrix2)
    print(e)
    print(e2)
    ExtrinsicParam = [
        [
            e2[0],
            e2[1],
            e2[2]
        ],
        [
            e[0],
            e[1],
            e[2]
        ]
    ] # N * 3 * 4 

    Images = [
        cv.imread("2.png",0),
        cv.imread("1.png",0)
    ] 

    instr = np.array(InstrisicParam)
    extri =  np.array(ExtrinsicParam)

    if DEBUG:
        print("Instrisic Parameter")
        print(instr)
        print("Extrinsic Parameter")
        print(extri)

    result = open("{0}.obj".format(imgFolder), "a")
    result.truncate(0)
    # set 3d point range
    min = (-50,-50,-50)
    max = (50,50,50)
    scale = 0.01
    for x in range(min[0],max[0]):
        for y in range(min[1],max[1]):
            for z in range(min[2],max[2]):
                point = np.array([x*scale,y*scale,z*scale,1.0])

                passCount = 0
                # project point to each images
                for idx in range(len(Images)):
                    img = Images[idx]
                    pixel = instr@extri[idx]@point.T
                    pixel = pixel/pixel[2]
                    if(pixel[1]>=img.shape[0] or pixel[0]>=img.shape[1] or pixel[0]<0 or pixel[1]<0 or img[int(pixel[1])][int(pixel[0])] ==0 ):
                        break
                    else:
                        passCount = passCount  +1
                
                # visbile on all image then is vaild voxel
                if (passCount==len(Images)):
                    result.writelines("v {0} {1} {2} {3} {4} {5}\n".format(x,y,z,
                    img[int(pixel[1])][int(pixel[0])],
                    img[int(pixel[1])][int(pixel[0])],
                    img[int(pixel[1])][int(pixel[0])]))

    result.close()
    print("Visaulhull Done : {0}.obj".format(imgFolder))


ComputeVisaulhull("visualhull0")
