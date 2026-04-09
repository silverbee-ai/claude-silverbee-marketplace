#!/usr/bin/env python3
"""
Telemetry Start Timer — PreToolUse hook for Silverbee.

Records the start timestamp for Silverbee tool calls so that
telemetry-tracker.py (PostToolUse) can compute duration_ms.

Only Silverbee MCP tools are timed — non-Silverbee tools are skipped
since they are not tracked (Directory Policy §1D).
"""
import json
import os
import sys
import tempfile
import time

# ── Known Silverbee MCP operation suffixes (mirrors telemetry-tracker.py) ──
SILVERBEE_OPS = {
    "run_action", "run_action_batch", "run_action_ui",
    "run_multi_actions", "run_multi_actions_ui",
    "list_available_apps", "list_actions", "search_actions",
    "get_instructions", "list_skills", "get_skill", "get_skill_content",
    "add_skill", "get_context", "list_contexts", "add_context", "search_contexts",
    "show_generative_ui", "render_template",
    "silverbee_crystallize", "silverbee_get_leads",
    "silverbee_publish", "silverbee_register", "silverbee_update_profile",
}


def _is_silverbee_tool(tool_name: str) -> bool:
    lower = tool_name.lower()
    if "silverbee" in lower:
        return True
    if lower.startswith("mcp__"):
        parts = lower.split("__")
        if len(parts) >= 3:
            op = parts[-1]
            return op in SILVERBEE_OPS
    return False


def main():
    if os.environ.get("SILVERBEE_FEEDBACK_ENABLED", "true").lower() == "false":
        sys.exit(0)

    raw = sys.stdin.read()
    try:
        hook_input = json.loads(raw)
    except json.JSONDecodeError:
        sys.exit(0)

    tool_name = hook_input.get("tool_name", "")
    if not tool_name:
        sys.exit(0)

    # Only time Silverbee tools
    if not _is_silverbee_tool(tool_name):
        sys.exit(0)

    session_id = hook_input.get("session_id", "")
    transcript_path = hook_input.get("transcript_path", "")
    if not session_id or session_id == "unknown":
        session_id = str(abs(hash(transcript_path)))

    # Write start timestamp
    safe = tool_name.replace("/", "_").replace(" ", "_")[:80]
    path = os.path.join(
        tempfile.gettempdir(),
        f"silverbee-tool-start-{session_id}-{safe}.ts",
    )
    try:
        with open(path, "w") as f:
            f.write(str(time.time()))
    except OSError:
        pass


if __name__ == "__main__":
    main()
