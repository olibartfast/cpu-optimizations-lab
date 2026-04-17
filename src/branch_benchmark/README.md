# Branch Prediction Benchmark

Demonstrates the performance impact of branch mispredictions and how to eliminate them.
Four implementations of the same summation kernel are compared side-by-side.

## Implementations

| File | Strategy |
|---|---|
| `naive.cpp` | Unsorted array — branch outcome is unpredictable per element |
| `sorted.cpp` | Sorted array — branch changes exactly once (all-false then all-true) |
| `branchless.cpp` | `val * (val > 128)` — integer multiply eliminates the jump |
| `ternary.cpp` | `(val > 128) ? val : 0` — idiomatic form, best SIMD auto-vec hint |

## Build

```bash
mkdir build && cd build
cmake ..
make -j$(nproc)
```

All binaries are written to `build/`. The `build/` directory is git-ignored.

CMake flags used per optimization level:

| Suffix | Flags |
|---|---|
| `_O0` | `-O0 -g` |
| `_O2` | `-O2 -g` |
| `_O3` | `-O3 -mavx2 -g` |

## Binaries

| Binary | Purpose |
|---|---|
| `bench_all_{O0,O2,O3}` | All four implementations in one run, with a timing table |
| `bench_naive_{O0,O2,O3}` | Standalone naive — for perf / VTune isolation |
| `bench_sorted_{O0,O2,O3}` | Standalone sorted |
| `bench_branchless_{O0,O2,O3}` | Standalone branchless |
| `bench_ternary_{O0,O2,O3}` | Standalone ternary |

The standalone binaries use `volatile long sink` to prevent dead-code elimination at `-O3`.

## Profiling

### perf (Linux)

```bash
# branch miss summary
perf stat -e branches,branch-misses,cycles,instructions \
    ./build/bench_naive_O0

# compare naive vs branchless
perf stat -e branch-misses ./build/bench_naive_O0
perf stat -e branch-misses ./build/bench_branchless_O0

# flame graph / annotated source
perf record -g ./build/bench_naive_O0
perf report
```

### Intel VTune

```bash
# hotspot analysis
vtune -collect hotspots -knob sampling-mode=hw -- ./build/bench_naive_O0

# memory access analysis
vtune -collect memory-access -- ./build/bench_branchless_O3

# micro-architecture exploration (branch misprediction detail)
vtune -collect uarch-exploration -- ./build/bench_naive_O3
```

> **Tip:** Always profile the `_O0` binary to see the branch-heavy baseline and the `_O3` binary to confirm the compiler eliminated branches in the branchless/ternary variants.

## Expected Results

On a typical x86-64 CPU with `N=100000`, `REPEATS=100`:

- **Naive** — high `branch-misses` (~50 % of branches for random data)
- **Sorted** — near-zero misses once the branch transitions at index ~50 %
- **Branchless / Ternary** — near-zero misses; compiler emits `cmov` / SIMD at `-O2+`
