# CPU Optimization RAG MCP Server (Python)

Python implementation of the MCP server providing RAG capabilities for CPU optimization learning resources.

## Setup

1. **Create a virtual environment** (recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Linux/Mac
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Run directly
```bash
python server.py
```

### Use with Continue.dev

Update your `.continuerc.json` (adjust the path to match where you cloned the repo):
```json
{
  "experimental": {
    "modelContextProtocolServers": [
      {
        "name": "cpu-optimization-rag",
        "command": "python",
        "args": [
          "/path/to/cpu-optimizations-lab/mcp-server/server.py"
        ]
      }
    ]
  }
}
```

## Available Tools

- `search_optimization_topics` — Search resources by keyword
- `get_learning_path` — Get recommended labs by skill level
- `get_lab_info` — Get details about a lab by id (e.g. `lab-03`) or number (`3`)
- `get_profiling_tools` — Get tools for a specific platform
- `get_all_resources` — Get complete resource catalog
- `search_performance_rules` — Search the repo's normative performance rules (`.agents/rules/`)

## Available Resources

- `cpu-opt://resources/all` — All learning resources
- `cpu-opt://labs/overview` — Lab exercises overview
- `cpu-opt://rules/all` — All performance rule files
