# 1: Python Baseline for LiDAR Change Detection

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

# 2: C++ Spatial Hash Grid Optimization

### Performance Results
- **Brute-force (50k points):** 13,837ms
- **Spatial hash grid (50k points):** 262ms
- **Speedup:** 52x quicker

## 3: Python Integration via pybind11

### Architecture
- Built a Python extension module exposing C++ functions
- Simplified API: `detect_changes(points_a, points_b, xy_tolerance, z_threshold, cell_size)`
- Hidden complexity: Grid building and spatial indexing happen internally in C++

### Performance
- 50,000 points processed in ~160ms from Python
- Same performance as native C++ (zero overhead from Python bridge)

## 4: Intelligent Change Classification with PyTorch

### Architecture
- **AI**: Used a lightweight Multi-Layer Perceptron (MLP) instead of a black-box 3D CNN.
- **Features**: Classifies changes based on 3 interpretable geometric features: `z_diff`, `local_density`, and `z_variance`.
- **Classes**: `0 = Sensor Noise`, `1 = Tree Fall`, `2 = New Structure`.

### Results
- Achieved **>95% test accuracy** on synthetic data.
- Inference correctly classifies scenarios with >95% confidence.
