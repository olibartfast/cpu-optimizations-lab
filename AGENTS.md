# AGENTS.md — CPU Optimizations Lab

This file is the canonical reference for AI agents working in this repository.
**Agents must keep this file up to date** as the codebase evolves (new labs, tools, conventions, pitfalls).

## Project Overview

A hands-on CPU performance optimization curriculum with 8 progressive C++17 lab exercises (cache optimization, SIMD, branch prediction, data structure design), plus a Python MCP server that provides RAG-based learning assistance via Continue.dev.

## Repository Structure

```
/
├── src/                        # C++17 lab source files
│   └── branch_benchmark/       # Branch prediction lab (bench_O0, bench_O3)
├── mcp-server/                 # Python MCP server for RAG assistance
│   ├── server.py               # Entry point; 5 MCP tools, SimpleRetrievalProvider
│   ├── knowledge_base.py       # Static LEARNING_RESOURCES dict (only data source)
│   ├── requirements.txt        # mcp>=1.0.0
│   ├── EXAMPLES.md             # 10 usage examples for Continue.dev
│   └── README.md
├── .github/
│   └── copilot-instructions.md # VS Code Copilot workspace instructions (references this file)
├── README.md                   # Project overview and lab descriptions
└── AGENTS.md                   # This file — agent-facing conventions (keep up to date)
```

## Build and Test

**MCP Server (Python):**
```bash
cd mcp-server
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python server.py
```

**C++ Labs (per-lab, standalone):**
```bash
cd src/<lab_dir>
g++ -O0 -o bench_O0 <source>.cpp   # unoptimized baseline
g++ -O3 -o bench_O3 <source>.cpp   # optimized
./bench_O0 && ./bench_O3
```

**C++ Labs (CMake, when root CMakeLists.txt exists):**
```bash
mkdir build && cd build
cmake ..
make -j$(nproc)
ctest
```

Install C++ deps (Linux): `sudo apt-get install cmake build-essential libgtest-dev`

## Code Conventions

### C++ Labs
- Standard: C++17
- Build: CMake + Google Test (target); per-lab `g++` commands used in practice today
- SIMD: Google Highway for portable vectorization
- Pattern per lab: one `.cpp` source, compiled at O0 and O3 to compare performance
- Benchmark output goes to stdout; keep benchmarks deterministic and side-effect-free

### Python (MCP Server)
- Requires Python 3.9+ (uses built-in generics: `dict[str, Any]`, `list[...]`)
- Use `async/await` and full type hints throughout
- All MCP tool outputs must be JSON-serializable
- Knowledge base entries must include: `id`, `title`, `topics` (list), `description`, plus metadata (`level`, `url`, `author`)
- Search is case-insensitive substring matching — write keyword-rich descriptions

## Agent Instructions

- When adding a new C++ lab, create `src/<lab_name>/` with a `.cpp` source and update this file's structure table.
- When adding a knowledge base resource, edit `mcp-server/knowledge_base.py` directly (no external loading).
- When a new convention, pitfall, or build step is discovered, **update this file immediately**.
- Do not pollute the global Python environment — always work inside the `mcp-server/venv`.

## Pitfalls

- The Continue.dev config path is hardcoded to `/workspaces/cpu-optimizations-lab/` — update `.continuerc.json` if the repo is cloned elsewhere.
- `dict[str, Any]` syntax requires Python 3.9+; do not use `typing.Dict` unless supporting older versions.
- C++ labs currently use standalone `g++` compilation (not CMake) — a root `CMakeLists.txt` does not yet exist.
- The knowledge base is purely static — there is no external data loading.
