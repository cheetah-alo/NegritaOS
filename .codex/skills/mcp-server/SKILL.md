---
name: mcp-server
description: >
  Generic MCP server patterns and tool design.
  Trigger: When adding tools, transports, or auth to an MCP server.
license: Apache-2.0
metadata:
  author: generic
  version: "1.0"
  scope: [root, mcp_server]
  auto_invoke: "Working on MCP server tools"
allowed-tools: Read, Edit, Write, Glob, Grep, Bash, WebFetch, WebSearch, Task
---

## Core Rules

- ALWAYS: Keep tool execution side-effect safe and explicit.
- ALWAYS: Validate input payloads.
- NEVER: Log secrets or tokens.

## Structure

```
mcp_server/
├── tools/     # Tool implementations
├── utils/     # Shared utilities
└── server.py  # Entry point
```

## Auth & Transport

- Separate auth from tool logic.
- Support STDIO and HTTP transports where possible.
