'''
Midterm Project: Stitching images (based on homography)
'''

import numpy as np
import cv2

DEBUG=False

def drawPoint(image,center_coordinates,index):
    if index ==0:
        color = (255, 0, 0)
    elif index==1:
        color = (0, 255, 0)
    elif index==2:
        color = (0, 0, 255)
    elif index ==3:
        color = (255, 255, 0)

    # Radius of circle
    radius = 10
    # Line thickness of 2 px
    thickness = 2    
    # Using cv2.circle() method
    # Draw a circle with blue line borders of thickness of 2 px
    image = cv2.circle(image, center_coordinates, radius, color, thickness)

def visulizeFeaturePair(srcImages,correspondingPoints,DEBUG):
    
    imagePair=[]
    for idx in range(len(srcImages)-1):

        img1 = srcImages[idx].copy()
        img2 = srcImages[idx+1].copy()

        for index,pointSet in enumerate(correspondingPoints[idx]):
            drawPoint(img1,pointSet[0],index)
            drawPoint(img2,pointSet[1],index)

        imagePair.append(np.hstack([img1,img2]))

    if DEBUG:
        cv2.imshow("FeaturePoints",np.vstack(imagePair))

    cv2.imwrite("FeaturePoints.png",np.vstack(imagePair))


def directSolveHomography(correspondingPoints):
    # fill ax=b matrix
    a_arr = []
    b_arr = []
    for pointSet in correspondingPoints:
        srcPoint = pointSet[0]
        dstPoint = pointSet[1]
        a_arr.append([srcPoint[0],srcPoint[1],1,0,0,0,-dstPoint[0]*srcPoint[0],-dstPoint[0]*srcPoint[1]])
        a_arr.append([0,0,0,srcPoint[0],srcPoint[1],1,-dstPoint[1]*srcPoint[0],-dstPoint[0]*srcPoint[1]])
        b_arr.append(dstPoint[0])
        b_arr.append(dstPoint[1])

    # sovle ax=b and fill H
    x = np.linalg.solve(np.array(a_arr), np.array(b_arr))
    h = np.array([
        [x[0],x[1],x[2]],
        [x[3],x[4],x[5]],
        [x[6],x[7],1],
    ])
    h_inverse = np.linalg.inv(h)
    return h,h_inverse

srcImages = [
    cv2.imread("004.JPG"),
    cv2.imread("003.JPG"),
    cv2.imread("002.JPG"),
    cv2.imread("001.JPG"),
]

correspondingPoints=[
    [#004.JPG and 003.JPG
        ((387,225),(84,202)),
        ((605,319),(306,300)),
        ((574,674),(281,658)),
        ((357,642),(68,625)),
    ],
    [#003.JPG and 002.JPG
        ((565,352),(266,345)),
        ((711,356),(408,345)),
        ((635,729),(346,712)),
        ((330,610),(40,613)),
    ],
    [#002.JPG and 001.JPG
        ((251,227),(24,217)),
        ((643,214),(424,214)),
        ((591,695),(385,691)),
        ((345,711),(136,718)),
    ]
]

visulizeFeaturePair(srcImages,correspondingPoints,DEBUG)

# homographys to warp point from-to : 3-4 2-3 1-2 1
homographys=[]
for i in range(len(correspondingPoints)):
    h,h_inverse = directSolveHomography(correspondingPoints[i])
    homographys.append(h_inverse)
homographys.append(np.identity(3))

# create result canvas
paddingY = 100
paddingX = 1200
h = srcImages[0].shape[0] + paddingY
w = srcImages[0].shape[1] + paddingX

warpImages = []
for i in range(len(srcImages)):
    warpImages.append(np.zeros((h,w,3), np.uint8))

blendingResult = np.zeros((h,w,3), np.uint8)

# project point to get colors
for i in range(warpImages[0].shape[0]):
    for j in range(warpImages[0].shape[1]):
        
        srcPoint = np.array([j-paddingX,i-paddingY,1])

        value = np.array([0,0,0])
        count = 0
        for idx in range(len(srcImages),0,-1):
            index = idx-1
            # 3 2 1 0

            srcPoint = homographys[index]@srcPoint
            srcPoint /= srcPoint[2]

            if srcPoint[1] > 0 and srcPoint[1]<srcImages[index].shape[0] and srcPoint[0] > 0 and srcPoint[0]<srcImages[index].shape[1]:
                warpImages[len(srcImages)-idx][i,j] = srcImages[index][int(srcPoint[1]),int(srcPoint[0])]

                value[0] += int(srcImages[index][int(srcPoint[1]),int(srcPoint[0])][0])
                value[1] += int(srcImages[index][int(srcPoint[1]),int(srcPoint[0])][1])
                value[2] += int(srcImages[index][int(srcPoint[1]),int(srcPoint[0])][2])
                count += 1
        
        blendingResult[i,j] = value/count


for idx,result in enumerate(warpImages):
    cv2.imwrite("warpResult"+str(idx)+".png",result)
cv2.imwrite('blendingResult.png',blendingResult)

if DEBUG:
    for idx,result in enumerate(warpImages):
        cv2.imshow('Result'+str(idx),result)
    cv2.imshow('Result',blendingResult)
    cv2.waitKey(0)
    cv2.destroyAllWindows()