#!/usr/bin/env python3
"""MCP server providing RAG capabilities for CPU optimization learning resources"""

import asyncio
import json
import pathlib
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Resource, Tool, TextContent

from knowledge_base import LEARNING_RESOURCES

RULES_DIR = pathlib.Path(__file__).parent.parent / ".agents" / "rules"


class SimpleRetrievalProvider:
    """Simple keyword-based retrieval provider"""
    
    def __init__(self):
        self.resources = LEARNING_RESOURCES
    
    def search_topics(self, query: str) -> dict[str, Any]:
        """Search for topics matching the query"""
        query_lower = query.lower()
        categories = ["books", "onlineResources", "projects", "labs"]
        results: dict[str, list[Any]] = {cat: [] for cat in categories}

        for cat in categories:
            for item in self.resources[cat]:
                if (
                    any(query_lower in t.lower() for t in item["topics"])
                    or query_lower in item["title"].lower()
                    or query_lower in item["description"].lower()
                ):
                    results[cat].append(item)

        return results
    
    def get_learning_path(self, level: str) -> list[dict[str, Any]]:
        """Get recommended learning path based on skill level"""
        return [lab for lab in self.resources["labs"] if lab["level"] == level]
    
    def get_lab_info(self, lab_id: str) -> dict[str, Any] | None:
        """Get detailed information about a specific lab by id or 1-based number"""
        # support numeric lookup for backward compat
        if lab_id.isdigit():
            idx = int(lab_id) - 1
            if 0 <= idx < len(self.resources["labs"]):
                return self.resources["labs"][idx]
            return None
        return next(
            (lab for lab in self.resources["labs"] if lab["id"] == lab_id), None
        )
    
    def get_profiling_tools(self, platform: str) -> list[dict[str, Any]]:
        """Get profiling tools for a specific platform"""
        return self.resources["tools"].get(platform, [])
    
    def get_performance_rules(self) -> list[dict[str, Any]]:
        """Return all performance rule files as structured entries"""
        rules = []
        if RULES_DIR.is_dir():
            for path in sorted(RULES_DIR.glob("*.md")):
                rules.append({"id": path.stem, "title": path.stem.replace("_", " ").title(), "content": path.read_text()})
        return rules

    def search_performance_rules(self, query: str) -> list[dict[str, Any]]:
        """Search performance rule files by keyword"""
        query_lower = query.lower()
        return [
            {"id": r["id"], "title": r["title"], "excerpt": r["content"][:500]}
            for r in self.get_performance_rules()
            if query_lower in r["content"].lower() or query_lower in r["id"].lower()
        ]


# Initialize the retrieval provider
retrieval_provider = SimpleRetrievalProvider()

# Create the MCP server
app = Server("cpu-optimization-rag-server")


@app.list_resources()
async def list_resources() -> list[Resource]:
    """List available resources"""
    resources = [
        Resource(
            uri="cpu-opt://resources/all",
            name="All CPU Optimization Resources",
            description="Complete catalog of learning resources, labs, tools, and references",
            mimeType="application/json",
        ),
        Resource(
            uri="cpu-opt://labs/overview",
            name="Labs Overview",
            description="Overview of all 8 lab exercises with difficulty and topics",
            mimeType="application/json",
        ),
        Resource(
            uri="cpu-opt://rules/all",
            name="Performance Rules",
            description="All repository-specific CPU performance rules (branch prediction, cache, SIMD, IPC, TLB, etc.)",
            mimeType="application/json",
        ),
    ]
    return resources


@app.read_resource()
async def read_resource(uri: str) -> str:
    """Read a specific resource"""
    if uri == "cpu-opt://resources/all":
        return json.dumps(LEARNING_RESOURCES, indent=2)
    elif uri == "cpu-opt://labs/overview":
        return json.dumps(LEARNING_RESOURCES["labs"], indent=2)
    elif uri == "cpu-opt://rules/all":
        return json.dumps(retrieval_provider.get_performance_rules(), indent=2)
    else:
        raise ValueError(f"Resource not found: {uri}")


@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools"""
    return [
        Tool(
            name="search_optimization_topics",
            description="Search for CPU optimization resources, techniques, and learning materials by topic or keyword",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query (e.g., 'cache optimization', 'simd', 'branch prediction')",
                    },
                },
                "required": ["query"],
            },
        ),
        Tool(
            name="get_learning_path",
            description="Get recommended learning path and labs based on skill level",
            inputSchema={
                "type": "object",
                "properties": {
                    "level": {
                        "type": "string",
                        "enum": ["beginner", "intermediate", "advanced"],
                        "description": "Your current skill level with CPU optimization",
                    },
                },
                "required": ["level"],
            },
        ),
        Tool(
            name="get_lab_info",
            description="Get detailed information about a specific lab exercise by id (e.g. 'lab-03') or number (1-8)",
            inputSchema={
                "type": "object",
                "properties": {
                    "labId": {
                        "type": "string",
                        "description": "Lab id (e.g. 'lab-03') or 1-based number as string (e.g. '3')",
                    },
                },
                "required": ["labId"],
            },
        ),
        Tool(
            name="get_profiling_tools",
            description="Get recommended profiling tools for a specific platform",
            inputSchema={
                "type": "object",
                "properties": {
                    "platform": {
                        "type": "string",
                        "enum": ["linux", "windows", "macos"],
                        "description": "Operating system platform",
                    },
                },
                "required": ["platform"],
            },
        ),
        Tool(
            name="get_all_resources",
            description="Get complete catalog of all available learning resources",
            inputSchema={
                "type": "object",
                "properties": {},
            },
        ),
        Tool(
            name="search_performance_rules",
            description="Search the repository's normative CPU performance rules (cache, SIMD, branch prediction, IPC, TLB, ROB, frontend, memory latency) by keyword",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Keyword to search for (e.g. 'cache miss', 'vectorization', 'branch misprediction')",
                    },
                },
                "required": ["query"],
            },
        ),
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    """Handle tool calls"""
    if name == "search_optimization_topics":
        results = retrieval_provider.search_topics(arguments["query"])
        return [TextContent(type="text", text=json.dumps(results, indent=2))]

    elif name == "get_learning_path":
        path = retrieval_provider.get_learning_path(arguments["level"])
        result = {
            "level": arguments["level"],
            "recommendedLabs": path,
            "description": f"Recommended learning path for {arguments['level']} level",
        }
        return [TextContent(type="text", text=json.dumps(result, indent=2))]

    elif name == "get_lab_info":
        lab_info = retrieval_provider.get_lab_info(str(arguments["labId"]))
        if lab_info:
            return [TextContent(type="text", text=json.dumps(lab_info, indent=2))]
        return [TextContent(type="text", text=f"Lab '{arguments['labId']}' not found")]

    elif name == "get_profiling_tools":
        tools = retrieval_provider.get_profiling_tools(arguments["platform"])
        result = {"platform": arguments["platform"], "tools": tools}
        return [TextContent(type="text", text=json.dumps(result, indent=2))]

    elif name == "get_all_resources":
        resources = retrieval_provider.get_all_resources()
        return [TextContent(type="text", text=json.dumps(resources, indent=2))]

    elif name == "search_performance_rules":
        results = retrieval_provider.search_performance_rules(arguments["query"])
        return [TextContent(type="text", text=json.dumps(results, indent=2))]

    else:
        raise ValueError(f"Unknown tool: {name}")


async def main():
    """Main entry point"""
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
