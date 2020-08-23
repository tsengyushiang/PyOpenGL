from argparse import ArgumentParser, SUPPRESS
import math
import cv2
import numpy as np


class MODE:
    pass


mode = MODE()
mode.all = 0
mode.front = 1
mode.back = 2


def build_argparser():
    parser = ArgumentParser(add_help=False)
    args = parser.add_argument_group('Options')
    args.add_argument('-h', '--help', action='help', default='SUPPRESS')

    # custom command line input parameters
    args.add_argument("-model", "--model", type=str,
                      default='./medias/sample.obj')
    args.add_argument("-mode", "--mode", type=int, default=mode.all)

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

filename = 'fullPointCloud'
if args.mode == mode.front:
    filename = 'frontPointCloud'
elif args.mode == mode.back:
    filename = 'backPointCloud'

outF = open("./medias/"+filename+".txt", "w")

def normalDir(normal):
    return math.copysign(1, normal[2]-0.5)

for index, vertex in enumerate(vertice):

    if args.mode == mode.front:
        if((normalDir(normal[index]) == 1)):
            outF.write("{0} {1} {2}\n".format(
                vertex[0], vertex[1], vertex[2]))
    elif args.mode == mode.back:
        if((normalDir(normal[index]) != 1)):
            outF.write("{0} {1} {2}\n".format(
                vertex[0], vertex[1], vertex[2]))
    else:
        outF.write("{0} {1} {2}\n".format(
            vertex[0], vertex[1], vertex[2]))
