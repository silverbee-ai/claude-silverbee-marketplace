---
name: seo-supervisor
description: DEPRECATED — do not use this as an agent or subagent. Load the supervisor skill instead.
---

This agent definition is intentionally disabled.

All SEO orchestration logic has been moved to the `supervisor` skill so it
runs directly in the main conversation (no subagent black-box).

If you are reading this, load `read_skill("supervisor")` and execute the
task yourself in the current conversation. Do NOT spawn a subagent.
