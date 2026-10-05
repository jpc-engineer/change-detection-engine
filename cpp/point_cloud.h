#ifndef POINT_CLOUD_H
#define POINT_CLOUD_H

#include <vector>
#include <string>
#include <unordered_map>

struct Point3D {
    float x;
    float y;
    float z;
};

// Function declarations
__attribute__((visibility("default"))) std::vector<Point3D> load_points_from_csv(const std::string& file_path);

__attribute__((visibility("default"))) std::unordered_map<long long, std::vector<const Point3D*>> build_spatial_grid(
    const std::vector<Point3D>& points_b, float cell_size);

__attribute__((visibility("default"))) std::vector<Point3D> find_significant_changes_fast(
    const std::vector<Point3D>& points_a,
    const std::unordered_map<long long, std::vector<const Point3D*>>& grid,
    float xy_tolerance,
    float z_threshold,
    float cell_size);

__attribute__((visibility("default"))) std::vector<Point3D> detect_changes(
    const std::vector<Point3D>& points_a,
    const std::vector<Point3D>& points_b,
    float xy_tolerance,
    float z_threshold,
    float cell_size);

#endif
