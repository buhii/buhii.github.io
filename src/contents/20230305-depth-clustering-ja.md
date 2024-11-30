## 点群クラスタリング手法の C++ から Python への移植

去年の夏から 3D LiDAR のプロジェクトに携わっており、主にセンサーデータの取り込みや物体検出・追跡アルゴリズムの実装を行った。物体検出では高速・軽量な点群クラスタリング手法である [Depth Clustering](https://github.com/PRBonn/depth_clustering) を利用した。動作環境などの都合上、その際に C++ のオリジナル実装から Python に [Numba](https://numba.pydata.org/) を利用して移植した。GitHub でも公開した:
- [github.com/uchiyamalab/depth_clustering_py](https://github.com/uchiyamalab/depth_clustering_py)

Numba では LLVM による SIMD 最適化などもしてくれるみたいなので、そのうちベンチマークなども取ってみようと思う。
