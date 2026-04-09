#!/usr/bin/env python3
"""
First Save Celebration — PostToolUse hook for Silverbee.

Fires after the user's first silverbee_crystallize call in a session.
Outputs a one-time congratulatory message with next steps.

Opt-out: SILVERBEE_FEEDBACK_ENABLED=false
"""
import hashlib
import json
import os
import re
import sys
import tempfile


CELEBRATION_MESSAGE = (
    "Workflow saved! You can re-run it anytime with "
    "`/silverbee:run-workflow`, share it with your team, "
    "or turn it into a lead magnet at https://silverbee.ai/lead-magnets."
)


def _safe_session_id(session_id: str) -> str:
    """Sanitize session_id to prevent path traversal."""
    return re.sub(r'[^a-zA-Z0-9_-]', '', session_id)[:64]


def _flag_path(session_id: str) -> str:
    safe_id = _safe_session_id(session_id)
    return os.path.join(
        tempfile.gettempdir(),
        f"silverbee-first-crystallize-{safe_id}.flag",
    )


def main():
    if os.environ.get("SILVERBEE_FEEDBACK_ENABLED", "true").lower() == "false":
        sys.exit(0)

    raw = sys.stdin.read()
    try:
        hook_input = json.loads(raw)
    except json.JSONDecodeError:
        sys.exit(0)

    tool_name = hook_input.get("tool_name", "").lower()

    # Only trigger on Silverbee's crystallize tool
    if "silverbee_crystallize" not in tool_name:
        sys.exit(0)

    # Check for error response — don't celebrate failures
    tool_response = hook_input.get("tool_response", {})
    if isinstance(tool_response, dict):
        if tool_response.get("is_error") or tool_response.get("isError"):
            sys.exit(0)

    session_id = hook_input.get("session_id", "")
    transcript_path = hook_input.get("transcript_path", "")
    if not session_id or session_id == "unknown":  # fallback for environments without session IDs
        session_id = hashlib.sha256(transcript_path.encode()).hexdigest()[:16]

    # Already celebrated this session
    flag = _flag_path(session_id)
    if os.path.exists(flag):
        sys.exit(0)

    # Write flag — failure is non-critical; user may see duplicate message
    try:
        with open(flag, "w") as f:
            f.write("1")
    except OSError:
        pass

    print(json.dumps({
        "decision": "notify",
        "reason": CELEBRATION_MESSAGE,
    }))


if __name__ == "__main__":
    main()
