cmake_minimum_required(VERSION 3.15)
project(change_detection)

# 1. Force C++17
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# 2. MACOS FIXES: Force symbols to be visible and disable aggressive stripping
set(CMAKE_CXX_VISIBILITY_PRESET default)
set(CMAKE_VISIBILITY_INLINES_HIDDEN OFF)
set(CMAKE_INTERPROCEDURAL_OPTIMIZATION OFF) # This disables -flto

# 3. Find pybind11
find_package(pybind11 REQUIRED)

# 4. Add C++ source files
pybind11_add_module(change_detection
    cpp/point_cloud.cpp
    cpp/bindings.cpp
)

# 5. Include directories
target_include_directories(change_detection PRIVATE cpp)
