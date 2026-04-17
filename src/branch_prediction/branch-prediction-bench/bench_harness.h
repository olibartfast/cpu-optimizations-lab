#pragma once

#include <string>
#include <vector>

struct BenchResult {
    std::string name;
    double      median_us;
    long        checksum;
};

// fn signature allows mutable array (needed by solve_sorted)
using BenchFn = long (*)(int*, int);

BenchResult bench(const std::string& name, BenchFn fn,
                  const std::vector<int>& original);

void print_table(const std::vector<BenchResult>& results);
