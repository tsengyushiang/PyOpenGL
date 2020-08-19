from argparse import ArgumentParser, SUPPRESS
import math
import cv2
import numpy as np

def build_argparser():
   parser = ArgumentParser(add_help=False)
   args = parser.add_argument_group('Options')   
   args.add_argument('-h', '--help', action='help',default='SUPPRESS') 

   # custom command line input parameters       
   args.add_argument("-model", "--model", type=str,default='./medias/sample.obj')
   args.add_argument("-texture", "--texture", type=str,default='./medias/sample.png')

   return parser
args = build_argparser().parse_args()

objfile = open(args.model, 'r')
Lines = objfile.readlines()

vertice = []
uv = []
normal = []
face = []

# Strips the newline character
for line in Lines:
    contents = line.split()

    if contents[0] == 'v':
        vertice.append([float(contents[1]), float(
            contents[2]), float(contents[3])])
        uv.append([float(contents[1])*0.5+0.5, float(contents[2])*0.5+0.5])
        normal.append([float(contents[4]), float(
            contents[5]), float(contents[6])])

    elif contents[0] == 'f':
        face.append([float(contents[1]), float(
            contents[2]), float(contents[3])])

outF = open("./sample.obj", "w")

outF.write('mtllib sample.mtl\n')
outF.write('usemtl Material\n')
outF.write('s off\n')

def normalDir(normal):
    return math.copysign(1, normal[2]-0.5)

for vertex in vertice:
    outF.write("v {0} {1} {2}\n".format(vertex[0], vertex[1], vertex[2]))

for index,coord in enumerate(uv):
    if(normalDir(normal[index])==1):
        outF.write("vt {0} {1}\n".format(coord[0]/2.0, coord[1]))
    else:
        outF.write("vt {0} {1}\n".format(coord[0]/2.0+0.5, coord[1]))

for n in normal:
    outF.write("vn {0} {1} {2}\n".format(n[0], n[1], n[2]))

for f in face:
    
    f[0]=int(f[0])
    f[1]=int(f[1])
    f[2]=int(f[2])    

    if(normalDir(normal[f[0]-1])==normalDir(normal[f[1]-1]) 
    and normalDir(normal[f[1]-1])==normalDir(normal[f[2]-1])
    and normalDir(normal[f[0]-1])==normalDir(normal[f[2]-1])
    ):
        outF.write("f {0}/{0} {1}/{1} {2}/{2}\n".format(int(f[0]), int(f[1]), int(f[2])))
    else:
        outF.write("f {0} {1} {2}\n".format(int(f[0]), int(f[1]), int(f[2])))


outF.close()

sampleTexture = 'test.png'
mtlF = open("./sample.mtl", "w")

mtlF.write('newmtl Material\n')
mtlF.write('Ns 96.078431\n')
mtlF.write('Ka 0.000000 0.000000 0.000000\n')
mtlF.write('Kd 1.000000 1.000000 1.000000\n')
mtlF.write('Ks 0.000000 0.000000 0.000000\n')
mtlF.write('Ni 1.000000\n')
mtlF.write('d 1.000000\n')
mtlF.write('illum 2\n')
mtlF.write('map_Kd '+sampleTexture+'\n')

mtlF.close()

texture = cv2.imread(args.texture)
texture_gray = cv2.cvtColor(texture,cv2.COLOR_BGR2GRAY)
texture_gray = cv2.cvtColor(texture_gray,cv2.COLOR_GRAY2BGR)

vis = np.concatenate((texture, texture_gray), axis=1)
cv2.imwrite(sampleTexture, vis)
