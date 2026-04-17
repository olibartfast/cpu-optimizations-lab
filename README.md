# CPU Optimizations Lab

A hands-on curriculum for learning CPU-level performance optimization through progressive C++17 exercises. Labs cover cache behavior, branch prediction, SIMD vectorization, and data structure design — each built and benchmarked at multiple optimization levels.

## Prerequisites

**Required:**
- C++17 compiler (GCC/Clang)
- CMake 3.15+
- Basic understanding of computer architecture

**Recommended:**
- Assembly reading skills
- Experience with profiling tools (perf, VTune, etc.)
- Understanding of cache hierarchies

## Repository Structure

```
cpu-optimizations-lab/
├── src/
│   ├── branch_prediction/          # ✅ Branch prediction lab (one folder per project)
│   │   ├── branch-prediction-bench/    # naive → sorted → branchless → ternary
│   │   └── <other-projects>/           # additional branch prediction projects
│   ├── cache_optimization/         # (planned)
│   ├── simd_basics/                # (planned)
│   ├── memory_bound_optimizations/ # (planned)
│   ├── data_structures_for_performance/ # (planned)
│   ├── highway_simd_library/       # (planned)
│   ├── advanced_vectorization/     # (planned)
│   └── real_world_scenarios/       # (planned)
└── mcp-server/                     # Python MCP server for RAG-based learning assistance
    ├── server.py                   # 5 MCP tools via Continue.dev
    └── knowledge_base.py           # Static learning resource catalog
```

## Getting Started

### Install Dependencies (Linux)

```bash
sudo apt-get install cmake build-essential
```

### Build a Project

Each project has its own directory under `src/<lab>/` with a CMakeLists.txt:

```bash
cd src/<lab>/<project-name>
mkdir build && cd build
cmake ..
make -j$(nproc)
```

Each project's README documents the binaries it produces and how to run them.

**Currently implemented:**

- [src/branch_prediction/branch-prediction-bench/](src/branch_prediction/branch-prediction-bench/README.md) — naive → sorted → branchless → ternary, benchmarked at O0/O2/O3

## Lab Overview

### Branch Prediction: `branch-prediction-bench`

Threshold query on 100K integers, 100 passes. Eliminate branch misprediction by preprocessing the array once before the repeated scans.

See [src/branch_prediction/branch-prediction-bench/README.md](src/branch_prediction/branch-prediction-bench/README.md) for problem statement, constraints, targets, and measured results.

| # | Lab | Status | Focus |
|---|-----|--------|-------|
| 1 | Branch Prediction | ✅ Implemented | Threshold query on random array: sort to eliminate branch misprediction |
| 2 | Cache Optimization | Planned | Cache-friendly data structures and access patterns |
| 3 | SIMD Basics | Planned | Introduction to vectorization |
| 4 | Memory Bound Optimizations | Planned | Memory bandwidth optimization |
| 5 | Data Structures for Performance | Planned | SoA layouts and cache-friendly design |
| 6 | Highway SIMD Library | Planned | Portable SIMD with [Google Highway](https://github.com/google/highway) |
| 7 | Advanced Vectorization | Planned | Complex SIMD patterns |
| 8 | Real-World Scenarios | Planned | Complete optimization projects |

### Speedup Targets (per lab)

- ⭐ Basic: 2× speedup
- ⭐⭐ Good: 5× speedup
- ⭐⭐⭐ Excellent: 10×+ speedup

## MCP Learning Assistant

An optional Python MCP server provides RAG-based answers about CPU optimization topics via [Continue.dev](https://continue.dev/):

```bash
cd mcp-server
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python server.py
```

Available tools: `search_optimization_topics`, `get_learning_path`, `get_lab_info`, `get_profiling_tools`, `get_all_resources`.

> ⚠️ The Continue.dev config in `.continuerc.json` uses a hardcoded path `/workspaces/cpu-optimizations-lab/`. Update it if you've cloned the repo elsewhere.

## Profiling Tools

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

**Windows:** Intel VTune Profiler, Visual Studio Profiler, AMD μProf  
**macOS:** Instruments (Xcode)

## Learning Resources

### Books
- *Performance Analysis and Tuning on Modern CPUs* — Denis Bakhvalov
- *Computer Architecture: A Quantitative Approach* — Hennessy & Patterson
- *Agner Fog's Optimization Manuals* — [free online](https://www.agner.org/optimize/)

### Online Resources
- [Algorithms for Modern Hardware](https://en.algorithmica.org/hpc/)
- [Intel Intrinsics Guide](https://www.intel.com/content/www/us/en/docs/intrinsics-guide/)
- [Compiler Explorer](https://godbolt.org/) — view assembly output
- [SIMD for C++ Developers](http://const.me/articles/simd/simd.pdf)

### Related Projects
- [perf-ninja](https://github.com/dendibakh/perf-ninja) — performance optimization course
- [Google Highway](https://github.com/google/highway) — portable SIMD library
- [EVE](https://github.com/jfalcou/eve) — Expressive Vector Engine
