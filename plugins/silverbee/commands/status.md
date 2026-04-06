---
description: Check Silverbee connection status and available data sources
allowed-tools: mcp__silverbee__list_available_apps
---

## CRITICAL — read before doing anything

**Rule 1 — No subagents.** You are the executor. Run every step yourself in
this conversation. Never use the Agent tool or delegate to any subagent.

**Rule 2 — Output after every tool call.** After every single tool call,
output one line of plain text before making the next call. Never let more
than 15 seconds pass without giving the user a visible update.

---

## Steps

1. Output this message first, before any tool call:
   > "Checking Silverbee connection and available data sources..."

2. Call `list_available_apps` to verify connectivity and see which integrations
   are connected. While waiting, check if `.silverbee.json` exists in the
   working directory.

3. Present a single status summary:

   **MCP server:** reachable or not (based on whether `list_available_apps` succeeded)

   **Data sources** (table from `list_available_apps` response):
   | Source | Status |
   |--------|--------|
   | Google Search Console | ✓ Connected |
   | Ahrefs | ✗ Not connected |

   **Project config:** If `.silverbee.json` exists, show the domain and
   competitors. If not, mention it can be created for project defaults.
