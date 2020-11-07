import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

from skimage import measure
from skimage.draw import ellipsoid

def marchingCube(ndarray,ContourValue=0,visualize=False):
    # Use marching cubes to obtain the surface mesh
    verts, faces, normals, values = measure.marching_cubes(ndarray,ContourValue)
        
    return verts, faces, normals