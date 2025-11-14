#!/usr/bin/env python3
"""MCP server providing RAG capabilities for CPU optimization learning resources"""

import asyncio
import json
import os
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    Resource,
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
)

from knowledge_base import LEARNING_RESOURCES


class SimpleRetrievalProvider:
    """Simple keyword-based retrieval provider"""
    
    def __init__(self):
        self.resources = LEARNING_RESOURCES
    
    def search_topics(self, query: str) -> dict[str, Any]:
        """Search for topics matching the query"""
        query_lower = query.lower()
        results = {
            "books": [],
            "onlineResources": [],
            "projects": [],
            "labs": []
        }
        
        # Search books
        for book in self.resources["books"]:
            if any(query_lower in topic.lower() for topic in book["topics"]) or \
               query_lower in book["title"].lower() or \
               query_lower in book["description"].lower():
                results["books"].append(book)
        
        # Search online resources
        for resource in self.resources["onlineResources"]:
            if any(query_lower in topic.lower() for topic in resource["topics"]) or \
               query_lower in resource["title"].lower() or \
               query_lower in resource["description"].lower():
                results["onlineResources"].append(resource)
        
        # Search projects
        for project in self.resources["projects"]:
            if any(query_lower in topic.lower() for topic in project["topics"]) or \
               query_lower in project["title"].lower() or \
               query_lower in project["description"].lower():
                results["projects"].append(project)
        
        # Search labs
        for lab in self.resources["labs"]:
            if any(query_lower in topic.lower() for topic in lab["topics"]) or \
               query_lower in lab["title"].lower() or \
               query_lower in lab["description"].lower():
                results["labs"].append(lab)
        
        return results
    
    def get_learning_path(self, level: str) -> list[dict[str, Any]]:
        """Get recommended learning path based on skill level"""
        return [lab for lab in self.resources["labs"] if lab["level"] == level]
    
    def get_lab_info(self, lab_number: int) -> dict[str, Any] | None:
        """Get detailed information about a specific lab"""
        if 1 <= lab_number <= len(self.resources["labs"]):
            return self.resources["labs"][lab_number - 1]
        return None
    
    def get_profiling_tools(self, platform: str) -> list[dict[str, Any]]:
        """Get profiling tools for a specific platform"""
        return self.resources["tools"].get(platform, [])
    
    def get_all_resources(self) -> dict[str, Any]:
        """Get all resources"""
        return self.resources


# Initialize the retrieval provider
retrieval_provider = SimpleRetrievalProvider()

# Create the MCP server
app = Server("cpu-optimization-rag-server")


@app.list_resources()
async def list_resources() -> list[Resource]:
    """List available resources"""
    return [
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
    ]


@app.read_resource()
async def read_resource(uri: str) -> str:
    """Read a specific resource"""
    if uri == "cpu-opt://resources/all":
        return json.dumps(LEARNING_RESOURCES, indent=2)
    elif uri == "cpu-opt://labs/overview":
        return json.dumps(LEARNING_RESOURCES["labs"], indent=2)
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
            description="Get detailed information about a specific lab exercise",
            inputSchema={
                "type": "object",
                "properties": {
                    "labNumber": {
                        "type": "number",
                        "description": "Lab number (1-8)",
                        "minimum": 1,
                        "maximum": 8,
                    },
                },
                "required": ["labNumber"],
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
            "description": f"Recommended learning path for {arguments['level']} level"
        }
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    
    elif name == "get_lab_info":
        lab_info = retrieval_provider.get_lab_info(arguments["labNumber"])
        if lab_info:
            return [TextContent(type="text", text=json.dumps(lab_info, indent=2))]
        else:
            return [TextContent(type="text", text=f"Lab {arguments['labNumber']} not found")]
    
    elif name == "get_profiling_tools":
        tools = retrieval_provider.get_profiling_tools(arguments["platform"])
        result = {
            "platform": arguments["platform"],
            "tools": tools
        }
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    
    elif name == "get_all_resources":
        resources = retrieval_provider.get_all_resources()
        return [TextContent(type="text", text=json.dumps(resources, indent=2))]
    
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
