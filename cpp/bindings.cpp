#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "point_cloud.h"

namespace py = pybind11;

PYBIND11_MODULE(change_detection, m) {
    m.doc() = "High-performance LiDAR change detection engine";
    
    // Expose Point3D struct
    py::class_<Point3D>(m, "Point3D")
        .def(py::init<>())
        .def_readwrite("x", &Point3D::x)
        .def_readwrite("y", &Point3D::y)
        .def_readwrite("z", &Point3D::z);
    
    // Expose simple functions
    m.def("load_points_from_csv", &load_points_from_csv,
          "Load points from a CSV file",
          py::arg("file_path"));
    
    // Expose the wrapper function (not the grid-based one)
    m.def("detect_changes", &detect_changes,
          "Detect significant changes between two point clouds",
          py::arg("points_a"),
          py::arg("points_b"),
          py::arg("xy_tolerance"),
          py::arg("z_threshold"),
          py::arg("cell_size"));
}
