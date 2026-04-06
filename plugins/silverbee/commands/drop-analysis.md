---
description: Diagnose a traffic or ranking drop
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
   > "🔍 Diagnosing traffic drop for **$ARGUMENTS**. Comparing periods, checking algorithm updates, and identifying affected pages — this takes 2–4 minutes. You'll see a status update after each step."

2. Load and follow the `supervisor` skill (call `get_instructions`, then run MCP tools).

3. Load and follow the `drop-analysis` skill for the full diagnosis protocol.

4. Present the findings as a structured diagnosis with timeline, affected areas,
   root cause analysis, and recovery recommendations.
