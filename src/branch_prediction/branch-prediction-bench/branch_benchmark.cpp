// g++ -O0 -std=c++17 -o bench_O0 branch_benchmark.cpp && ./bench_O0

// g++ -O2 -std=c++17 -o bench_O2 branch_benchmark.cpp && ./bench_O2

// g++ -O3 -mavx2 -std=c++17 -o bench_O3 branch_benchmark.cpp && ./bench_O3

#include <algorithm>
#include <chrono>
#include <iomanip>
#include <iostream>
#include <numeric>
#include <random>
#include <string>
#include <vector>

static constexpr int N       = 100'000;
static constexpr int REPEATS = 100;
static constexpr int RUNS    = 7;

// ─── implementations ──────────────────────────────────────────────────────────

// 1. Naive – unsorted, unpredictable branch
long solve_naive(const int* arr, int n) {
    long total = 0;
    for (int r = 0; r < REPEATS; r++)
        for (int i = 0; i < n; i++)
            if (arr[i] > 128)
                total += arr[i];
    return total;
}

// 2. Sorted – branch transitions exactly once (false…false…true…true)
long solve_sorted(int* arr, int n) {
    std::sort(arr, arr + n);
    long total = 0;
    for (int r = 0; r < REPEATS; r++)
        for (int i = 0; i < n; i++)
            if (arr[i] > 128)
                total += arr[i];
    return total;
}

// 3. Branchless – multiply by boolean (compiler emits cmov/setg, no jump)
long solve_branchless(const int* arr, int n) {
    long total = 0;
    for (int r = 0; r < REPEATS; r++)
        for (int i = 0; i < n; i++) {
            int val = arr[i];
            total += val * (val > 128);
        }
    return total;
}

// 4. Ternary – idiomatic form, best auto-vectorisation hint for -O2 -mavx2
long solve_ternary(const int* arr, int n) {
    long total = 0;
    for (int r = 0; r < REPEATS; r++)
        for (int i = 0; i < n; i++) {
            int val = arr[i];
            total += (val > 128) ? val : 0;
        }
    return total;
}

// ─── bench harness ────────────────────────────────────────────────────────────
using Clock  = std::chrono::high_resolution_clock;
using Micros = std::chrono::duration<double, std::micro>;

struct BenchResult {
    std::string name;
    double      median_us;
    long        checksum;
};

using Fn = long (*)(int*, int);

BenchResult bench(const std::string& name, Fn fn,
                  const std::vector<int>& original) {
    std::vector<double> times;
    times.reserve(RUNS);
    long chk = 0;
    for (int run = 0; run < RUNS; run++) {
        std::vector<int> data = original;
        auto t0 = Clock::now();
        chk = fn(data.data(), (int)data.size());
        auto t1 = Clock::now();
        times.push_back(Micros(t1 - t0).count());
    }
    std::sort(times.begin(), times.end());
    return {name, times[RUNS / 2], chk};
}

// ─── pretty printer ───────────────────────────────────────────────────────────
void print_table(const std::vector<BenchResult>& results) {
    const double baseline  = results[0].median_us;
    const double best_time = results.back().median_us; // last tends to be fastest

    // find actual best for bar scaling
    double fastest = baseline;
    for (auto& r : results) fastest = std::min(fastest, r.median_us);

    const int W1 = 26, W2 = 14, W3 = 10, BARW = 30;
    std::string SEP(W1 + W2 + W3 + BARW + 6, '-');

    std::cout << "\n" << SEP << "\n";
    std::cout << std::left
              << std::setw(W1) << "  Implementation"
              << std::setw(W2) << "  Median µs"
              << std::setw(W3) << "  Speedup"
              << "  Bar\n"
              << SEP << "\n";

    for (auto& r : results) {
        double speedup = baseline / r.median_us;
        int    blen    = std::max(1, (int)(BARW * (fastest / r.median_us)));
        blen = std::min(blen, BARW);

        std::cout << std::left
                  << "  " << std::setw(W1 - 2) << r.name
                  << "  " << std::setw(W2 - 2)
                           << std::fixed << std::setprecision(1) << r.median_us
                  << "  " << std::setw(W3 - 2)
                           << std::fixed << std::setprecision(2) << speedup << "x"
                  << "  " << std::string(blen, '|') << "\n";
    }
    std::cout << SEP << "\n\n";
}

// ─── main ─────────────────────────────────────────────────────────────────────
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