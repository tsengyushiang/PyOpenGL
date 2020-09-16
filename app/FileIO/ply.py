# pip install plyfile
# https://pypi.org/project/plyfile/

from plyfile import PlyData, PlyElement
import numpy as np


def save(npArr, colorArr, path):

    vertex_color = np.array(colorArr,
                            dtype=[('red', 'u1'), ('green', 'u1'), ('blue', 'u1')])

    vertex = np.array(npArr,
                      dtype=[('x', 'f4'), ('y', 'f4'),
                             ('z', 'f4')])
    n = len(vertex)

    vertex_all = np.empty(n, vertex.dtype.descr + vertex_color.dtype.descr)

    for prop in vertex.dtype.names:
        vertex_all[prop] = vertex[prop]

    for prop in vertex_color.dtype.names:
        vertex_all[prop] = vertex_color[prop]

    PlyData([PlyElement.describe(vertex_all, 'vertex')], text=True).write(path)
