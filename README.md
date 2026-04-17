# CPU Optimization Lab

A comprehensive hands-on lab for learning CPU-level performance optimization techniques through practical exercises. This lab combines low-level performance tuning with modern SIMD programming.

## 🎯 Learning Objectives

Master practical CPU optimization techniques including:
- Cache optimization and memory access patterns
- Branch prediction and control flow optimization
- SIMD vectorization using portable libraries
- Data structure design for performance
- Compiler optimization understanding
- Performance measurement and profiling

## 📚 Prerequisites

**Required:**
- C++ (C++17 or higher)
- Basic understanding of computer architecture
- Familiarity with compilers (GCC/Clang/MSVC)

**Recommended:**
- Assembly reading skills
- Experience with profiling tools (perf, VTune, etc.)
- Understanding of cache hierarchies

## 🏗️ Repository Structure

```
cpu-optimization-lab/
├── labs/
│   ├── cache-optimization/      # Cache-friendly algorithms
│   ├── branch-prediction/       # Control flow optimization
│   ├── simd-basics/             # Introduction to SIMD
│   ├── memory-bound/            # Memory bandwidth optimization
│   ├── data-structures/         # Performance-oriented data structures
│   ├── highway-simd/            # Highway library exercises
│   ├── advanced-vectorization/  # Complex SIMD patterns
│   └── real-world/              # Real-world optimization scenarios
├── tools/
│   ├── benchmark/                  # Benchmarking utilities
│   └── profiling/                  # Profiling helpers
├── references/
│   └── quick-reference.md          # Quick reference guide
└── solutions/                      # Reference solutions (separate branch)
```

## 🚀 Getting Started

### Installation

#### Linux/macOS
```bash
# Install dependencies
sudo apt-get install cmake build-essential libgtest-dev

# Clone the repository
git clone https://github.com/yourusername/cpu-optimization-lab.git
cd cpu-optimization-lab

# Build all labs
mkdir build && cd build
cmake ..
make -j$(nproc)

# Run tests
ctest
```

#### Windows
```powershell
# Install dependencies (using vcpkg)
vcpkg install gtest

# Clone and build
git clone https://github.com/yourusername/cpu-optimization-lab.git
cd cpu-optimization-lab
mkdir build
cd build
cmake ..
cmake --build . --config Release
```

### Running Your First Lab

```bash
cd labs/01-cache-optimization
mkdir build && cd build
cmake ..
make
./benchmark_baseline
```

## 📖 Lab Overview

### Cache Optimization
**Focus:** Cache-friendly data structures and access patterns

### Branch Prediction
**Focus:** Branch misprediction elimination

### SIMD Basics
**Focus:** Introduction to vectorization

### Memory Bound Optimizations
**Focus:** Memory bandwidth optimization

### Data Structures for Performance
**Focus:** Structure-of-Arrays and cache-friendly layouts

### Highway SIMD Library
**Focus:** Portable SIMD with Google Highway

### Advanced Vectorization
**Focus:** Complex SIMD patterns

### Real-World Scenarios
**Focus:** Complete optimization projects

## 🎓 How to Use This Lab

Each lab follows a consistent structure:

1. **README.md** - Lab overview and learning objectives
2. **baseline/** - Unoptimized starting code
3. **benchmark.cpp** - Performance measurement harness
4. **tests/** - Unit tests to verify correctness
5. **hints.md** - Optimization hints (optional)

### Workflow

1. Read the lab README to understand the problem
2. Run the baseline benchmark to establish performance
3. Profile the code to identify bottlenecks
4. Implement optimizations
5. Verify correctness with unit tests
6. Measure performance improvements
7. Compare with reference solutions (on solutions branch)

### Measuring Success

Each lab has target speedup goals:
- ⭐ Basic: 2x speedup
- ⭐⭐ Good: 5x speedup  
- ⭐⭐⭐ Excellent: 10x+ speedup

## 🛠️ Tools and Profiling

### Recommended Profiling Tools

**Linux:**
```bash
# perf - CPU performance counters
perf stat -e cycles,instructions,cache-misses,branch-misses ./your_program

# perf record/report - detailed profiling
perf record -g ./your_program
perf report

# valgrind - cache simulation
valgrind --tool=cachegrind ./your_program
```

**Windows:**
- Intel VTune Profiler
- Visual Studio Profiler
- AMD μProf

**macOS:**
- Instruments (Xcode)

### Benchmarking Best Practices

```cpp
// Use Google Benchmark or similar
#include <benchmark/benchmark.h>

static void BM_YourFunction(benchmark::State& state) {
    // Setup
    std::vector<int> data = GenerateTestData();
    
    for (auto _ : state) {
        // Code to benchmark
        YourFunction(data);
        
        // Prevent optimization
        benchmark::DoNotOptimize(data);
        benchmark::ClobberMemory();
    }
}
BENCHMARK(BM_YourFunction);
```

## 📚 Learning Resources

### Books
- "Performance Analysis and Tuning on Modern CPUs" by Denis Bakhvalov
- "Computer Architecture: A Quantitative Approach" by Hennessy & Patterson
- "Agner Fog's Optimization Manuals" (free online)

### Online Resources
- [SIMD for C++ Developers](http://const.me/articles/simd/simd.pdf)
- [Algorithms for Modern Hardware](https://en.algorithmica.org/hpc/)
- [Intel Intrinsics Guide](https://www.intel.com/content/www/us/en/docs/intrinsics-guide/)
- [Compiler Explorer](https://godbolt.org/) - View assembly output
- [LeetCPU] - https://www.leetcpu.com/

### Related Projects
- [perf-ninja](https://github.com/dendibakh/perf-ninja) - Performance optimization course
- [Google Highway](https://github.com/google/highway) - Portable SIMD library
- [EVE](https://github.com/jfalcou/eve) - Expressive Vector Engine

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

Areas where contributions are especially welcome:
- New lab assignments
- Additional architecture support
- Improved documentation
- Bug fixes and optimizations

## 📝 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) for details.

Portions inspired by:
- perf-ninja (CC BY 4.0) by Denis Bakhvalov
- Google Highway (Apache 2.0 / BSD-3)
- EVE (Boost Software License)

## 🙏 Acknowledgments

This lab draws inspiration from:
- The perf-ninja project and its educational approach
- Google Highway's portable SIMD abstraction
- EVE's modern C++ design patterns
- The broader performance engineering community

## 📧 Contact

- Issues: [GitHub Issues](https://github.com/yourusername/cpu-optimization-lab/issues)
- Discussions: [GitHub Discussions](https://github.com/yourusername/cpu-optimization-lab/discussions)

## 🎯 Learning Path

**Beginner** (Start here if new to optimization):
- Lab 1: Cache Optimization
- Lab 2: Branch Prediction
- Lab 3: SIMD Basics

**Intermediate** (Some optimization experience):
- Lab 4: Memory Bound
- Lab 5: Data Structures
- Lab 6: Highway SIMD

**Advanced** (Experienced with performance work):
- Lab 7: Advanced Vectorization
- Lab 8: Real-World Scenarios

Happy optimizing! 🚀
