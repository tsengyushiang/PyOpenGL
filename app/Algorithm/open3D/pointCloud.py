import copy
import numpy as np
import open3d as o3d


def normalEstimate(npPcd):
    # load source and target point cloud
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(npPcd)
    pcd.estimate_normals(
        search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=0.01, max_nn=300))

    return np.asarray(pcd.normals)*-1
