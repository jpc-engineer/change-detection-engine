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
        /*
        1. Iterate through every point in points_a
        2. for each point in A, find the closest point in points_b (based on x_y distance)
        3. If the x,y distance is <= xy_tolerance, calculate the z difference
        4. If the Z difference is > z_threshold, add this point to our results vector
        5. return the results vector
        */
       return {};
    }

int main() {
    
    //1. Define file paths for scan A and Scan B (csvfiles)
    std::string path1 = "/Users/jamescawthray/Desktop/DEV/2026projects/change-detection-engine/Data/p1.csv";
    std::string path2 = "/Users/jamescawthray/Desktop/DEV/2026projects/change-detection-engine/Data/p2.csv";
    //2. call load_points_from_csv on both
    std::vector<Point3D> points = load_points_from_csv(path1);
    std::cout << "Loaded " << points.size() << " points." << std::endl;
    //3. print how many points were loaded.
    //4. call find_significant changes.
    //5. print the count of changes found.
    
   return 0;
}
