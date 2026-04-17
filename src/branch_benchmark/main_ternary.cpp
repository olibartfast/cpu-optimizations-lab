// Standalone ternary benchmark – use this target for perf/VTune profiling.
// perf stat -e branches,branch-misses ./bench_ternary
// vtune -collect hotspots -- ./bench_ternary

#include "ternary.h"
#include "common.h"

#include <algorithm>
#include <iostream>
#include <random>
#include <vector>

int main() {
    std::mt19937 rng(42);
    std::uniform_int_distribution<int> dist(0, 255);
    std::vector<int> data(N);
    std::generate(data.begin(), data.end(), [&]{ return dist(rng); });

    volatile long sink = solve_ternary(data.data(), (int)data.size());
    std::cout << "ternary checksum=" << sink << "\n";
    return 0;
}
