## Porting Point Cloud Clustering from C++ to Python

Since last summer, I have been working on a 3D LiDAR project that involves implementing sensor data acquisition, object detection, and tracking algorithms. For object detection, I used [Depth Clustering](https://github.com/PRBonn/depth_clustering), a fast and lightweight point cloud clustering algorithm. Due to the constraints of the environments where I needed to run, I ported the algorithm from the original C++ version to Python using [Numba](https://numba.pydata.org/). I have also published the project to GitHub:
- [github.com/uchiyamalab/depth_clustering_py](https://github.com/uchiyamalab/depth_clustering_py)

Numba does SIMD optimization with LLVM, so I will try to get some benchmarks in the future.
