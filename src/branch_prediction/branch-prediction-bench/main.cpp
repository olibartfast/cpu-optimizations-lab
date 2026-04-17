// Combined benchmark – all four implementations in one run.
// Build:
//   g++ -O0 -std=c++17 -o bench_all_O0 main.cpp naive.cpp sorted.cpp branchless.cpp ternary.cpp bench_harness.cpp
//   g++ -O3 -mavx2 -std=c++17 -o bench_all_O3 main.cpp naive.cpp sorted.cpp branchless.cpp ternary.cpp bench_harness.cpp

#include "bench_harness.h"
#include "branchless.h"
#include "common.h"
#include "naive.h"
#include "sorted.h"
#include "ternary.h"

#include <algorithm>
#include <iostream>
#include <random>
#include <vector>

int main() {
    std::mt19937 rng(42);
    std::uniform_int_distribution<int> dist(0, 255);
    std::vector<int> data(N);
    std::generate(data.begin(), data.end(), [&]{ return dist(rng); });

    std::cout << "\n";
    std::cout << "  Branch Prediction Benchmark\n";
    std::cout << "  N=" << N << "  REPEATS=" << REPEATS
              << "  RUNS(median)=" << RUNS << "\n";
    std::cout << "  Random ints in [0, 255]\n";

    std::vector<BenchResult> results;

    results.push_back(bench("Naive (unsorted branch)",
        [](int* a, int n){ return solve_naive(a, n); }, data));

    results.push_back(bench("Sorted (1 transition)",
        [](int* a, int n){ return solve_sorted(a, n); }, data));

    results.push_back(bench("Branchless val*(val>128)",
        [](int* a, int n){ return solve_branchless(a, n); }, data));

    results.push_back(bench("Ternary (auto-vec hint)",
        [](int* a, int n){ return solve_ternary(a, n); }, data));

    print_table(results);

    bool ok = true;
    for (size_t i = 1; i < results.size(); i++)
        if (results[i].checksum != results[0].checksum) ok = false;

    std::cout << "  Checksum: " << results[0].checksum
              << "  [" << (ok ? "PASS" : "FAIL - mismatch!") << "]\n\n";
    return ok ? 0 : 1;
}
