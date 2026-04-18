---
name: Optimize for Branch Prediction
description: Rules for minimizing branch mispredictions and pipeline flushes in performance-critical code by improving branch predictability and using branchless patterns.
tags: [performance, optimization, c, cpp, rust, low-level, systems, branch-prediction, pipeline]
---

# Rule: Optimize for Branch Prediction

## Purpose

Help the CPU predict control flow correctly to avoid pipeline flushes. When the branch predictor guesses wrong, the CPU must squash all speculative work and restart — wasting **10–20 cycles per misprediction**. In tight loops, this compounds into a significant throughput loss.

---

## How the Pipeline Sees a Branch

When the CPU encounters an `if/else` or loop condition, it cannot stall and wait for the result — that would halt the entire pipeline. Instead it:

1. **Predicts** the outcome using a hardware state machine trained on past branch behavior.
2. **Speculatively executes** the predicted path.
3. If the prediction was **wrong**, squashes every speculative instruction and restarts from the correct path.

The branch predictor learns patterns over time. Regular, repetitive branches are predicted well. Irregular, data-dependent branches are not.

---

## Core Principles

### 1. Make Branches Predictable

The branch predictor excels at patterns — loop exit conditions, alternating sequences, and biased branches (almost always true or almost always false).

- **DO:** Structure code so branches are heavily biased or follow a regular pattern.  
- **DON'T:** Rely on branches whose outcome depends on arbitrary or unpredictable input values.

---

### 2. Sort Data Before Branching

Data-dependent branches over unsorted input give the predictor nothing to learn. Sorting the input first makes the branch outcome change at most once, turning an unpredictable branch into a trivially predicted one.

- **DO:** Sort data before processing when branch outcome depends on value comparisons.  
- **DON'T:** Branch on unsorted, randomly distributed values in hot loops.

---

### 3. Replace Branches with Branchless Arithmetic

Conditional assignments can often be rewritten as branchless arithmetic using bitwise operations or ternary expressions that compile to `CMOV` (conditional move) instructions — no prediction required.

- **DO:** Use branchless patterns for simple conditional assignments in hot paths.  
- **DON'T:** Use explicit `if/else` for value selection when a `CMOV` equivalent is available.

---

### 4. Separate Hot and Cold Paths

Restructure loops and functions to isolate the common case from exceptional or rare cases. This keeps the hot path linear and easy to predict.

- **DO:** Move rare or exceptional cases out of the inner loop (e.g., error handling, boundary checks).  
- **DON'T:** Interleave hot-path and cold-path logic inside tight loops.

---

## Anti-Patterns to Avoid

- ❌ Branching on unsorted, randomly distributed input values  
- ❌ Conditional assignments inside hot loops written as `if/else`  
- ❌ Mixing error-handling logic with the hot execution path  
- ❌ Branches whose outcome alternates unpredictably based on data  
- ❌ Early-exit conditions in tight loops that trigger irregularly  

---

## Code Examples

### ❌ Bad: Unpredictable Branch Over Unsorted Data

```c
int sum = 0;
for (int i = 0; i < n; i++) {
    if (a[i] > 128) {       // Unpredictable — random data, random outcome
        sum += a[i];
    }
}
```

---

### ✅ Good: Sort First to Make Branch Predictable

```c
std::sort(a, a + n);        // Branch now transitions once: false → true

int sum = 0;
for (int i = 0; i < n; i++) {
    if (a[i] > 128) {       // Predictor learns the transition point easily
        sum += a[i];
    }
}
```

---

### ❌ Bad: Conditional Assignment with a Branch

```c
int result;
if (a > b) {
    result = a;             // Branch in hot path — potentially mispredicted
} else {
    result = b;
}
```

---

### ✅ Good: Branchless Conditional Assignment (Compiles to CMOV)

```c
int result = (a > b) ? a : b;    // No branch — compiles to CMOV on x86
```

---

### ✅ Good: Branchless Arithmetic with Bitwise Ops

```c
// Branchless absolute value
int mask = x >> 31;               // All 0s if positive, all 1s if negative
int abs_x = (x + mask) ^ mask;   // No branch required
```

---

### ❌ Bad: Cold-Path Logic Mixed into Hot Loop

```c
for (int i = 0; i < n; i++) {
    process(a[i]);
    if (error_flag) {             // Rare but checked every iteration
        handle_error();
    }
}
```

---

### ✅ Good: Cold Path Separated from Hot Loop

```c
for (int i = 0; i < n; i++) {
    process(a[i]);                // Hot path is clean and linear
}

if (error_flag) {                 // Cold path checked once, outside the loop
    handle_error();
}
```

---

## Metrics to Monitor

When profiling branch-heavy code, inspect:

- **Branch Accuracy %**
- **Branch MPKI** (Mispredictions Per Kilo-Instructions)
- **IPC Lost to Branch Mispredictions**

---

## Enforcement Guideline

In performance-critical code:

- Eliminate data-dependent branches over unordered input  
- Replace conditional assignments with branchless patterns where possible  
- Separate hot-path logic from rare or exceptional cases  
- Verify branch accuracy via profiling before and after optimization  

