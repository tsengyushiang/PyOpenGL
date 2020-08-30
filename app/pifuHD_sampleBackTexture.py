import math
import cv2
import numpy as np
from FileIO.obj import Load, save
from FileIO.mtl import save_withTexture
from Args.TwoModelTexture import build_argparser
from Algorithm.cpd import alignPointClouds
from Algorithm.png import tuneBorder

args = build_argparser().parse_args()

obj = 'sample.obj'
sampleTexture = 'sample.png'
mat = 'sample.mtl'
Material = 'Material'

save_withTexture('./medias/'+mat, sampleTexture, Material)

texture1 = cv2.imread(args.textureFront, cv2.IMREAD_UNCHANGED)
texture2 = cv2.imread(args.textureBack, cv2.IMREAD_UNCHANGED)
'''
texture1 = tuneBorder(texture1)
texture2 = tuneBorder(texture2)
'''
vertices_f,  normals_f, faces_f = Load(args.modelFront)
vertices_b,  normals_b, faces_b = Load(args.modelBack)

vertices_alignBack = alignPointClouds(vertices_f, vertices_b)
# calc uv
uvs = []


def normalDir(normal):
    return math.copysign(1, normal[2]-0.5)


# handle texture
for index, vertex in enumerate(vertices_f):
    coordFrontX = vertex[0]*0.5+0.5
    coordFrontY = vertex[1]*0.5+0.5
    coordBackX = vertices_alignBack[index][0]*0.5+0.5
    coordBackY = vertices_alignBack[index][1]*0.5+0.5
    if(texture2[texture2.shape[0]-int(coordBackY*texture2.shape[0]), int(coordBackX*texture2.shape[1])][3] == 0):
        texture2[texture2.shape[0]-int(coordBackY*texture2.shape[0]), int(coordBackX*texture2.shape[1])
                 ] = texture1[texture1.shape[0]-int(coordFrontY*texture1.shape[0])-1, int(coordFrontX*texture1.shape[1])-1]

    if((normalDir(normals_f[index])) == 1):
        uvs.append([coordFrontX/2.0, coordFrontY])
    else:
        uvs.append([coordBackX/2.0+0.5, coordBackY])
# handle edge face
for index, f in enumerate(faces_f):

    uv1 = f[0]
    uv2 = f[1]
    uv3 = f[2]

    textureSideOfv1 = normalDir(normals_f[int(f[0])-1])
    textureSideOfv2 = normalDir(normals_f[int(f[1])-1])
    textureSideOfv3 = normalDir(normals_f[int(f[2])-1])

    if (textureSideOfv1 == textureSideOfv2 and textureSideOfv1 != textureSideOfv3):
        # v3 on the other side
        uv3 = uv1

    if (textureSideOfv1 == textureSideOfv3 and textureSideOfv1 != textureSideOfv2):
        # v2 on the other side
        uv2 = uv1

    if (textureSideOfv2 == textureSideOfv3 and textureSideOfv1 != textureSideOfv2):
        # v1 on the other side
        uv1 = uv2

    faces_f[index] = [[f[0], uv1], [f[1], uv2], [f[2], uv3]]

save('./medias/'+obj, mat, Material, vertices_f, uvs, normals_f, faces_f)

# make mask of where the transparent bits are
'''
trans_mask = texture2[:,:,3] == 0
texture2[trans_mask] = texture1[trans_mask]
'''

vis = np.concatenate((texture1, texture2), axis=1)
cv2.imwrite('./medias/'+sampleTexture, vis)
