---
description: Gap analysis vs a competitor (keywords, content, links)
---

## CRITICAL — read before doing anything

**Rule 1 — No subagents.** You are the executor. Run every step yourself in
this conversation. Never use the Agent tool or delegate to any subagent.

**Rule 2 — Output after every tool call.** After every single `run_action`,
output one line of plain text before making the next call. Never let more
than 15 seconds pass without giving the user a visible update.

---

## Steps

1. Output this message first, before any tool call:
   > "🔍 Starting competitor analysis for **$ARGUMENTS**. Comparing keyword coverage, content gaps, and backlinks — this takes 3–5 minutes. You'll see a status update after each step."

2. Load and follow the `supervisor` skill (call `get_instructions`, then run MCP tools).

3. Load and follow the `competitor-analysis` skill for the full comparison protocol.

4. After all data is collected, load `seo-output-formatter` and follow its
   three-layer output: call `show_generative_ui` with the competitor-analysis
   dashboard spec (Layer 1), write the HTML report (Layer 2), then output
   the full markdown deliverable (Layer 3).
