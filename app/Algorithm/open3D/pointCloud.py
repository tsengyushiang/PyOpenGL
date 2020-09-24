import copy
import numpy as np
import open3d as o3d

def draw_registration_result(source, target, transformation):
    source_temp = copy.deepcopy(source)
    target_temp = copy.deepcopy(target)
    source_temp.paint_uniform_color([1, 0.706, 0])
    target_temp.paint_uniform_color([0, 0.651, 0.929])
    source_temp.transform(transformation)
    o3d.visualization.draw_geometries([source_temp, target_temp])

# point noramls is necessary
def point2planeICP(pcd1,pcd2):

    max_correspondence_distance = 0.05

    source = o3d.io.read_point_cloud(pcd1, format='ply')
    target = o3d.io.read_point_cloud(pcd2, format='ply')

    trans_init = np.asarray([[1.0,0.0,0.0, 0.0],
                            [0.0, 1.0,0.0, 0.],
                            [0.0, 0.0, 1.0, 0.0],
                            [0.0, 0.0, 0.0, 1.0]])
    draw_registration_result(source, target, trans_init)
    reg_p2p = o3d.registration.registration_icp(
        source, target, max_correspondence_distance ,trans_init,
        o3d.registration.TransformationEstimationPointToPlane(), o3d.registration.ICPConvergenceCriteria(
        relative_fitness=1e-10,
        relative_rmse=0.1,
        max_iteration=100
    ))
    

    print(reg_p2p)
    print("Transformation is:")
    print(reg_p2p.transformation)
    draw_registration_result(source, target, reg_p2p.transformation)

    return reg_p2p.transformation

def normalEstimate(npPcd, cameraPos):
    # load source and target point cloud
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(npPcd)
    pcd.estimate_normals(
        search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=0.01, max_nn=300))

    pcd.orient_normals_towards_camera_location(cameraPos)

    return np.asarray(pcd.normals)
