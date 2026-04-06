---
description: Keyword research with Ahrefs, SERP, and cannib check
---

## CRITICAL — read before doing anything

**Rule 1 — No subagents.** You are the executor. Run every step yourself in
this conversation. Never use the Agent tool or delegate to any subagent.
All `run_action` calls must happen here so the user sees each one in real time.

**Rule 2 — Output after every tool call.** After every single `run_action`,
output one line of plain text before making the next call. Never batch two
tool calls back-to-back without text in between. 15 seconds of silence is
too long.

---

## Steps

1. Output this message first, before any tool call:
   > "🔍 Starting keyword research for **$ARGUMENTS**. I'll pull data from Ahrefs, GSC, and DataForSEO — this takes 3–6 minutes. You'll see a status update after each step."

2. Load and follow the `supervisor` skill (call `get_instructions`, then run MCP tools).

3. Load and follow the `keyword-research` skill for the full research protocol.

4. After all data is collected, load `seo-output-formatter` and follow its
   three-layer output: call `show_generative_ui` with the keyword-research
   dashboard spec (Layer 1), write the HTML report (Layer 2), then output
   the full markdown deliverable (Layer 3).
