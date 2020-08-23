import math
import cv2
import numpy as np
from FileIO.obj import Load, save
from FileIO.mtl import save_withTexture
from Args.TwoModelTexture import build_argparser
from Algorithm.cpd import alignPointClouds

args = build_argparser().parse_args()

vertices_f,  normals_f, faces_f = Load(args.modelFront)
vertices_b,  normals_b, faces_b = Load(args.modelBack)

vertices_alignBack = alignPointClouds(vertices_f, vertices_b)
# calc uv
uvs = []

def normalDir(normal):
    return math.copysign(1, normal[2]-0.5)

for index, vertex in enumerate(vertices_f):
    if(normalDir(normals_f[index]) == 1):
        coordX = vertex[0]*0.5+0.5
        coordY = vertex[1]*0.5+0.5
        uvs.append([coordX/2.0, coordY])
    else:
        coordX = vertices_alignBack[index][0]*0.5+0.5
        coordY = vertices_alignBack[index][1]*0.5+0.5
        uvs.append([coordX/2.0+0.5, coordY])

obj = 'sample.obj'
sampleTexture = 'sample.png'
mat = 'sample.mtl'
Material = 'Material'

save('./medias/'+obj, mat, Material, vertices_f, uvs, normals_f, faces_f)
save_withTexture('./medias/'+mat, sampleTexture, Material)

texture1 = cv2.imread(args.textureFront)
texture2 = cv2.imread(args.textureBack)
vis = np.concatenate((texture1, texture2), axis=1)
cv2.imwrite('./medias/'+sampleTexture, vis)
