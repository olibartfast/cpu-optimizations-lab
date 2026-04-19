# perf-diagnoser

## Purpose

Diagnose whether a performance issue is primarily frontend, branch, cache, memory-latency,
TLB, or IPC/ILP related before proposing changes.

## Use When

- A benchmark regressed
- A hot loop needs investigation
- The right optimization direction is unclear
- Profiling data needs interpretation

## Inputs

- Relevant source files
- Benchmark behavior or observed slowdown
- Available profiler counters or timing output

## Outputs

- A bottleneck classification
- The evidence used
- The next measurement or optimization to try
- Relevant `.agents/rules/*.md` files consulted

## Constraints

- Do not jump to code changes without a bottleneck hypothesis
- Prefer measurement-driven guidance over speculation
- Preserve correctness and readability unless evidence justifies a tradeoff
