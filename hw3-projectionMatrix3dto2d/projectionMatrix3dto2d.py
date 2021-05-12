'''

NTUST course: Computer Vision and Applications (CI5336701, 2021 Spring)
Homework#3：Calculate the distance between an object and your camera

'''

import numpy as np
import cv2

# 3d 2d feature points

# example from "Lecture07-camera calibration P.17 to verify alogrithm"
# correspondingPoints3d2d=[
#     ( (0,0,75,1),(83,146,1) ),
#     ( (0,0,25,1),(103,259,1) ),
#     ( (100,0,25,1),(346,315,1) ),
#     ( (120,90,15,1),(454,218,1) ),
#     ( (90,50,60,1),(365,161,1) ),
#     ( (0,100,25,1),(218,144,1) ),
#     ( (60,40,20,1),(286,244,1) )
# ]

# intrinsic = np.array([
#     [797.467667,0,318.980339],
#     [0,797.569342,243.459839],
#     [0,0,1]
# ])

# pick from homework image and 3d world
correspondingPoints3d2d=[
    ( (50,-50,0,1),(1109,773) ),
    ( (50,-50,50,1),(1146,598) ),
    ( (50,-100,50,1),(1366,706) ),
    ( (100,-100,0,1),(1407,789) ),
    ( (-100,50,0,1),(300,839) ),
    ( (-100,50,100,1),(227,415) ),
    ( (0,50,100,1),(669,296) ),
    ( (-100,150,100,1),(38,259) ),
]

intrinsic = np.array([
    [1308.36,0,780],
    [0,1308.36,480.50],
    [0,0,1]
])

targetPoint = np.array([-4.5,-2.5,130,1.0])
img = cv2.imread("./Photo.jpg")

# Ax = b 
A = []

for pointset in correspondingPoints3d2d:
    
    # draw select point

    cv2.circle(img,pointset[1], 15, (255, 0, 0), -1)
    cv2.putText(img, str(pointset[0]), pointset[1], cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 255), 1, cv2.LINE_AA)

    #fill A matrix for SVD
    _3dpoint = pointset[0]
    _2dpixel = pointset[1]
    
    A.append([
        _3dpoint[0],_3dpoint[1],_3dpoint[2],_3dpoint[3],
        0,0,0,0,
        -_3dpoint[0]*_2dpixel[0],-_3dpoint[1]*_2dpixel[0],-_3dpoint[2]*_2dpixel[0],-_3dpoint[3]*_2dpixel[0]
    ])

    A.append([
        0,0,0,0,
        _3dpoint[0],_3dpoint[1],_3dpoint[2],_3dpoint[3],
        -_3dpoint[0]*_2dpixel[1],-_3dpoint[1]*_2dpixel[1],-_3dpoint[2]*_2dpixel[1],-_3dpoint[3]*_2dpixel[1]
    ])

cv2.imwrite("Photo_selectedPoints.jpg",img)

# solve by SVD
U,sigma,V = np.linalg.svd(np.array(A))

# get solution and normalize
P = V[11,:].reshape((3,4))/ V[11][11]

print('projectionMatirx : \n\n', P)

# get RT -> P = K@RT
RT = np.linalg.inv(intrinsic)@P

# extrinsic parameter
normalizedRT = RT / np.linalg.norm(RT[:,0])

cameraSpaceTargetPoint = normalizedRT@targetPoint
print('\nDistance vector : \n', cameraSpaceTargetPoint, '\nDistance :\n', np.linalg.norm(cameraSpaceTargetPoint))