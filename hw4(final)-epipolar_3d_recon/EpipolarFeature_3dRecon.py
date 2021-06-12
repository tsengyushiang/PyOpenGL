
import numpy as np
import cv2

DEBUG=False

# determine is laser pixel
def isLaserPixelFromRGB(pixelRGB):
    sum  = float(pixelRGB[0])+float(pixelRGB[1])+float(pixelRGB[2])
    return sum > 100

# get laser line pixel of each row in left image
def getSideFeatures(offsetX,img):
    w = img.shape[1]
    h = img.shape[0]
    features = []
    for j in range(h):
        xIndex = []
        for i in range(int(w/2)):        
            if(isLaserPixelFromRGB(img[j][offsetX+i])):
                xIndex.append(i)

        if len(xIndex)>3:
            features.append([j,xIndex[int(len(xIndex)/2)+1],1.0])
    
    return np.array(features)

# know fundamental matrix F and one feature pixel
# return other pixel is on epipolar line or not
def fundamentalMatrixError(F,knowPixel,determinePixel):
    p1 = np.array([knowPixel[1],knowPixel[0],knowPixel[2]])
    pp1 = np.array([determinePixel[1],determinePixel[0],determinePixel[2]])
    return pp1.T@F@p1

# know projection matrix to view0,view1, correspond uv pixel
# return reconstruct 3d point
def directTriangulationMethod(p0,p1,uv0,uv1):
    A = np.array([
        uv0[0]* p0[2]-p0[0],
        uv0[1]* p0[2]-p0[1],
        uv1[0]* p1[2]-p1[0],
        uv1[1]* p1[2]-p1[1]
    ])
    U,S,V = np.linalg.svd(np.array(A))
    X = V[-1]
    X = X/X[-1]
    return X

P_left = np.array([
    [1496.880651, 0.000000, 605.175810],
    [0.000000, 1490.679493, 338.418796],
    [0.000000, 0.000000, 1.000000]
])@np.array([
    [1.0, 0.0, 0.0, 0.0],
    [0.0, 1.0, 0.0, 0.0],
    [0.0, 0.0, 1.0, 0.0]
])

P_right = np.array([
    [1484.936861, 0.000000, 625.964760],
    [0.000000, 1480.722847, 357.750205],
    [0.000000, 0.000000, 1.000000]
])@np.array([
    [0.893946, 0.004543, 0.448151, -186.807456], 
    [0.013206, 0.999247, -0.036473, 3.343985],
    [-0.447979, 0.038523, 0.893214, 45.030463] 
])

F = np.array([
    [0.000000191234, 0.000003409602, -0.001899934537],
    [0.000003427498,-0.000000298416,-0.023839273818],
    [-0.000612047140,0.019636148869,1.000000000000]
]).T

result = open("{0}.xyz".format("M10815098"), "a")

for index in range(193):
    filenmae = "./SidebySide/SBS_{0}.jpg".format(str(index).zfill(3))
    print("working on {0}...".format(filenmae))

    img = cv2.imread(filenmae)
    featurePointmap = img.copy()

    leftfeatures = getSideFeatures(0,img)
    rightfeatures = getSideFeatures(int(img.shape[1]/2),img)

    if DEBUG:
        for lf in leftfeatures:
            featurePointmap[int(lf[0])][int(lf[1])][0] = 255
            featurePointmap[int(lf[0])][int(lf[1])][1] = 0
            featurePointmap[int(lf[0])][int(lf[1])][2] = 0

        for rf in rightfeatures:
            featurePointmap[int(rf[0])][int(rf[1])+int(img.shape[1]/2)][1] = 255
            featurePointmap[int(rf[0])][int(rf[1])+int(img.shape[1]/2)][2] = 0
            featurePointmap[int(rf[0])][int(rf[1])+int(img.shape[1]/2)][2] = 0

    skip=0
    for lf in leftfeatures:
        minErrPoint = None
        minErr = img.shape[0]
        for rf in rightfeatures:
            err = abs(fundamentalMatrixError(F,lf,rf))
            if(err<minErr):
                minErrPoint = rf 
                minErr = err
        
        if minErrPoint is not None:
            point = directTriangulationMethod(
                P_left,
                P_right,
                np.array([lf[1],lf[0],lf[2]]),
                np.array([minErrPoint[1],minErrPoint[0],minErrPoint[2]])
            )
            result.writelines("{0} {1} {2}\n".format(point[0],point[1],point[2]))

            if DEBUG:
                skip+=1
                if(skip%5==0):
                    img = cv2.line(img, (int(lf[1]), int(lf[0])), (int(minErrPoint[1])+int(img.shape[1]/2), int(minErrPoint[0])), (0, 0, 255), 1)

    if DEBUG:
        cv2.imshow("correspondFeaturePoints",img)
        cv2.imshow("FeaturePoints",featurePointmap)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

result.close()

# lecture08-3D reconstruction P.24 example data
# P = np.array([
#     [2.0179, 1.5967, -0.5695, 113.8805],
#     [0.2820, -0.7636, -2.4258, 305.7125],
#     [-0.0009, 0.0023, -0.0018, 1.0]
# ])

# Pp=np.array([
#     [2.8143,-1.3450,-0.5673, 347.4957],
#     [-0.4439, -0.4444, -3.0134, 371.1864],
#     [0.0023, 0.0023, -0.0018, 1.0]
# ])

# x = np.array([259,120,1])
# xp = np.array([395,89,1])

# directTriangulationMethod(P,Pp,x,xp)