#include "point_cloud.h"
#include <iostream>
#include <vector>
#include <string>
#include <fstream>
#include <cmath>
#include <limits>
#include <sstream>
#include <chrono>
#include <unordered_map>

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
std::vector<Point3D> find_significant_changes_fast(
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

    std::vector<Point3D> detect_changes(
    const std::vector<Point3D>& points_a,
    const std::vector<Point3D>& points_b,
    float xy_tolerance,
    float z_threshold,
    float cell_size)
{
    // Build the grid internally
    auto grid = build_spatial_grid(points_b, cell_size);
    
    // Run the search
    return find_significant_changes_fast(points_a, grid, xy_tolerance, z_threshold, cell_size);
}
