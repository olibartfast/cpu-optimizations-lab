# CPU Optimizations Lab — Copilot Instructions

> **Agents: follow and maintain [AGENTS.md](../AGENTS.md) at the repo root.**
> It is the single source of truth for conventions, structure, and pitfalls.
> When you discover something new (a build step, a gotcha, a new lab), edit `AGENTS.md` first.

## Project Overview

A hands-on CPU performance optimization curriculum with 8 progressive C++17 lab exercises (cache optimization, SIMD, branch prediction, data structure design), plus a Python MCP server that provides RAG-based learning assistance via Continue.dev.

## Architecture

| Component | Path | Role |
|-----------|------|------|
| MCP Server | `mcp-server/server.py` | Entry point; defines 5 MCP tools, dispatches to `SimpleRetrievalProvider` |
| Knowledge Base | `mcp-server/knowledge_base.py` | Static `LEARNING_RESOURCES` dict (books, labs, tools, projects); only data source |
| C++ Labs | _(to be added)_ | 8 lab directories built with CMake + GTest |

Data flow: Continue.dev → `call_tool()` in `server.py` → `SimpleRetrievalProvider` → `knowledge_base.py` → JSON response.

## Build and Test

**MCP Server (Python):**
```bash
cd mcp-server
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python server.py
```

**C++ Labs (CMake + GTest):**
```bash
mkdir build && cd build
cmake ..
make -j$(nproc)
ctest
```

Install C++ deps (Linux): `sudo apt-get install cmake build-essential libgtest-dev`

## Code Conventions

- **Python**: Requires 3.9+ (uses built-in generics like `dict[str, Any]`). Use `async/await`, full type hints, and JSON serialization for all MCP tool outputs.
- **Knowledge base entries** must include: `id`, `title`, `topics` (list), `description`, and relevant metadata (`level`, `url`, `author`).
- **Search** is simple case-insensitive substring matching across `title`, `description`, and `topics` — keep resource descriptions keyword-rich.
- **C++ labs**: C++17 standard, CMake build system, Google Test for unit tests, Google Highway for portable SIMD.

## Pitfalls

- The Continue.dev config path is hardcoded to `/workspaces/cpu-optimizations-lab/` — update `.continuerc.json` if the repo is cloned elsewhere.
- Avoid polluting the global Python environment; always activate the `venv` before installing dependencies.
- The knowledge base is purely static — there is no external data loading. To add a resource, edit `knowledge_base.py` directly.
- C++ lab source files are not yet in the repo; only the MCP server exists currently.
