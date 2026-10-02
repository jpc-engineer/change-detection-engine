#include <iostream>
#include <vector>
#include <string>
#include <fstream>
#include <cmath>
#include <limits>
#include <sstream>

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

// 3. Core algorithm (like matching points in load.py)
std::vector<Point3D> find_significant_changes(
    const std::vector<Point3D>& points_a,
    const std::vector<Point3D>& points_b,
    float xy_tolerance,
    float z_threshold) {

        std::vector<Point3D> changes;
        float xy_square_tol = xy_tolerance * xy_tolerance;

        //1. Look at each point in scan A one by one.
        for (const auto& pt_a : points_a) {
            // 2. inner loop setup: before searching B, reset our 'best match' trackers
            float min_dist_sq = std::numeric_limits<float>::max(); // start with infinity
            float best_match_z = 0.0f;

            // 3. INNER LOOP: search all points in scan B to find the closest one to pt_a
            for (const auto& pt_b : points_b) {
                float dx = pt_a.x - pt_b.x;
                float dy = pt_a.y - pt_b.y;
                float dist_sq = (dx * dx) + (dy * dy); // squared distance

                // if this point in B is closer than any we've seen so far, remember it.
                if (dist_sq < min_dist_sq) {
                    min_dist_sq = dist_sq;
                    best_match_z = pt_b.z;
                }
            }

            // 4. POST INNER LOOP: we have now checked every point in B
            // did we find a match that is horizontally close enough?
            if (min_dist_sq <= xy_square_tol) {
                // 5. check if the Z difference is significant
                float z_diff = std::abs(pt_a.z - best_match_z);

                if (z_diff > z_threshold) {
                    // 6. Its a match AND a significant change. save it.
                    changes.push_back(pt_a);
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
    //4. call find_significant changes.
    auto changes = find_significant_changes(points_a, points_b, 0.5f, 2.0f);
    //5. print the count of changes found.
    std::cout << "C++ Engine found " << changes.size() << " significant changes." << std::endl;
   return 0;
}
