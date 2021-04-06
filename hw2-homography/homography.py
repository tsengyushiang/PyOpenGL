'''
Homework#2 Using homography to swap the contents of two photo frames
'''

import numpy as np
import cv2

DEBUG=True

def drawPoint(image,center_coordinates,color = (255, 0, 0)):        
    # Radius of circle
    radius = 5

    # Line thickness of 2 px
    thickness = 2
    
    # Using cv2.circle() method
    # Draw a circle with blue line borders of thickness of 2 px
    image = cv2.circle(image, center_coordinates, radius, color, thickness)


src = cv2.imread('./ArtGallery.jpg')

if DEBUG:
    cv2.imshow('src',src)

# choose by https://pixlr.com/tw/e/#editor, counter-clock-wise is necessary to build polygon mask latter
correspondingPoints=[
    ((41,104),(685,121)),
    ((342,124),(958,68)),
    ((343,427),(957,516)),
    ((42,446),(681,454)),
]

if DEBUG:
    debug = src.copy()
    for pointSet in correspondingPoints:
        print(pointSet)
        drawPoint(debug,pointSet[0],(255, 0, 0))
        drawPoint(debug,pointSet[1],(0, 255, 0))
        cv2.line(debug,(pointSet[0][0],pointSet[0][1]),(pointSet[1][0],pointSet[1][1]),(255,0,0),2)
    cv2.imshow('correspondingPoints',debug)
    cv2.imwrite('correspondingPoints.jpg', debug)

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

# porject point form src to dst
if DEBUG:
    for pointSet in correspondingPoints:
        srcPoint = np.array([pointSet[0][0],pointSet[0][1],1])
        projectPoint = h@srcPoint
        projectPoint /= projectPoint[2]
        print(projectPoint,pointSet[1])

# make mask for each region for latter project pixel
maskSrc = src.copy()
maskSrc[:]=(0,0,0)
maskDst = src.copy()
maskDst[:]=(0,0,0)
srcPoly=[]
dstPoly=[]
maskColor = np.array([255,255,255])

for pointSet in correspondingPoints:
    srcPoly.append([pointSet[0][0],pointSet[0][1]])
    dstPoly.append([pointSet[1][0],pointSet[1][1]])

cv2.fillPoly(maskSrc, [np.array(srcPoly)], (255,255,255))
cv2.fillPoly(maskDst, [np.array(dstPoly)], (255,255,255))

if DEBUG:
    cv2.imshow('Masksrc',maskSrc)
    cv2.imwrite('Masksrc.jpg', maskSrc)
    cv2.imshow('Maskdst',maskDst)
    cv2.imwrite('Maskdst.jpg', maskDst)


result = src.copy()
for i in range(result.shape[0]):
    for j in range(result.shape[1]):
        if(maskDst[i,j]==maskColor).all():
            srcPoint = np.array([j,i,1])
            projectPoint = h_inverse@srcPoint
            projectPoint /= projectPoint[2]
            result[i,j]=src[int(projectPoint[1]),int(projectPoint[0])]
        elif(maskSrc[i,j]==maskColor).all():
            srcPoint = np.array([j,i,1])
            projectPoint = h@srcPoint
            projectPoint /= projectPoint[2]
            result[i,j]=src[int(projectPoint[1]),int(projectPoint[0])]

cv2.imwrite('M10815098.jpg', result)


if DEBUG:
    cv2.imshow('Result',result)

if DEBUG:
    cv2.waitKey(0)
    cv2.destroyAllWindows()