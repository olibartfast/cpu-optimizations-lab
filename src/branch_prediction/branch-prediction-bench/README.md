# Branch Prediction Benchmark

## Problem

Answer the same threshold query (`arr[i] > 128`) 100 times on an array of 100,000 integers.

The baseline scans a random-order array. Because the branch is nearly 50/50 on random data, the branch predictor mispredicts on ~half the elements.

**Task:** Implement `long solve(int *arr, int n)` that returns the total sum of all values > 128 across 100 full passes. You may preprocess the array **once** before the repeated scans begin. All original values must be preserved and the output must match the reference sum exactly.

**Hint:** A stable partition — all values ≤ 128 first, then all values > 128 — turns a nearly random branch into two long predictable runs.

**Constraints:**
- One up-front preprocessing step allowed; no SIMD intrinsics; no multithreading
- Output must equal the reference total across all 100 passes

**Targets:**

| Metric | Target |
|--------|--------|
| Branch MPKI | < 1.5 |
| IPC | > 2.6 |

---

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

### Key metrics

**IPC (Instructions Per Cycle)** — how many instructions retire each clock tick. Higher = better. Mispredictions drain the pipeline and lower IPC.

$$\text{IPC} = \frac{\text{instructions}}{\text{cycles}}$$

**MPKI (Misses Per Kilo-Instructions)** — branch mispredictions normalized by instruction count, so results are comparable across implementations that do different amounts of work. Lower = better. Each misprediction costs ~15–20 wasted cycles on a modern out-of-order CPU.

$$\text{MPKI} = \frac{\text{branch-misses} \times 1000}{\text{instructions}}$$

### Measured results (`perf stat`, x86-64)

| Implementation | Opt | Cycles | IPC | Branch Miss% | MPKI |
|----------------|-----|-------:|----:|-------------:|-----:|
| naive | O0 | 263M | 0.73 | 21.0% | 26.9 |
| naive | O3 | 16.5M | 1.76 | 2.2% | 2.1 |
| sorted | O0 | 140M | 1.92 | 1.4% | 1.8 |
| sorted | O3 | 26.4M | 1.49 | 8.3% | 11.4 |
| branchless | O0 | 85M | **2.37** | 0.8% | **0.59** |
| branchless | O3 | 10.9M | 2.20 | 2.2% | 2.5 |
| ternary | O0 | 261M | 0.73 | 17.4% | 26.7 |
| ternary | O3 | 15.1M | 1.93 | 2.2% | 2.1 |

Reproduce with:

```bash
perf stat -e cycles,instructions,branches,branch-misses ./build/bench_<impl>_<opt>
```
