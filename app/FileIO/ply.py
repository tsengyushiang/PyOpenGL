import numpy as np
import open3d as o3d

# xyz rgb
def savePcd(npPcd,npColor,path):
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(npPcd)
    pcd.colors = o3d.utility.Vector3dVector(npColor)
    o3d.io.write_point_cloud(path, pcd)

def readPlyPoints(path):
    pcd = o3d.io.read_point_cloud(path, format='ply')
    return np.asarray(pcd.points), np.asarray(pcd.colors)

def save(npArr, colorArr, normalArr, path):
    header = ["ply",
              "format ascii 1.0",
              "element vertex "+str(len(npArr)),
              "property float x",
              "property float y",
              "property float z",
              "property uchar red",
              "property uchar green",
              "property uchar blue",
              "property uchar alpha",
              "property float nx",
              "property float ny",
              "property float nz",
              "end_header", ]

    outF = open(path, "w")

    # write header
    for line in header:
        outF.write(line)
        outF.write("\n")

    for index in range(len(npArr)):
        line = "{0} {1} {2} {3} {4} {5} {6} {7} {8} {9}\n".format(
            npArr[index][0], npArr[index][1], npArr[index][2],
            colorArr[index][0], colorArr[index][1], colorArr[index][2], colorArr[index][3],
            normalArr[index][0], normalArr[index][1], normalArr[index][2]
        )
        outF.write(line)
    outF.close()
