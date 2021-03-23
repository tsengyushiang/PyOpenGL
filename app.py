'''
Anaconda env setup command :

    conda create -n hw1-visualhull python=3.7
    conda activate hw1-visualhull
    conda install -c conda-forge opencv
    python app.py

place app.py at root folder and structure will be like :

Homework#1
 | Bird
    | 01.bmp
    | 02.bmp
    | *.bmp
 | Last
    | 01.bmp
    | 02.bmp
    | *.bmp
 | Monkey
    | 01.bmp
    | 02.bmp
    | *.bmp
 | Teapot
    | 01.bmp
    | 02.bmp
    | *.bmp
 | Camera Parameter.txt 
 | app.py

output

Homework
 | Bird.xyz
 | Last.xyz
 | Monkey.xyz
 | Teapot.xyz

'''

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
def ComputeVisaulhull(imgFolder,camParmTxt):

    InstrisicParam = [] # 3 * 3
    ExtrinsicParam = [] # N * 3 * 4 
    Images = []

    mode = 0 # 0 save InstrisicParam, 1 save ExtrinsicParam
    with open(camParmTxt, 'r') as file:
        # reading each line    
        for line in file:
            # reading each word  
            for word in line.split():
                if(word == "Instrisic"):
                    mode = 0
                elif(word =="Extrinsic"):
                    mode = 1
                elif(word == "Parameter" or word =="for"):
                    pass
                else:
                    if (is_float(word)):
                        if(mode == 0):
                            InstrisicParam.append(float(word))
                        elif(mode==1):
                            ExtrinsicParam.append(float(word))
                    else :
                        filePath = "./"+imgFolder+"/"+word
                        image = cv.imread(filePath,0)
                        Images.append(image)
                        
                        if DEBUG:
                            cv.imshow('img',image)
                            cv.waitKey(0)
    
    instr = np.array(InstrisicParam).reshape((3,3))
    extri =  np.array(ExtrinsicParam).reshape((len(Images),3,4))
    
    if DEBUG:
        print("Instrisic Parameter")
        print(instr)
        print("Extrinsic Parameter")
        print(extri)

    result = open("{0}.xyz".format(imgFolder), "a")

    # set 3d point range
    min = (-50,-50,0)
    max = (50,50,100)
    for x in range(min[0],max[0]):
        for y in range(min[1],max[1]):
            for z in range(min[2],max[2]):
                point = np.array([x,y,z,1.0])

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
                    result.writelines("{0} {1} {2}\n".format(x,y,z))

    result.close()
    print("Visaulhull Done : {0}.xyz".format(imgFolder))

imageSet = ["Teapot","Bird","Last","Monkey"]
param = "./Camera Parameter.txt"

for folder in imageSet :
    ComputeVisaulhull(folder,param)
