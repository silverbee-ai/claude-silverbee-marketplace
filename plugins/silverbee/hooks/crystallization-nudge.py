#!/usr/bin/env python3
"""
Crystallization Nudge — PostToolUse hook for Silverbee MCP tools.

Counts Silverbee MCP tool calls per session using a temp file counter.
After the 5th successful tool call, outputs a one-time nudge suggesting
the user save/crystallize their workflow.

Simple, stateless (per session), and doesn't parse transcripts.
"""
import json
import os
import sys
import tempfile


# Minimum Silverbee tool calls before nudging
THRESHOLD = 5

NUDGE_MESSAGE = (
    "You've built a multi-step workflow this session. "
    "Want to save it for reuse? Use `/silverbee:run-workflow save` to crystallize it "
    "— then re-run it anytime or turn it into a shareable template "
    "at https://silverbee.ai/workflows."
)


def get_counter_path(session_id: str) -> str:
    return os.path.join(
        tempfile.gettempdir(),
        f"silverbee-tool-count-{session_id}",
    )


def get_flag_path(session_id: str) -> str:
    return os.path.join(
        tempfile.gettempdir(),
        f"silverbee-nudge-done-{session_id}.flag",
    )


def main():
    raw = sys.stdin.read()
    try:
        hook_input = json.loads(raw)
    except json.JSONDecodeError:
        sys.exit(0)

    tool_name = hook_input.get("tool_name", "")

    # Only count Silverbee MCP tools (name format varies by environment:
    # "mcp__silverbee-mcp__run_action", "silverbee__run_action", "silverbee run_action", etc.)
    tool_lower = tool_name.lower()
    if "silverbee" not in tool_lower:
        sys.exit(0)

    # Skip non-data tools (UI calls, context, catalog queries)
    skip_keywords = [
        "get_instructions", "list_available_apps", "list_actions",
        "search_actions", "show_generative_ui",
        "get_context", "list_contexts", "add_context",
        "search_contexts",
    ]
    if any(kw in tool_lower for kw in skip_keywords):
        sys.exit(0)

    # Derive session key
    session_id = hook_input.get("session_id", "")
    transcript_path = hook_input.get("transcript_path", "")
    if not session_id or session_id == "unknown":
        session_id = str(abs(hash(transcript_path)))

    # Already nudged this session — exit silently
    flag_path = get_flag_path(session_id)
    if os.path.exists(flag_path):
        sys.exit(0)

    # Increment counter
    counter_path = get_counter_path(session_id)
    count = 0
    try:
        with open(counter_path, "r") as f:
            count = int(f.read().strip())
    except (OSError, ValueError):
        pass

    count += 1

    try:
        with open(counter_path, "w") as f:
            f.write(str(count))
    except OSError:
        sys.exit(0)

    # Not at threshold yet
    if count < THRESHOLD:
        sys.exit(0)

    # Write flag so we never nudge again this session
    try:
        with open(flag_path, "w") as f:
            f.write("1")
    except OSError:
        pass  # If flag can't be written, nudge may fire again — acceptable

    # Output the nudge
    print(json.dumps({
        "decision": "notify",
        "reason": NUDGE_MESSAGE,
    }))


if __name__ == "__main__":
    main()
