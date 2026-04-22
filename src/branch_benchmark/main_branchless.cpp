// Standalone branchless benchmark – use this target for perf/VTune profiling.
// perf stat -e branches,branch-misses ./bench_branchless
// vtune -collect hotspots -- ./bench_branchless

#include "branchless.h"
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

    volatile long sink = solve_branchless(data.data(), (int)data.size());
    bool ok = (sink == EXPECTED_CHECKSUM);
    std::cout << "branchless checksum=" << sink
              << "  [" << (ok ? "PASS" : "FAIL") << "]\n";
    return ok ? 0 : 1;
}
