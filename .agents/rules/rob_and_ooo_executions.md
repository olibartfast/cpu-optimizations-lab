---
name: ROB & Out-of-Order Execution
description: Rules for understanding and diagnosing Reorder Buffer pressure, out-of-order execution efficiency, and compound bottlenecks in performance-critical code.
tags: [performance, optimization, c, cpp, rust, low-level, systems, pipeline, ooo, rob, ipc]
---

# Rule: ROB & Out-of-Order Execution

## Purpose

Understand how the Reorder Buffer (ROB) governs out-of-order execution and use ROB
metrics to correctly diagnose whether a bottleneck is **compute-bound**,
**memory-bound**, or **branch-bound** before applying any optimization.

The ROB is the heart of out-of-order execution. Misreading its signals leads to
optimizing the wrong thing.

---

## How the ROB Works

The ROB tracks every in-flight instruction from dispatch to retirement:

1. Instructions **enter** the ROB in program order.
2. Instructions **execute** out of order on whichever execution units are available.
3. Instructions **retire** from the ROB in program order once complete.

If the **oldest instruction** in the ROB is stalled (e.g. waiting on a cache miss or
a branch resolution), **nothing can retire**. The ROB fills up, the front-end stalls,
and execution units go idle — even if many younger instructions are ready to run.

> A full ROB is not the problem — it is a symptom. The problem is whatever is
> blocking the oldest instruction from retiring.

---

## Core Principles

### 1. Read ROB Occupancy Correctly

ROB occupancy alone is not enough information. Its meaning depends on IPC.

| IPC | ROB Occupancy | Diagnosis |
|---|---|---|
| Low | High | **Memory-bound** — ROB full, oldest instruction waiting on a load |
| Low | Low | **Frontend-bound or branch-bound** — ROB draining via mispredicts or not filling fast enough |
| High | Low | **Compute-bound** — near-optimal, limited by execution unit throughput |

- **DO:** Always read ROB occupancy alongside IPC to form a correct diagnosis.
- **DON'T:** Assume high ROB occupancy means the CPU is working efficiently — it may
  mean the ROB is stuck.

---

### 2. Diagnose Before Optimizing

Applying the wrong optimization wastes effort and can make performance worse.

- **DO:** Use the diagnosis table above to identify the actual bottleneck first.
- **DO:** Confirm the diagnosis with profiler data before changing code.
- **DON'T:** Assume a workload is memory-bound just because it touches a lot of data.
- **DON'T:** Assume a workload is compute-bound just because IPC looks high locally.

---

### 3. Understand ROB Occupancy at Mispredict

ROB occupancy at mispredict tells you how deeply the CPU had speculated when a branch
misprediction was detected. All instructions dispatched after the mispredicted branch
must be squashed.

- **High ROB occupancy at mispredict** → the CPU was deeply speculated. Many
  instructions are squashed per misprediction. This indicates a **compound bottleneck**:
  memory-bound stalls are keeping the ROB full while branches are also mispredicting.
- **Low ROB occupancy at mispredict** → the CPU was not deeply speculated. Fewer
  instructions are lost per mispredict. The bottleneck is more likely pure
  branch-bound or frontend-bound.

- **DO:** Treat high ROB occupancy at mispredict as a signal of a compound
  memory + branch bottleneck requiring both cache and branch fixes.
- **DON'T:** Fix only branch mispredictions if the ROB is also being stalled by
  long-latency loads — both must be addressed.

---

### 4. Address the Root Cause of ROB Stalls

Different root causes require different fixes.

#### Memory-bound (ROB full, waiting on loads)
- Improve cache locality — see `.agents/rules/cache-hierarchy.md`
- Increase MLP and use prefetching — see `.agents/rules/llc-and-latency-hiding.md`
- Reduce working set size

#### Branch-bound (ROB draining via mispredicts)
- Eliminate unpredictable branches — see `.agents/rules/branch-prediction.md`
- Use branchless patterns in hot paths
- Separate hot and cold paths

#### Frontend-bound (ROB not filling fast enough)
- Reduce instruction count — simplify hot loops
- Improve ILP to give the front-end more independent work to dispatch
- Check for instruction cache pressure in very large hot loops

#### Compute-bound (execution unit throughput limited)
- Use SIMD/vectorization to do more work per instruction
- Improve ILP — see `.agents/rules/ipc-and-ilp.md`
- Check for structural hazards on specific execution units (e.g. FP divide, integer multiply)

---

## Diagnostic Reference

### Step-by-Step ROB Diagnosis

```
1. Measure IPC and ROB Occupancy together.

2. Is IPC low?
   ├── Yes + ROB Occupancy HIGH  → Memory-bound
   │       Fix: cache locality, prefetching, MLP
   ├── Yes + ROB Occupancy LOW   → Frontend-bound or Branch-bound
   │       Fix: reduce mispredictions, simplify front-end
   └── No  + ROB Occupancy LOW   → Compute-bound
           Fix: SIMD, ILP, execution unit throughput

3. Check ROB Occupancy at Mispredict.
   └── HIGH → Compound memory + branch bottleneck
           Fix: both cache and branch issues simultaneously
```

---

## Anti-Patterns to Avoid

- ❌ Optimizing for branch prediction when the bottleneck is actually memory-bound
- ❌ Adding prefetching when the bottleneck is actually branch-bound
- ❌ Treating high ROB occupancy as a sign of healthy execution without checking IPC
- ❌ Treating low ROB occupancy as a sign of poor execution without checking IPC
- ❌ Fixing only one half of a compound memory + branch bottleneck
- ❌ Applying micro-optimizations before identifying which bottleneck category applies

---

## Metrics to Monitor

When profiling out-of-order execution behavior, inspect:

| Metric | What it reveals |
|---|---|
| **ROB Occupancy** | How full the ROB is — combined with IPC reveals bottleneck type |
| **ROB Occupancy at Mispredict** | Depth of speculation lost per misprediction |
| **IPC** | Overall execution efficiency |
| **Slots Utilised %** | Fraction of available pipeline slots doing useful work |

---

## Relationship to Other Rules

ROB metrics are a **diagnostic layer** that sits above the other performance rules.
Use them to decide which rule to apply:

| Diagnosis | Primary Rule to Apply |
|---|---|
| Memory-bound | `.agents/rules/cache-hierarchy.md` |
| Latency-hiding needed | `.agents/rules/llc-and-latency-hiding.md` |
| Branch-bound | `.agents/rules/branch-prediction.md` |
| Compute-bound / low IPC | `.agents/rules/ipc-and-ilp.md` |

---

## Enforcement Guideline

In performance-critical code:

- Always diagnose bottleneck type using IPC and ROB occupancy together before optimizing
- Treat ROB occupancy at mispredict as a compound bottleneck signal
- Address the root cause of ROB stalls — not the symptom
- Cross-reference the relevant rule file for the identified bottleneck category
- Validate that the optimization moved the correct metric before declaring success

