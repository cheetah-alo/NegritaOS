# Spreadsheet Runtime Routing

## Codex Desktop

Use the workspace-dependency loader exposed by the Codex app MCP server:

```text
mcp__codex_app__load_workspace_dependencies
```

The older direct dynamic app tool may respond that it is no longer available
and instruct the caller to use the MCP server. Follow that instruction once.
Do not count the MCP call as a repeated attempt against the same unavailable
tool.

After dependency resolution, use the runtime `Spreadsheets` skill and the
returned Node.js and `node_modules` paths. Do not guess bundle paths or import
package internals.

## Claude Code

Claude Code does not inherit Codex Desktop app tools. If its active tools do
not expose the approved spreadsheet runtime:

1. stop XLSX authoring with `BLOCKED_SPREADSHEET_RUNTIME`;
2. preserve the source repo and any prior tracker unchanged;
3. return a handoff containing project name and path, timezone, coverage
   boundary, prior tracker path, deduplicated commit SHAs, evidence inventory,
   confirmed calibrations, requested destinations, and retention candidates;
4. state that no retention deletion has occurred;
5. route the handoff to Codex Gisel for workbook authoring and visual QA.

Do not label this condition `BLOCKED_CONFIG_RESOLUTION` when Brain, catalog,
agent, and profile resolution have succeeded.

## Stop Conditions

- Do not call the same failed dependency loader more than once.
- Do not install or substitute an authoring library automatically.
- Do not emit an XLSX that has not passed formula inspection, complete sheet
  rendering, ZIP integrity, and local/shared SHA-256 comparison.
- Do not delete an older tracker while spreadsheet authoring is blocked.
