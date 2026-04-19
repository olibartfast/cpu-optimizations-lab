"""Knowledge base of CPU optimization resources"""

LEARNING_RESOURCES = {
    "books": [
        {
            "id": "perf-analysis-tuning",
            "title": "Performance Analysis and Tuning on Modern CPUs",
            "author": "Denis Bakhvalov",
            "url": "https://github.com/dendibakh/perf-book",
            "level": "intermediate",
            "topics": ["performance analysis", "cpu tuning", "profiling", "optimization"],
            "description": "Comprehensive guide to analyzing and tuning performance on modern CPUs"
        },
        {
            "id": "comp-arch-quantitative",
            "title": "Computer Architecture: A Quantitative Approach",
            "author": "Hennessy & Patterson",
            "url": "https://www.elsevier.com/books/computer-architecture/hennessy/978-0-12-811905-1",
            "level": "advanced",
            "topics": ["computer architecture", "cpu design", "performance modeling"],
            "description": "Classic text on computer architecture principles and quantitative analysis"
        },
        {
            "id": "agner-fog-manuals",
            "title": "Agner Fog's Optimization Manuals",
            "author": "Agner Fog",
            "url": "https://www.agner.org/optimize/",
            "level": "advanced",
            "topics": ["optimization", "assembly", "microarchitecture", "instruction timing"],
            "description": "Free comprehensive manuals covering low-level optimization techniques"
        }
    ],
    "onlineResources": [
        {
            "id": "simd-cpp",
            "title": "SIMD for C++ Developers",
            "url": "http://const.me/articles/simd/simd.pdf",
            "topics": ["simd", "vectorization", "c++", "intrinsics"],
            "description": "Practical guide to SIMD programming in C++"
        },
        {
            "id": "algorithms-modern-hw",
            "title": "Algorithms for Modern Hardware",
            "url": "https://en.algorithmica.org/hpc/",
            "topics": ["algorithms", "performance", "modern hardware", "cache optimization"],
            "description": "Online book covering algorithm design for modern hardware"
        },
        {
            "id": "intel-intrinsics",
            "title": "Intel Intrinsics Guide",
            "url": "https://www.intel.com/content/www/us/en/docs/intrinsics-guide/",
            "topics": ["simd", "intrinsics", "intel", "x86"],
            "description": "Complete reference for Intel SIMD intrinsics"
        },
        {
            "id": "compiler-explorer",
            "title": "Compiler Explorer",
            "url": "https://godbolt.org/",
            "topics": ["compiler", "assembly", "optimization", "code generation"],
            "description": "Online tool to view assembly output from various compilers"
        }
    ],
    "projects": [
        {
            "id": "perf-ninja",
            "title": "perf-ninja",
            "url": "https://github.com/dendibakh/perf-ninja",
            "topics": ["performance", "optimization", "course", "exercises"],
            "description": "Performance optimization course with hands-on exercises"
        },
        {
            "id": "google-highway",
            "title": "Google Highway",
            "url": "https://github.com/google/highway",
            "topics": ["simd", "vectorization", "portable", "library"],
            "description": "Portable SIMD library for cross-platform vectorization"
        },
        {
            "id": "eve",
            "title": "EVE - Expressive Vector Engine",
            "url": "https://github.com/jfalcou/eve",
            "topics": ["simd", "vectorization", "c++", "modern"],
            "description": "Modern C++ SIMD library with expressive API"
        }
    ],
    "labs": [
        {
            "id": "lab-01",
            "title": "Cache Optimization",
            "duration": "1-2 hours",
            "topics": ["cache", "memory access patterns", "cache-oblivious algorithms"],
            "description": "Learn to identify and fix cache misses, optimize array traversal",
            "level": "beginner",
            "speedupTargets": {"basic": "2x", "good": "5x", "excellent": "10x+"}
        },
        {
            "id": "lab-02",
            "title": "Branch Prediction",
            "duration": "1-2 hours",
            "topics": ["branch prediction", "branchless programming", "cmov", "lookup tables"],
            "description": "Eliminate branch mispredictions using various techniques",
            "level": "beginner",
            "speedupTargets": {"basic": "2x", "good": "5x", "excellent": "10x+"}
        },
        {
            "id": "lab-03",
            "title": "SIMD Basics",
            "duration": "2-3 hours",
            "topics": ["simd", "vectorization", "intrinsics"],
            "description": "Learn fundamentals of SIMD programming with portable intrinsics",
            "level": "beginner",
            "speedupTargets": {"basic": "2x", "good": "5x", "excellent": "10x+"}
        },
        {
            "id": "lab-04",
            "title": "Memory Bound Optimizations",
            "duration": "2-3 hours",
            "topics": ["memory bandwidth", "prefetching", "streaming", "data layout"],
            "description": "Optimize for memory-bound workloads",
            "level": "intermediate",
            "speedupTargets": {"basic": "2x", "good": "5x", "excellent": "10x+"}
        },
        {
            "id": "lab-05",
            "title": "Data Structures for Performance",
            "duration": "2-3 hours",
            "topics": ["data structures", "SoA", "AoS", "cache-friendly layouts"],
            "description": "Design data structures optimized for modern CPU architectures",
            "level": "intermediate",
            "speedupTargets": {"basic": "2x", "good": "5x", "excellent": "10x+"}
        },
        {
            "id": "lab-06",
            "title": "Highway SIMD Library",
            "duration": "3-4 hours",
            "topics": ["highway", "simd", "portable simd", "cross-platform"],
            "description": "Implement algorithms using Highway library for cross-platform vectorization",
            "level": "intermediate",
            "speedupTargets": {"basic": "2x", "good": "5x", "excellent": "10x+"}
        },
        {
            "id": "lab-07",
            "title": "Advanced Vectorization",
            "duration": "3-4 hours",
            "topics": ["gather", "scatter", "masked operations", "horizontal reductions"],
            "description": "Master complex SIMD patterns",
            "level": "advanced",
            "speedupTargets": {"basic": "2x", "good": "5x", "excellent": "10x+"}
        },
        {
            "id": "lab-08",
            "title": "Real-World Scenarios",
            "duration": "4+ hours",
            "topics": ["real-world optimization", "complete projects"],
            "description": "Apply all learned techniques to realistic performance problems",
            "level": "advanced",
            "speedupTargets": {"basic": "2x", "good": "5x", "excellent": "10x+"}
        }
    ],
    "tools": {
        "linux": [
            {"name": "perf", "usage": "perf stat -e cycles,instructions,cache-misses,branch-misses ./program", "description": "CPU performance counters"},
            {"name": "perf record/report", "usage": "perf record -g ./program && perf report", "description": "Detailed profiling with call graphs"},
            {"name": "valgrind cachegrind", "usage": "valgrind --tool=cachegrind ./program", "description": "Cache simulation and analysis"}
        ],
        "windows": [
            {"name": "Intel VTune Profiler", "description": "Comprehensive performance analysis"},
            {"name": "Visual Studio Profiler", "description": "Built-in VS profiling tools"},
            {"name": "AMD μProf", "description": "AMD CPU profiler"}
        ],
        "macos": [
            {"name": "Instruments", "description": "Xcode profiling tools"}
        ]
    }
}
