# Module 1: Python Baseline for LiDAR Change Detection

## Objective
Build a vectorized Python pipeline to detect significant Z-axis changes (>2.0m) between two LiDAR point clouds.

## Approach
1. **Spatial Matching:** Used `scipy.spatial.KDTree` to efficiently find nearest neighbors in 2D (X,Y) space.
2. **Vectorized Math:** Used NumPy arrays for high-performance Z-difference calculations.
3. **Synthetic Testing:** Created controlled test data to validate the pipeline logic before working with real LAZ files.

## Key Functions
- `load_and_filter()`: Loads LAZ files and removes statistical outliers using Open3D.
- `find_matching_points()`: Core logic using KD-Trees to match points horizontally and calculate Z differences.
- `identify_significant_changes()`: Filters results to only include changes above a threshold.

## Challenges Solved
- **The Matching Problem:** LiDAR scans don't have the same number of points or ordering. Solved with KD-Tree spatial indexing.
  
- **Synthetic Data Logic:** Ensured test data had matching X,Y coordinates to properly validate the matching algorithm.

## Results
Tested with synthetic data: Successfully detected 5 out of 5 deliberately modified points with 3.0m Z-change.
