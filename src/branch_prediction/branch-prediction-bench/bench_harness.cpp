#include "bench_harness.h"
#include "common.h"

#include <algorithm>
#include <chrono>
#include <iomanip>
#include <iostream>
#include <vector>

using Clock  = std::chrono::high_resolution_clock;
using Micros = std::chrono::duration<double, std::micro>;

BenchResult bench(const std::string& name, BenchFn fn,
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

void print_table(const std::vector<BenchResult>& results) {
    const double baseline = results[0].median_us;

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
