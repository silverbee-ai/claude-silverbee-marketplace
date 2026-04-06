---
description: SEO-optimize content with keywords and metadata
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
   > "🔍 Analyzing content for **$ARGUMENTS**. Checking keyword gaps, density, and metadata — this takes 1–3 minutes. You'll see a status update after each step."

2. Load and follow the `supervisor` skill (call `get_instructions`, then run MCP tools).

3. Load and follow the `content-optimization` skill for the full optimization protocol.

4. After all data is collected, load `seo-output-formatter` and follow its
   three-layer output: call `show_generative_ui` with the content-optimization
   dashboard spec (Layer 1), write the HTML report (Layer 2), then output
   the full markdown deliverable (Layer 3).
