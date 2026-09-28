import laspy
import numpy as np
# figure out whiich algorithm library for spatial matching

def load_and_filter(file_path):
    """
    1. Open laz file using laspy
    2. Extract X,Y,Z coords into numpy arrays
    3. Filter out noise (obvious outliers)
    4. return XYZ arrays
    
    """
    pass

def find_matching_points(x_a, y_a, z_a, x_b, y_b, z_b):
    """
    Need to compare Z values, but only for points that share the same X,Y Location

    1. Think about how to efficiently find the nearest neighbor in scanB for every point in scanA.
    Use spatial indexing, KDTree or rounding X/Y to a discrete grid or create a hashmap
    2. Once matched, caluculate the absolute difference in Z: abs(z_a - z_b).
    3. Return an array of these Z-differences, and ideally, the X,Y coords of where they occured.
    """
    pass

def identify_significant_changes(z_differences, threshold=2.0):
    """
    1. Look through the z_differences array.
    2. find all indices where the difference is strictly greater than the threshold (2.0m)
    3. Return the count of these changes, and the specific X,Y,Z coords where they happened
    """

def main():
    # 1. Define the file paths for scan A and B
    # 2. Call load_and_filter for both
    # 3. call find_matching_points
    # 4. call identify_significant_changes
    # 5. Print the results to the console.
    pass

if __name__ == "__main__":
    main()
