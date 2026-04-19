# AGENTS.md — CPU Optimizations Lab

This file is the canonical reference for AI agents working in this repository.
**Agents must keep this file up to date** as the codebase evolves (new labs, tools, conventions, pitfalls).

---

## Project Overview

A hands-on CPU performance optimization curriculum with 8 progressive C++17 lab exercises
(cache optimization, SIMD, branch prediction, data structure design), plus a Python MCP server
that provides RAG-based learning assistance via Continue.dev.

---

## Repository Structure

```
/
├── src/                        # C++17 lab source files (one directory per lab topic)
│   ├── cache_optimization/
│   ├── branch_prediction/      # Branch prediction (one subfolder per project)
│   ├── simd_basics/
│   ├── memory_bound_optimizations/
│   ├── data_structures_for_performance/
│   ├── highway_simd_library/
│   ├── advanced_vectorization/
│   └── real_world_scenarios/
├── mcp-server/                 # Python MCP server for RAG assistance
│   ├── server.py               # Entry point; 5 MCP tools, SimpleRetrievalProvider
│   ├── knowledge_base.py       # Static LEARNING_RESOURCES dict (only data source)
│   ├── requirements.txt        # mcp>=1.0.0
│   ├── EXAMPLES.md             # 10 usage examples for Continue.dev
│   └── README.md
├── .agents/
│   └── rules/                  # Repository-specific performance rules for AI agents
│       ├── branch_prediction.md
│       ├── cache_hierarchy.md
│       ├── fe_performance_analysis.md
│       ├── memory_hierarchy_latency_hiding.md
│       ├── optimize_ipc_ilp.md
│       ├── rob_and_ooo_executions.md
│       ├── simd_and_vectorization.md
│       └── tlb_and_address_translation.md
├── .github/
│   └── copilot-instructions.md # VS Code Copilot workspace instructions (references this file)
├── README.md                   # Project overview and lab descriptions
└── AGENTS.md                   # This file — agent-facing conventions (keep up to date)
```

---

## Build and Test

### MCP Server (Python)

```bash
cd mcp-server
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python server.py
```

### C++ Labs (per-lab, standalone)

```bash
cd src/<lab_dir>
g++ -O0 -o bench_O0 <source>.cpp   # unoptimized baseline
g++ -O3 -o bench_O3 <source>.cpp   # optimized
./bench_O0 && ./bench_O3
```

### C++ Labs (CMake, when root CMakeLists.txt exists)

```bash
mkdir build && cd build
cmake ..
make -j$(nproc)
ctest
```

Install C++ deps (Linux):

```bash
sudo apt-get install cmake build-essential libgtest-dev
```

---

## Code Conventions

### C++ Labs

- Standard: **C++17**
- Build: CMake + Google Test (target); per-lab `g++` commands used in practice today
- SIMD: Google Highway for portable vectorization
- Pattern per lab: one `.cpp` source, compiled at O0 and O3 to compare performance
- Benchmark output goes to stdout; keep benchmarks deterministic and side-effect-free

### Python (MCP Server)

- Requires **Python 3.9+** (uses built-in generics: `dict[str, Any]`, `list[...]`)
- Use `async/await` and full type hints throughout
- All MCP tool outputs must be JSON-serializable
- Knowledge base entries must include: `id`, `title`, `topics` (list), `description`,
  plus metadata (`level`, `url`, `author`)
- Search is case-insensitive substring matching — write keyword-rich descriptions

---

## Agent Instructions

- When adding a new C++ lab, create `src/<lab_name>/` with a `.cpp` source and update
  this file's structure table.
- When adding a knowledge base resource, edit `mcp-server/knowledge_base.py` directly
  (no external loading).
- When a new convention, pitfall, or build step is discovered, **update this file immediately**.
- Do not pollute the global Python environment — always work inside `mcp-server/venv`.
- Before changing performance-sensitive C++ code, read the relevant rules in `.agents/rules/`
  and apply them explicitly.

---

## Repository-Specific Performance Rules

Performance rules live in `.agents/rules/`. These files are **normative** for all
optimization work in this repository. Agents must treat them as mandatory guidance,
not optional advice.

### Rule Files

| File | Topic |
|---|---|
| `.agents/rules/branch_prediction.md` | Branch predictability, branchless patterns, hot/cold path separation |
| `.agents/rules/cache_hierarchy.md` | Cache locality, data layouts, memory access patterns |
| `.agents/rules/fe_performance_analysis.md` | Frontend stalls, instruction cache pressure, BTB pressure, decode bandwidth |
| `.agents/rules/memory_hierarchy_latency_hiding.md` | DRAM latency hiding, Memory-Level Parallelism, software/hardware prefetching |
| `.agents/rules/optimize_ipc_ilp.md` | IPC, Instruction-Level Parallelism, dependency chains, loop unrolling |
| `.agents/rules/rob_and_ooo_executions.md` | ROB pressure, out-of-order execution diagnostics, compound bottlenecks |
| `.agents/rules/simd_and_vectorization.md` | SIMD opportunities, auto-vectorization blockers, lane utilization |
| `.agents/rules/tlb_and_address_translation.md` | TLB misses, page working set size, address translation overhead |

### When to Apply Rules

Agents must consult `.agents/rules/` before modifying any code that involves:

- Hot loops
- Branch-heavy logic
- Cache-sensitive data access
- Frontend-bound or instruction-cache-sensitive hot paths
- SIMD or vectorized code
- Memory-bound workloads
- DRAM-latency-bound workloads that need latency hiding or prefetching
- TLB/page-locality-sensitive access patterns
- Benchmarked lab exercises

### Rule Application Expectations

When editing performance-critical code, agents must:

- Check for dependency chains that reduce IPC
- Diagnose frontend vs backend vs memory vs branch bottlenecks before optimizing
- Check for ROB pressure and out-of-order execution limits when profiling indicates low IPC
- Improve instruction-level parallelism where appropriate
- Preserve or improve spatial and temporal cache locality
- Prefer contiguous memory access patterns
- Improve page locality and reduce unnecessary address translation overhead
- Expose Memory-Level Parallelism and use prefetching only when it matches the access pattern
- Reduce unpredictable branches in hot paths
- Separate hot/common paths from cold/rare paths
- Write vectorization-friendly loops and layouts when data-parallel work is present
- Avoid changes that harm correctness or readability without measurable benefit

### Optimization Priority Order

When rules or tradeoffs conflict, use this order:

1. **Correctness**
2. **Repository-specific rules** in `.agents/rules/`
3. **Measurable performance improvement**
4. **Maintainability**
5. **Micro-optimization**

### Validation Expectations

Prefer evidence over guesswork. When proposing or applying performance optimizations,
recommend measuring relevant metrics:

| Category | Metrics |
|---|---|
| Frontend | Frontend Stall %, L1I MPKI, BTB Miss Rate, Fetch Bubbles |
| IPC / Pipeline | IPC, Pipeline Efficiency %, ROB Occupancy |
| Cache | L1D MPKI, LLC MPKI, DRAM Transactions, Avg Miss Latency |
| Branch | Branch Accuracy %, Branch MPKI, IPC Lost to Branch Mispredictions |
| Translation | dTLB Miss Rate, dTLB MPKI, Page Working Set Size |

---

## Pitfalls

- The Continue.dev config path is hardcoded to `/workspaces/cpu-optimizations-lab/` —
  update `.continuerc.json` if the repo is cloned elsewhere.
- `dict[str, Any]` syntax requires Python 3.9+; do not use `typing.Dict` unless
  supporting older versions.
- C++ labs currently use standalone `g++` compilation (not CMake) — a root
  `CMakeLists.txt` does not yet exist.
- The knowledge base is purely static — there is no external data loading.
