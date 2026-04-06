---
description: Run a Silverbee SEO workflow by name
---

## CRITICAL — read before doing anything

**Rule 1 — No subagents.** You are the executor. Run every step yourself in
this conversation. Never use the Agent tool or delegate to any subagent.

**Rule 2 — Output after every tool call.** After every single `run_action`,
output one line of plain text before making the next call. Never let more
than 15 seconds pass without giving the user a visible update.

---

## Steps

1. Load and follow the `supervisor` skill (call `get_instructions` first).

2. Load and follow the `run-workflow` skill for the complete workflow execution
   protocol, including discovery, confirmation, and execution rules.

3. If no workflow name is provided in `$ARGUMENTS`: discover available workflows
   and present them as a numbered list for the user to choose from.

4. If a workflow name is provided: announce it to the user, then execute each
   stage one at a time using `run_action` — outputting a status line after
   every single call.
