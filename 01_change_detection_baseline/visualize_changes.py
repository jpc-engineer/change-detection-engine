import open3d as o3d
import numpy as np

def visualize_changes(baseline_points, change_points):

    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(baseline_points)
    color_len = len(baseline_points)

    colors_arr = np.full((color_len, 3), 0.7)
    pcd.colors = o3d.utility.Vector3dVector(colors_arr)

    # Change points
    pcd2 = o3d.geometry.PointCloud()
    pcd2.points = o3d.utility.Vector3dVector(change_points)
    color_len2 = len(change_points)

    colors_arr2 = np.full((color_len2, 3), [1.0, 0.0, 0.0])
    pcd2.colors = o3d.utility.Vector3dVector(colors_arr2)

    # visualize
    o3d.visualization.draw_geometries([pcd, pcd2])

    return

