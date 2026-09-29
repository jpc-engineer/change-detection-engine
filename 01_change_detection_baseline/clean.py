import open3d as o3d
import laspy 
import numpy as np

def clean_filter_save(file_path):
    las = laspy.read(file_path)

    coords = las.xyz

    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(coords)

    cl, ind = pcd.remove_statistical_outlier(nb_neighbors=20, std_ratio=3.0)
    cleaned = pcd.select_by_index(ind)

    # SAVE CLEAN FILE
    cleaned_coords = np.asarray(cleaned.points)

    new_header = laspy.LasHeader(version=las.header.version, point_format=las.header.point_format)
    new_header.offsets = las.header.offsets
    new_header.scales = las.header.scales

    cleaned_laz = laspy.LasData(new_header)

    # populate coords (laspy automatically handles scales/offsets)
    cleaned_laz.x = cleaned_coords[:, 0]
    cleaned_laz.y = cleaned_coords[:, 1]
    cleaned_laz.z = cleaned_coords[:, 2]

    # keep intensities
    cleaned_laz.intensity = las.intensity[ind]
    cleaned_laz.classification = las.classification[ind]

    # write to file
    output_path = "2018-clean.laz"
    cleaned_laz.write(output_path)

#o3d.visualization.draw_geometries([cleaned])

