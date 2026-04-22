---
name: Optimize for Cache Hierarchy & Memory Access Patterns
description: Rules for minimizing cache misses and memory latency in performance-critical code by improving data locality and access patterns.
tags: [performance, optimization, c, cpp, rust, low-level, systems, memory, cache]
---

# Rule: Optimize for Cache Hierarchy & Memory Access Patterns

## Purpose

Bridge the gap between CPU execution speed and memory latency by keeping frequently accessed data in cache. DRAM takes ~200 cycles to respond — a program that hits DRAM frequently will be bottlenecked no matter how fast the core is.

---

## The Cache Hierarchy

| Level       | Typical Size | Latency    |
|-------------|-------------|------------|
| L1D         | ~32 KB      | ~4 cycles  |
| L2          | ~256 KB     | ~12 cycles |
| LLC (L3)    | ~6 MB       | ~40 cycles |
| DRAM        | —           | ~200 cycles|

- **L1D:** Fastest and smallest. One miss here is recoverable if L2 has the data.  
- **L2:** Handles L1 overflows. Still fast.  
- **LLC:** Last line of defense before DRAM.  
- **DRAM:** Catastrophically slow. Avoid frequent hits at all costs.

---

## Core Principles

### 1. Exploit Spatial Locality

CPUs load data in **64-byte cache lines**. Accessing one element brings adjacent elements into cache for free.

- **DO:** Access memory sequentially and in contiguous blocks.  
- **DON'T:** Jump across memory with large, irregular strides.

> Accessing `arr[0]` brings `arr[1]` through `arr[7]` into cache automatically.

---

### 2. Exploit Temporal Locality

Reuse the same data as soon as possible after loading it to avoid eviction before the next access.

- **DO:** Structure loops to reuse loaded data within the same or nearby iterations.  
- **DON'T:** Load data once, discard it, and reload it later from a cold cache.

---

### 3. Restructure Data Layouts

Favor layouts where frequently accessed fields are contiguous in memory.

- **DO:** Prefer **Struct of Arrays (SoA)** for hot loops that access a subset of fields.  
- **DON'T:** Use **Array of Structs (AoS)** when only one or two fields are accessed per iteration.

---

### 4. Tile Loops to Fit Cache

When operating on large matrices or multi-dimensional data, tile (block) loops so the working set fits within L1 or L2.

- **DO:** Process data in cache-sized blocks.  
- **DON'T:** Traverse large 2D arrays column-by-column (destroys spatial locality).

---

### 5. Prefetch Predictable Access Patterns

When access patterns are regular and predictable, use software prefetching to hide DRAM latency.

- **DO:** Use `__builtin_prefetch` (GCC/Clang) ahead of predictable memory accesses.  
- **DON'T:** Prefetch irregular or data-dependent access patterns — it adds noise with no benefit.

---

### 6. Reduce Data Size

Smaller data keeps more elements in cache per cache line.

- **DO:** Use smaller types where precision allows (e.g., `float` vs `double`, `int16_t` vs `int32_t`).  
- **DO:** Consider bit packing for boolean or flag-heavy structures.  
- **DON'T:** Pad structures unnecessarily or store redundant fields in hot data paths.

---

## Anti-Patterns to Avoid

- ❌ Column-major traversal of row-major arrays  
- ❌ Array of Structs with large structs when only one field is accessed per loop  
- ❌ Large working sets that exceed LLC capacity in inner loops  
- ❌ Pointer-chasing linked structures in hot paths (e.g., linked lists, trees)  
- ❌ Unpredictable or scattered memory access patterns in tight loops  

---

## Code Examples

### ❌ Bad: Column-Major Traversal (Destroys Spatial Locality)

```c
for (int col = 0; col < N; col++) {
    for (int row = 0; row < N; row++) {
        sum += matrix[row][col];   // Stride-N access — cache line wasted
    }
}
```

---

### ✅ Good: Row-Major Traversal (Exploits Spatial Locality)

```c
for (int row = 0; row < N; row++) {
    for (int col = 0; col < N; col++) {
        sum += matrix[row][col];   // Sequential access — full cache line used
    }
}
```

---

### ❌ Bad: Array of Structs (AoS) — Wastes Cache Lines

```c
struct Particle {
    float x, y, z;   // Position
    float vx, vy, vz; // Velocity
    float mass;
    int   flags;
};

Particle particles[N];

for (int i = 0; i < N; i++) {
    particles[i].x += particles[i].vx;   // Loads full struct, uses only 2 fields
}
```

---

### ✅ Good: Struct of Arrays (SoA) — Dense Cache Lines

```c
struct Particles {
    float x[N], y[N], z[N];
    float vx[N], vy[N], vz[N];
    float mass[N];
    int   flags[N];
};

Particles particles;

for (int i = 0; i < N; i++) {
    particles.x[i] += particles.vx[i];   // Only accesses relevant arrays
}
```

---

### ✅ Software Prefetching

```c
for (int i = 0; i < n; i++) {
    __builtin_prefetch(&a[i + 16], 0, 1);   // Prefetch ahead
    sum += a[i];
}
```

---

## Metrics to Monitor

When profiling memory-bound code, inspect:

- **L1D MPKI** (Misses Per Kilo-Instructions)  
- **LLC MPKI**  
- **DRAM Transactions**  
- **Average Miss Latency**  

---

## Enforcement Guideline

In performance-critical code:

- Access memory sequentially and in contiguous blocks  
- Restructure data layouts to match access patterns  
- Tile loops to keep working sets within L1/L2  
- Reduce data size to increase cache density  
- Avoid pointer-chasing and scattered access in hot paths  

