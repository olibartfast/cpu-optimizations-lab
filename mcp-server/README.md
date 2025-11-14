# CPU Optimization RAG/MCP Server

A Model Context Protocol (MCP) server providing Retrieval-Augmented Generation (RAG) capabilities for CPU optimization learning resources with **pluggable retrieval strategies**.

## Overview

This MCP server uses a **factory pattern** to support three different retrieval strategies:

### 🔧 Retrieval Strategies (Switch via `RETRIEVAL_PROVIDER` env var)

1. **Simple Provider** (`simple`) - Default, no external dependencies
   - Fast keyword-based search
   - No AI models required
   - Instant startup
   - Perfect for basic resource lookup

2. **Embeddings Provider** (`embeddings`) - Option A: Vector search
   - Semantic search using llama.cpp embeddings
   - Better understanding of query intent
   - Requires embedding model (e.g., nomic-embed-text)
   - Returns ranked results by similarity

3. **Full RAG Provider** (`full-rag`) - Option B: Complete RAG system
   - Embeddings for retrieval + LLM for generation
   - Generates natural language responses
   - Requires both embedding and LLM models
   - Most powerful but resource-intensive

## Quick Start

### Installation

```bash
cd mcp-server
npm install
npm run build
```

### Usage - Simple Provider (Default)

```bash
# No configuration needed
npm start
```

### Usage - With Embeddings (Advanced)

```bash
# 1. Download an embedding model
# Example: https://huggingface.co/nomic-ai/nomic-embed-text-v1.5-GGUF
mkdir -p models
# Download nomic-embed-text-v1.5.Q8_0.gguf to models/

# 2. Configure environment
export RETRIEVAL_PROVIDER=embeddings
export EMBEDDING_MODEL_PATH=./models/nomic-embed-text-v1.5.Q8_0.gguf

# 3. Run
npm start
```

### Usage - Full RAG (Maximum Power)

```bash
# 1. Download both embedding and LLM models
mkdir -p models
# Download embedding model (e.g., nomic-embed-text)
# Download LLM model (e.g., llama-3.2-1b-instruct)

# 2. Configure environment
export RETRIEVAL_PROVIDER=full-rag
export EMBEDDING_MODEL_PATH=./models/nomic-embed-text-v1.5.Q8_0.gguf
export LLM_MODEL_PATH=./models/llama-3.2-1b-instruct-q4_0.gguf

# 3. Run
npm start
```

Or use the `.env` file:

```bash
cp .env.example .env
# Edit .env with your configuration
npm start
```

## Features

### Available Tools

1. **search_optimization_topics** - Search for resources by keyword or topic
   - Example: Search for "simd", "cache optimization", "branch prediction"
   - Returns ranked results from books, online resources, projects, and labs

2. **get_learning_path** - Get personalized learning recommendations
   - Input: skill level (beginner/intermediate/advanced)
   - Returns: Recommended sequence of labs for that level

3. **get_lab_info** - Get detailed information about specific labs
   - Input: lab number (1-8)
   - Returns: Duration, topics, description, speedup targets

4. **get_profiling_tools** - Get platform-specific profiling tools
   - Input: platform (linux/windows/macos)
   - Returns: Recommended tools with usage examples

5. **get_all_resources** - Get complete resource catalog
   - Returns: All books, online resources, projects, labs, and tools

### Resources

- `cpu-opt://resources/all` - Complete catalog of all resources
- `cpu-opt://labs/overview` - Overview of all lab exercises

## Installation

```bash
cd mcp-server
npm install
npm run build
```

## Usage

### As Standalone Server

```bash
npm start
```

## Configuration for Claude Desktop

Add to your Claude Desktop configuration file:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

### Simple Provider (Default - Recommended)
```json
{
  "mcpServers": {
    "cpu-optimization": {
      "command": "node",
      "args": ["/workspaces/cpu-optimizations-lab/mcp-server/dist/index.js"],
      "env": {
        "RETRIEVAL_PROVIDER": "simple"
      }
    }
  }
}
```

### Embeddings Provider
```json
{
  "mcpServers": {
    "cpu-optimization": {
      "command": "node",
      "args": ["/workspaces/cpu-optimizations-lab/mcp-server/dist/index.js"],
      "env": {
        "RETRIEVAL_PROVIDER": "embeddings",
        "EMBEDDING_MODEL_PATH": "/path/to/models/nomic-embed-text-v1.5.Q8_0.gguf"
      }
    }
  }
}
```

### Full RAG Provider
```json
{
  "mcpServers": {
    "cpu-optimization": {
      "command": "node",
      "args": ["/workspaces/cpu-optimizations-lab/mcp-server/dist/index.js"],
      "env": {
        "RETRIEVAL_PROVIDER": "full-rag",
        "EMBEDDING_MODEL_PATH": "/path/to/models/nomic-embed-text-v1.5.Q8_0.gguf",
        "LLM_MODEL_PATH": "/path/to/models/llama-3.2-1b-instruct-q4_0.gguf"
      }
    }
  }
}
```

### Configuration for Other MCP Clients

Use the stdio transport with the command:
```bash
node /workspaces/cpu-optimizations-lab/mcp-server/dist/index.js
```

## Example Queries

Once connected to an MCP client (like Claude Desktop), you can ask:

- "What resources are available for learning SIMD programming?"
- "I'm a beginner. What's the recommended learning path?"
- "Tell me about lab 3"
- "What profiling tools should I use on Linux?"
- "Find resources about cache optimization"

## Development

```bash
# Watch mode for development
npm run watch

# Build
npm run build

# Run
npm run dev
```

## Architecture

The server uses a **Factory Pattern** for pluggable retrieval strategies:

```
┌─────────────────────────────────────┐
│      MCP Server (index.ts)          │
│                                     │
│  ┌───────────────────────────────┐ │
│  │ RetrievalProviderFactory      │ │
│  │  createFromEnv()              │ │
│  └───────────┬───────────────────┘ │
│              │                      │
│              ├─────────────────────┐│
│              │                     ││
│      ┌───────▼─────┐  ┌──────────▼▼────────┐  ┌─────────▼─────┐
│      │   Simple    │  │   Embeddings       │  │   Full RAG    │
│      │  Provider   │  │    Provider        │  │   Provider    │
│      │             │  │                    │  │               │
│      │ • Keyword   │  │ • Vector Search    │  │ • Embeddings  │
│      │   Matching  │  │ • Cosine Sim       │  │ • LLM Gen     │
│      │             │  │ • llama.cpp        │  │ • llama.cpp   │
│      └─────────────┘  └────────────────────┘  └───────────────┘
└─────────────────────────────────────┘
```

### Knowledge Base Structure

```typescript
{
  books: [...],           // Learning books and manuals
  onlineResources: [...], // Web resources and documentation
  projects: [...],        // Related open-source projects
  labs: [...],           // Lab exercises with metadata
  tools: {               // Platform-specific profiling tools
    linux: [...],
    windows: [...],
    macos: [...]
  }
}
```

### Search Algorithms

**Simple Provider:**
- Title matches (10 points)
- Description matches (5 points)
- Topic matches (8 points)

**Embeddings Provider:**
- Cosine similarity between query and document embeddings
- Threshold-based filtering
- Similarity score ranking

**Full RAG Provider:**
- Context retrieval via embeddings
- LLM prompt construction with retrieved context
- Natural language response generation

## Extending the System

### Adding a New Provider

1. Create a new provider class implementing `IRetrievalProvider`:

```typescript
// src/providers/MyCustomProvider.ts
import { IRetrievalProvider, SearchResult } from "./IRetrievalProvider.js";

export class MyCustomProvider implements IRetrievalProvider {
  async initialize(): Promise<void> {
    // Setup logic
  }

  async searchTopics(query: string, limit?: number): Promise<SearchResult[]> {
    // Your search implementation
  }

  // Implement other required methods...
  async dispose(): Promise<void> {
    // Cleanup
  }
}
```

2. Register it in the factory:

```typescript
// src/providers/RetrievalProviderFactory.ts
case 'my-custom':
  provider = new MyCustomProvider();
  break;
```

### Adding New Resources

To add new resources, edit `src/data/knowledgeBase.ts`:

```typescript
export const LEARNING_RESOURCES = {
  books: [
    {
      id: "unique-id",
      title: "Book Title",
      author: "Author Name",
      topics: ["topic1", "topic2"],
      description: "Description",
      url: "optional-url"
    },
    // ... add more
  ],
  // ... other categories
};
```

### Implementing llama.cpp Integration

The `EmbeddingsRetrievalProvider` and `FullRAGProvider` have TODO comments showing where to add llama.cpp integration. To implement:

1. Install llama.cpp bindings (already in optionalDependencies):
```bash
npm install node-llama-cpp
```

2. Uncomment and implement the TODO sections in:
   - `src/providers/EmbeddingsRetrievalProvider.ts`
   - `src/providers/FullRAGProvider.ts`

3. Download appropriate models from Hugging Face

Example implementation snippet:
```typescript
import { LlamaCpp } from 'node-llama-cpp';

const model = new LlamaCpp({
  modelPath: process.env.EMBEDDING_MODEL_PATH,
  embedding: true
});

const embedding = await model.embed("your text here");
```

## License

MIT License - see parent project LICENSE file for details.
