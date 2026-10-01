import laspy
import numpy as np
import open3d as o3d
import sys
from scipy.spatial import KDTree
from synthetic_test_data import generate_test_data
from visualize_changes import visualize_changes

def load_and_filter(file_path):
    """
    1. Open laz file using laspy
    2. Extract X,Y,Z coords into numpy arrays
    3. Filter out noise (obvious outliers)
    4. return XYZ arrays
    """
    try:
        las = laspy.read(file_path)
        coords = las.xyz

        pcd = o3d.geometry.PointCloud()
        pcd.points = o3d.utility.Vector3dVector(coords)

        cl, ind = pcd.remove_statistical_outlier(nb_neighbors=20, std_ratio=2.0)

        cleaned = pcd.select_by_index(ind)

        return np.asarray(cleaned.points)

    except FileNotFoundError:
        print("File not found")
        sys.exit(1)

def find_matching_points(points_a, points_b, xy_tolerance=0.5):
    """
    points_a and points_b are Nx3 numpy arrays
    xy_tolerance is how close the X,Y must be to be considered a match (e.g 0.5metres)

    1. build cKDtree using only the X and Y coords of points_b (only match horizontal location first)
    2. Query this tree using the X and Y coordinates of points_a (for every point in A, what is the nearest neighbor in B, and what is the distance?)
    3. Filter the results: keep only matches where the horizontal distance is <= xy_tolerance
    4. For those valid matches, extract the Z value from points_a, and the Z value from points_b
    5. Calculate the absolute difference: abs(z_a, z_b)
    6. return the X,Y coordinates of the matches and their calculated z differences
    """
    xy_points_a = points_a[:, :2]
    xy_points_b = points_b[:, :2]
    
    tree = KDTree(xy_points_b)

    distance, index = tree.query(xy_points_a)

    valid_mask = distance <= xy_tolerance

    matched_points_a = points_a[valid_mask]
    matched_points_b = points_b[index[valid_mask]] # type: ignore

    z_a_matched = matched_points_a[:, 2]
    z_b_matched = matched_points_b[:, 2]

    difference = np.abs(z_a_matched - z_b_matched)

    return matched_points_a, matched_points_b, difference


def identify_significant_changes(matched_points_a, differences, threshold=2.0):
    """
    matched_points_a: The XYZ points from scan A that had a valid horizontal match.
    differences: The array of absolute Z differences for those matches
    threshold: the Minimum Z difference to be considered significant change.

    1. create a boolean mask where the differences array is strictly greater than the threshold
    2. use that mask to filter 'matched_points_a', keeping only the locations of significant changes.
    3. calculate the total count of these significant changes.
    4. return the count and the filtered array of points where the significant changes occured
    """

    greater_mask = differences > threshold
    significant_changes = matched_points_a[greater_mask]

    change_count = len(significant_changes)

    return change_count, significant_changes

def main():
    # 1. Define the file paths for scan A and B
    #file1 = "/Users/jamescawthray/Desktop/DEV/2026projects/change-detection-engine/Data/2011-clean.laz"
    #file2 = "/Users/jamescawthray/Desktop/DEV/2026projects/change-detection-engine/Data/2018-clean.laz"
    arr_a, arr_b = generate_test_data()
    
    # 2. Call load_and_filter for both
    # 3. call find_matching_points
    matched_a, matched_b, diff = find_matching_points(arr_a, arr_b)
    # 4. call identify_significant_changes
    ch_count, sig_changes = identify_significant_changes(matched_a, diff)
    # 5. Print the results to the console.
    print(f"Change count: {ch_count}, Significant changes: {sig_changes}")
    visualize_changes(arr_a, sig_changes)

if __name__ == "__main__":
    main()
