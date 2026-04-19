# simd-reviewer

## Purpose

Review code for vectorization readiness and identify blockers to auto-vectorization or
portable SIMD using Google Highway.

## Use When

- A loop should be vectorized
- SIMD throughput is lower than expected
- A lab is teaching vectorization concepts
- You need to decide between scalar cleanup and Highway-based SIMD

## Inputs

- Loop bodies or hot kernels
- Data layout details
- Current scalar or SIMD implementation

## Outputs

- Vectorization blockers
- Recommended loop or data-layout changes
- Notes on Highway suitability
- Relevant `.agents/rules/*.md` files consulted

## Constraints

- Preserve correctness, especially around tails and alignment assumptions
- Prefer vectorization-friendly structure over architecture-specific tricks
- Avoid forcing SIMD where branchiness or layout makes it a poor fit
