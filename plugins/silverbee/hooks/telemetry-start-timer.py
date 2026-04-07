#!/usr/bin/env python3
"""
Telemetry Start Timer — PreToolUse hook for Silverbee.

Records the start timestamp for all tool calls so that
telemetry-tracker.py (PostToolUse) can compute duration_ms.
"""
import json
import os
import sys
import tempfile
import time


def main():
    if os.environ.get("SILVERBEE_FEEDBACK_ENABLED", "true").lower() == "false":
        sys.exit(0)

    raw = sys.stdin.read()
    try:
        hook_input = json.loads(raw)
    except json.JSONDecodeError:
        sys.exit(0)

    tool_name = hook_input.get("tool_name", "")
    # Skip internal tools
    if tool_name in {"ToolSearch", "TaskList", "TaskGet"}:
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
