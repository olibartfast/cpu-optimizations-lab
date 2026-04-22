# mcp-kb-editor

## Purpose

Maintain the static MCP learning-resource knowledge base in a way that stays consistent
with the server's schema and search behavior.

## Use When

- Adding a new learning resource
- Editing resource metadata
- Improving discoverability of existing knowledge-base entries

## Inputs

- Resource metadata and URL
- Target topics and level
- Existing knowledge-base structure

## Outputs

- A valid `knowledge_base.py` update
- Consistent metadata fields
- Keyword-rich descriptions that improve substring search

## Constraints

- Edit `mcp-server/knowledge_base.py` directly
- Keep entries JSON-serializable through the MCP toolchain
- Include `id`, `title`, `topics`, `description`, `level`, `url`, and `author`
