# pip install plyfile
# https://pypi.org/project/plyfile/

from plyfile import PlyData, PlyElement
import numpy as np

def save(npArr, path):
    vertex = np.array(npArr,
                      dtype=[('x', 'f4'), ('y', 'f4'),
                             ('z', 'f4')])
    el = PlyElement.describe(vertex, 'vertex')
    PlyData([el]).write(path)
