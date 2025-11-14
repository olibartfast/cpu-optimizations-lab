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

Update your `.continuerc.json`:
```json
{
  "experimental": {
    "modelContextProtocolServers": [
      {
        "name": "cpu-optimization-rag",
        "command": "python",
        "args": [
          "/workspaces/cpu-optimizations-lab/mcp-server/server.py"
        ]
      }
    ]
  }
}
```

## Available Tools

- `search_optimization_topics` - Search resources by keyword
- `get_learning_path` - Get recommended labs by skill level
- `get_lab_info` - Get details about a specific lab
- `get_profiling_tools` - Get tools for a specific platform
- `get_all_resources` - Get complete resource catalog

## Available Resources

- `cpu-opt://resources/all` - All learning resources
- `cpu-opt://labs/overview` - Lab exercises overview
