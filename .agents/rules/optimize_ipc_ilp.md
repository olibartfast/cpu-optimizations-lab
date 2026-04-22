---
name: Optimize for IPC & Instruction-Level Parallelism (ILP)
description: Rules for maximizing Instructions Per Cycle (IPC) and Instruction-Level Parallelism in performance-critical code.
tags: [performance, optimization, c, cpp, rust, low-level, systems]
---

# Rule: Optimize for IPC & Instruction-Level Parallelism

## Purpose

Maximize **Instructions Per Cycle (IPC)** by increasing independent work per clock cycle and minimizing pipeline stalls.

Modern 4-wide out-of-order (OoO) cores can retire up to 4 instructions per cycle. Your goal is to keep the pipeline fed with independent instructions and eliminate avoidable stalls to approach peak IPC.

---

## Core Principles

### 1. Favor Independent Work

The CPU executes instructions out-of-order when dependencies allow it. Provide independent instructions so execution units can run in parallel.

- **DO:** Encourage independent computations.  
- **DON'T:** Introduce unnecessary serialization.

---

### 2. Break Dependency Chains

Long dependency chains limit IPC. A loop-carried dependency caps IPC at ≈ 1.

- **DO:** Use multiple accumulators for reductions to enable overlap across iterations and increase achievable IPC.

---

### 3. Prevent ROB (Reorder Buffer) Stalls

The ROB tracks in-flight instructions and retires them in order. If a long-latency instruction (e.g., cache miss) blocks retirement, the ROB fills, younger instructions stall, and IPC collapses.

- **DO:** Minimize cache misses.  
- **DON'T:** Place long-latency operations inside tight loops.

---

### 4. Use Hardware Efficiently

- **Loop Unrolling:** Increase scheduling window, reduce loop overhead, and help break dependency chains.  
- **SIMD / Vectorization:** Process multiple elements per instruction to multiply useful work per cycle.  
- **Reduce Branch Mispredictions:** Prefer predictable branches and use branchless patterns (e.g., conditional moves) in hot paths.

---

## Anti-Patterns to Avoid

When reviewing or writing code, actively avoid:

- ❌ Long sequential arithmetic chains  
- ❌ Single-accumulator reductions in hot loops  
- ❌ Tight loops with unpredictable branches  
- ❌ Memory access patterns causing frequent L1/L2/L3 cache misses  
- ❌ Blocking operations inside performance-critical paths  

---

## Metrics to Target

If guiding profiling or reviewing performance, monitor:

- IPC (Instructions Per Cycle)  
- Pipeline Efficiency %  
- ROB Occupancy  
- Branch Mispredict Rate  
- L1/L2/L3 Cache Miss Rates  

---

## Code Examples

### ❌ Bad: Loop-Carried Dependency (IPC ≈ 1)

```c
int sum = 0;
for (int i = 0; i < n; i++) {
    sum += a[i];   // Loop-carried dependency
}
```

---

### ✅ Good: Multiple Accumulators (Higher IPC)

```c
int sum0 = 0, sum1 = 0, sum2 = 0, sum3 = 0;

for (int i = 0; i < n; i += 4) {
    sum0 += a[i];
    sum1 += a[i+1];
    sum2 += a[i+2];
    sum3 += a[i+3];
}

int sum = sum0 + sum1 + sum2 + sum3;
```

---

## Enforcement Guideline

In performance-critical code:

- Break loop-carried dependencies  
- Increase instruction independence  
- Avoid long-latency operations in hot paths  
- Prefer designs that allow OoO execution to extract parallelism  

