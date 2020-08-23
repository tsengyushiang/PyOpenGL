import copy
import numpy as np
import open3d as o3
from probreg import cpd


def alignPointClouds(front, back, intensity=0.05):
    # load source and target point cloud
    source = o3.geometry.PointCloud()
    source.points = o3.utility.Vector3dVector(front)

    R = source.get_rotation_matrix_from_xyz((0, np.pi, 0))
    source.rotate(R, center=(0, 0, 0))

    target = o3.geometry.PointCloud()
    target.points = o3.utility.Vector3dVector(back)

    result = copy.deepcopy(source)

    # uniform sample
    source = source.voxel_down_sample(voxel_size=intensity)
    target = target.voxel_down_sample(voxel_size=intensity)

    # compute cpd registration
    tf_param, _, _ = cpd.registration_cpd(source, target)
    result.points = tf_param.transform(result.points)

    # draw result
    '''
    source.paint_uniform_color([1, 0, 0])
    target.paint_uniform_color([0, 1, 0])
    result.paint_uniform_color([0, 0, 1])
    o3.visualization.draw_geometries(
        [source, target, result.voxel_down_sample(voxel_size=intensity)])
    '''
    
    return np.asarray(result.points)
