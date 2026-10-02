#include <iostream>
#include <vector>
#include <string>
#include <fstream>
#include <cmath>
#include <limits>
#include <sstream>
#include <chrono>
#include <unordered_map>

// Data structure
struct Point3D {
    float x;
    float y;
    float z;
};

// I/O
// Read txt file where each line is "X Y Z"
std::vector<Point3D> load_points_from_csv(const std::string& file_path) {
    
    // 1. Open the file using std::ifstream.
    std::ifstream file(file_path);
    if (!file.is_open()) {
        std::cerr << "Error: Could not open file. " << file_path << std::endl;
        return {};
    }
    // 2. Read line by line
    std::vector<Point3D> points;
    std::string line;
    while (std::getline(file, line)) {
        std::stringstream ss(line);
        std::string val_x, val_y, val_z;

        // 3. Parse the X,Y,Z floats
        if (std::getline(ss, val_x, ',') && 
            std::getline(ss, val_y, ',') &&
            std::getline(ss, val_z, ',')) {
                // 4. Create a Point3D and push it into the vector
                Point3D pt;
                pt.x = std::stof(val_x);
                pt.y = std::stof(val_y);
                pt.z = std::stof(val_z);

                points.push_back(pt);
            }
    }
    file.close();
    return points;
}

// GRID BUILDER
// map a 2D grid coordinate (cell_x, cell_y) to a list of pointers to points in B
// To make it easy for the unordered_map, we combine cell_x and cell_y into a single long long "key".
std::unordered_map<long long, std::vector<const Point3D*>> build_spatial_grid(
    const std::vector<Point3D>& points_b, float cell_size)
    {
        std::unordered_map<long long, std::vector<const Point3D*>> grid;
        // 1. iterate through points_b using standard index loop for (size_t i=0 etc) so we can get the memoryaddress `&points_b[i]`
        for (size_t i = 0; i < points_b.size(); i++) {
            // 2. Calculate the grid cell X and Y:
            int cell_x = static_cast<int>(std::floor(points_b[i].x / cell_size));
            int cell_y = static_cast<int>(std::floor(points_b[i].y / cell_size));
            // 3. combine them into a unique key:
            // (the multiplier ensures X and Y dont overlap)
            long long key = (static_cast<long long>(cell_x) * 1000000) + cell_y;

            // 4. Push the memory address of the point into the grids bucket:
            // gid[key].push_back(&points_b[i]);
            grid[key].push_back(&points_b[i]);
        }
    
        return grid;
    }

// OPTIMISED SEARCH
std::vector<Point3D> find_significant_changes(
    const std::vector<Point3D>& points_a,
    const std::unordered_map<long long, std::vector<const Point3D*>>& grid,
    float xy_tolerance,
    float z_threshold,
    float cell_size)
    {
        std::vector<Point3D> changes;
        float xy_tol_sq = xy_tolerance * xy_tolerance;

        for (const auto& pt_a : points_a) {
            int cell_x = static_cast<int>(std::floor(pt_a.x / cell_size));
            int cell_y = static_cast<int>(std::floor(pt_a.y / cell_size));

            long long key = (static_cast<long long>(cell_x) * 1000000) + cell_y;

            auto it = grid.find(key);

            if (it != grid.end()) {
                for (const Point3D* pt_b_ptr : it->second) {
                    float dx = pt_a.x - pt_b_ptr->x;
                    float dy = pt_a.y - pt_b_ptr->y;
                    float dist_sq = (dx * dx) + (dy * dy);

                    if (dist_sq <= xy_tol_sq) {
                        float z_diff = std::abs(pt_a.z - pt_b_ptr->z);

                        if(z_diff > z_threshold) {
                            changes.push_back(pt_a);
                            break;
                        }
                    }
                }
            }
        }
        return changes;
    }

int main() {
    
    //1. Define file paths for scan A and Scan B (csvfiles)
    std::string path1 = "/Users/jamescawthray/Desktop/DEV/2026projects/change-detection-engine/Data/p1.csv";
    std::string path2 = "/Users/jamescawthray/Desktop/DEV/2026projects/change-detection-engine/Data/p2.csv";
    //2. call load_points_from_csv on both
    std::vector<Point3D> points_a = load_points_from_csv(path1);
    std::vector<Point3D> points_b = load_points_from_csv(path2);
    //3. print how many points were loaded.
    std::cout << "Loaded " << points_a.size() << " points." << std::endl;
    std::cout << "Loaded " << points_b.size() << " points." << std::endl;
    //4. call find_significant changes.
    float cell_size = 0.1f;
    auto start_time = std::chrono::high_resolution_clock::now();
    auto grid = build_spatial_grid(points_b, cell_size);
    auto changes = find_significant_changes(points_a, grid, 0.002f, 2.0f, cell_size);
    auto end_time = std::chrono::high_resolution_clock::now();
    // calculate the duration in milliseconds
    std::chrono::duration<double, std::milli> duration = end_time - start_time;

    std::cout << "\nDetected changes at these locations:" << std::endl;
    for (size_t i = 0; i < changes.size(); i++) {
        std::cout << "Change " << i+1 << ": X=" << changes[i].x << ", Y=" << changes[i].y << ", Z=" << changes[i].z << std::endl;
    }
    //5. print the count of changes found.
    std::cout << "C++ Engine found " << changes.size() << " significant changes." << std::endl;
    std::cout << "Processing time: " << duration.count() << " milliseconds." << std::endl;

   return 0;
}
