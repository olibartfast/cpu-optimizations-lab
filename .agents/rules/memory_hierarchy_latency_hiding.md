---
name: Memory Hierarchy & Latency Hiding
description: Rules for tolerating DRAM latency through Memory-Level Parallelism, prefetching, and DRAM-friendly access patterns in performance-critical code.
tags: [performance, optimization, c, cpp, rust, low-level, systems, memory, dram, prefetch, mlp]
---

# Rule: Memory Hierarchy & Latency Hiding

## Purpose

Tolerate the gap between CPU execution speed and DRAM latency by maximizing
**Memory-Level Parallelism (MLP)** and issuing memory requests early enough to
overlap their latency with useful work.

Even with perfect cache usage, some workloads must reach DRAM. The key insight is that
**latency is not the same as bandwidth** — if enough independent loads are in flight
simultaneously, the memory controller can overlap them and deliver high throughput
despite high per-request latency (~200 cycles).

---

## Core Principles

### 1. Distinguish Latency from Bandwidth

These are separate problems with different solutions.

| Problem | Cause | Solution |
|---|---|---|
| **Latency-bound** | Serial pointer chasing, one load at a time | Increase MLP, prefetch, restructure access |
| **Bandwidth-bound** | Many parallel loads, but memory bus saturated | Reduce working set, compress data, improve locality |

- **DO:** Identify which problem you have before optimizing.
- **DON'T:** Assume that faster access patterns always help — bandwidth saturation
  requires reducing data volume, not just issuing more requests.

---

### 2. Expose Memory-Level Parallelism (MLP)

Latency is hidden when multiple independent loads are in flight at the same time.
The memory controller can service them in parallel, amortizing the ~200 cycle cost
across many requests.

- **DO:** Issue independent loads as early as possible to keep the memory controller busy.
- **DO:** Prefer loops that access independent addresses per iteration over
  pointer-chasing chains.
- **DON'T:** Serialize memory requests — one load depending on the result of the
  previous one exposes full latency with no overlap.

---

### 3. Favor Strided Over Scattered Access

The hardware prefetcher automatically detects and prefetches regular stride patterns
(stride 1, 2, 4, etc.). Irregular or data-dependent access patterns cannot be
predicted and expose full DRAM latency on every miss.

- **DO:** Access memory in regular, predictable strides to activate hardware prefetching.
- **DON'T:** Scatter loads across memory in data-dependent or irregular patterns in
  hot loops.

> Strided accesses expose **bandwidth**.
> Random/scattered accesses expose **latency**.

---

### 4. Use Software Prefetching for Irregular Patterns

When access patterns are predictable in software but irregular enough to defeat the
hardware prefetcher, use explicit software prefetch hints.

- **DO:** Use `__builtin_prefetch(ptr, rw, locality)` to issue prefetches
  **100–200 cycles ahead** of the actual access.
- **DO:** Tune the prefetch distance to match memory latency on the target platform.
- **DON'T:** Prefetch data-dependent or truly random addresses — it adds overhead
  with no benefit.
- **DON'T:** Prefetch too close to the access — the data will not arrive in time.

---

### 5. Respect DRAM Row Buffer Locality

DRAM is organized in rows. Accessing the same row repeatedly is fast (row buffer hit).
Switching rows incurs an extra ~50 ns penalty (row buffer miss).

- **DO:** Access DRAM in strided, row-aligned patterns to maximize row buffer hit rate.
- **DON'T:** Scatter accesses across many DRAM rows — each row switch adds latency
  on top of base DRAM latency.

---

## Anti-Patterns to Avoid

- ❌ Pointer-chasing linked structures in memory-bound hot paths (linked lists, trees,
  pointer-heavy graphs)
- ❌ Serial dependent loads where each address depends on the previous load's result
- ❌ Scattered or random access patterns that defeat hardware prefetching
- ❌ Prefetching too close to the access (data does not arrive in time)
- ❌ Prefetching truly random or data-dependent addresses (overhead with no gain)
- ❌ Access patterns that thrash DRAM rows, maximizing row buffer misses

---

## Code Examples

### ❌ Bad: Pointer Chasing — Serial Latency, No MLP

```c
// Each load depends on the result of the previous one
// Full ~200 cycle DRAM latency is exposed serially
Node* cur = head;
while (cur) {
    process(cur->value);
    cur = cur->next;     // Address unknown until previous load completes
}
```

---

### ✅ Good: Sequential Streaming — Hardware Prefetcher Activates

```c
// Regular stride — hardware prefetcher detects and prefetches ahead
// Near-peak memory bandwidth is achievable
for (int i = 0; i < n; i++) {
    process(a[i]);       // Stride-1 access, fully predictable
}
```

---

### ✅ Good: Software Prefetch for Predictable Irregular Access

```c
#define PREFETCH_DISTANCE 16

for (int i = 0; i < n; i++) {
    __builtin_prefetch(&a[index[i + PREFETCH_DISTANCE]], 0, 1);  // Prefetch ahead
    process(a[index[i]]);
}
```

---

### ❌ Bad: Row-Thrashing Access Pattern

```c
// Accessing column-major in a row-major layout
// Each access hits a different DRAM row — maximizes row buffer misses
for (int col = 0; col < N; col++) {
    for (int row = 0; row < N; row++) {
        sum += matrix[row][col];    // Stride-N — new DRAM row every access
    }
}
```

---

### ✅ Good: Row-Aligned Access Pattern

```c
// Row-major traversal — stays within the same DRAM row across many accesses
// Maximizes row buffer hit rate
for (int row = 0; row < N; row++) {
    for (int col = 0; col < N; col++) {
        sum += matrix[row][col];    // Sequential — row buffer hit
    }
}
```

---

### ✅ Good: Independent Loads to Maximize MLP

```c
// Unrolled loop issues multiple independent loads per iteration
// Memory controller can service them in parallel
for (int i = 0; i < n; i += 4) {
    int v0 = a[i];
    int v1 = a[i + 1];    // Independent of v0
    int v2 = a[i + 2];    // Independent of v0, v1
    int v3 = a[i + 3];    // Independent of v0, v1, v2
    process(v0, v1, v2, v3);
}
```

---

## Metrics to Monitor

When profiling memory-latency-bound code, inspect:

| Metric | What it reveals |
|---|---|
| **DRAM Transactions** | Volume of traffic reaching DRAM |
| **Row Buffer Hit Rate** | Quality of DRAM access locality |
| **LLC Avg Miss Latency** | Effective latency seen by the CPU on LLC misses |

---

## Enforcement Guideline

In performance-critical code that reaches DRAM:

- Issue independent loads early and in parallel to maximize MLP
- Use regular stride patterns to activate hardware prefetching
- Use software prefetching when patterns are predictable but irregular
- Align access patterns to DRAM row boundaries to maximize row buffer hit rate
- Avoid pointer-chasing structures in hot paths — restructure to arrays where possible
- Profile before optimizing — distinguish latency-bound from bandwidth-bound workloads

