import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
  ListResourcesRequestSchema,
  ReadResourceRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";
import { RetrievalProviderFactory } from "./providers/RetrievalProviderFactory.js";
import { IRetrievalProvider } from "./providers/IRetrievalProvider.js";
import { LEARNING_RESOURCES } from "./data/knowledgeBase.js";

// Global retrieval provider instance
let retrievalProvider: IRetrievalProvider;

// Create MCP server
const server = new Server(
  {
    name: "cpu-optimization-rag-server",
    version: "1.0.0",
  },
  {
    capabilities: {
      resources: {},
      tools: {},
    },
  }
);

// List available tools
server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      {
        name: "search_optimization_topics",
        description: "Search for CPU optimization resources, techniques, and learning materials by topic or keyword",
        inputSchema: {
          type: "object",
          properties: {
            query: {
              type: "string",
              description: "Search query (e.g., 'cache optimization', 'simd', 'branch prediction')",
            },
          },
          required: ["query"],
        },
      },
      {
        name: "get_learning_path",
        description: "Get recommended learning path and labs based on skill level",
        inputSchema: {
          type: "object",
          properties: {
            level: {
              type: "string",
              enum: ["beginner", "intermediate", "advanced"],
              description: "Your current skill level with CPU optimization",
            },
          },
          required: ["level"],
        },
      },
      {
        name: "get_lab_info",
        description: "Get detailed information about a specific lab exercise",
        inputSchema: {
          type: "object",
          properties: {
            labNumber: {
              type: "number",
              description: "Lab number (1-8)",
              minimum: 1,
              maximum: 8,
            },
          },
          required: ["labNumber"],
        },
      },
      {
        name: "get_profiling_tools",
        description: "Get recommended profiling tools for a specific platform",
        inputSchema: {
          type: "object",
          properties: {
            platform: {
              type: "string",
              enum: ["linux", "windows", "macos"],
              description: "Operating system platform",
            },
          },
          required: ["platform"],
        },
      },
      {
        name: "get_all_resources",
        description: "Get complete catalog of all available learning resources",
        inputSchema: {
          type: "object",
          properties: {},
        },
      },
    ],
  };
});

// Handle tool calls
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  if (!args) {
    throw new Error("Missing arguments");
  }

  switch (name) {
    case "search_optimization_topics": {
      const query = args.query as string;
      const results = await retrievalProvider.searchTopics(query);
      return {
        content: [
          {
            type: "text",
            text: JSON.stringify(results, null, 2),
          },
        ],
      };
    }

    case "get_learning_path": {
      const level = args.level as string;
      const path = await retrievalProvider.getLearningPath(level);
      return {
        content: [
          {
            type: "text",
            text: JSON.stringify({
              level,
              recommendedLabs: path,
              description: `Recommended learning path for ${level} level`
            }, null, 2),
          },
        ],
      };
    }

    case "get_lab_info": {
      const labNumber = args.labNumber as number;
      const labInfo = await retrievalProvider.getLabInfo(labNumber);
      return {
        content: [
          {
            type: "text",
            text: labInfo ? JSON.stringify(labInfo, null, 2) : `Lab ${labNumber} not found`,
          },
        ],
      };
    }

    case "get_profiling_tools": {
      const platform = args.platform as string;
      const tools = await retrievalProvider.getProfilingTools(platform);
      return {
        content: [
          {
            type: "text",
            text: JSON.stringify({
              platform,
              tools
            }, null, 2),
          },
        ],
      };
    }

    case "get_all_resources": {
      const resources = await retrievalProvider.getAllResources();
      return {
        content: [
          {
            type: "text",
            text: JSON.stringify(resources, null, 2),
          },
        ],
      };
    }

    default:
      throw new Error(`Unknown tool: ${name}`);
  }
});

// List resources
server.setRequestHandler(ListResourcesRequestSchema, async () => {
  return {
    resources: [
      {
        uri: "cpu-opt://resources/all",
        name: "All CPU Optimization Resources",
        description: "Complete catalog of learning resources, labs, tools, and references",
        mimeType: "application/json",
      },
      {
        uri: "cpu-opt://labs/overview",
        name: "Labs Overview",
        description: "Overview of all 8 lab exercises with difficulty and topics",
        mimeType: "application/json",
      },
    ],
  };
});

// Read resources
server.setRequestHandler(ReadResourceRequestSchema, async (request) => {
  const uri = request.params.uri;

  if (uri === "cpu-opt://resources/all") {
    return {
      contents: [
        {
          uri,
          mimeType: "application/json",
          text: JSON.stringify(LEARNING_RESOURCES, null, 2),
        },
      ],
    };
  } else if (uri === "cpu-opt://labs/overview") {
    return {
      contents: [
        {
          uri,
          mimeType: "application/json",
          text: JSON.stringify(LEARNING_RESOURCES.labs, null, 2),
        },
      ],
    };
  }

  throw new Error(`Resource not found: ${uri}`);
});

// Start the server
async function main() {
  // Initialize the retrieval provider from environment variable
  // Set RETRIEVAL_PROVIDER=simple|embeddings|full-rag (default: simple)
  retrievalProvider = await RetrievalProviderFactory.createFromEnv();
  
  const transport = new StdioServerTransport();
  await server.connect(transport);
  
  const providerType = process.env.RETRIEVAL_PROVIDER || 'simple';
  console.error(`CPU Optimization RAG MCP Server running on stdio (provider: ${providerType})`);
}

main().catch((error) => {
  console.error("Server error:", error);
  process.exit(1);
});
