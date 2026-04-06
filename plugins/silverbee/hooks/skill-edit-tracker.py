#!/usr/bin/env python3
"""
Skill Edit Tracker — PostToolUse hook

Fires after every tool use. Silently detects when Edit or Write tools
modify a SKILL.md file and accumulates the diffs in a session-scoped
temp file for later feedback submission.
"""
import json
import os
import sys
import tempfile
from datetime import datetime, timezone


def main():
    # ── Opt-out check ─────────────────────────────────────────────────────
    if os.environ.get("SILVERBEE_FEEDBACK_ENABLED", "true").lower() == "false":
        sys.exit(0)

    # ── Skip accumulation if feedback is disabled ──────────────────────────
    # Accumulates by default (local server). Set SILVERBEE_FEEDBACK_ENABLED=false to disable.

    raw = sys.stdin.read()
    try:
        hook_input = json.loads(raw)
    except json.JSONDecodeError:
        sys.exit(0)

    tool_name = hook_input.get("tool_name", "")

    # ── Fast exit for non-file-editing tools ──────────────────────────────
    if tool_name not in ("Edit", "Write"):
        sys.exit(0)

    tool_input = hook_input.get("tool_input", {})
    if not isinstance(tool_input, dict):
        sys.exit(0)

    file_path = tool_input.get("file_path", "")
    if not file_path:
        sys.exit(0)

    # ── Check if this is a skill file ─────────────────────────────────────
    # Match any path containing /skills/<name>/SKILL.md
    parts = file_path.replace("\\", "/").split("/")
    try:
        skills_idx = parts.index("skills")
    except ValueError:
        sys.exit(0)

    # Expect: ...skills/<skill-name>/SKILL.md
    if skills_idx + 2 >= len(parts):
        sys.exit(0)
    if parts[skills_idx + 2] != "SKILL.md":
        sys.exit(0)

    skill_name = parts[skills_idx + 1]

    # ── Build edit record ─────────────────────────────────────────────────
    ts = datetime.now(timezone.utc).isoformat()

    if tool_name == "Edit":
        record = {
            "skill": skill_name,
            "type": "edit",
            "old_string": tool_input.get("old_string", ""),
            "new_string": tool_input.get("new_string", ""),
            "ts": ts,
        }
    else:  # Write
        content = tool_input.get("content", "")
        record = {
            "skill": skill_name,
            "type": "write",
            "content_length": len(content),
            "content_preview": content[:2000],
            "ts": ts,
        }

    # ── Derive session key ────────────────────────────────────────────────
    session_id = hook_input.get("session_id", "")
    transcript_path = hook_input.get("transcript_path", "")
    if not session_id or session_id == "unknown":
        session_id = str(abs(hash(transcript_path)))

    # ── Append to session accumulator ─────────────────────────────────────
    accumulator_path = os.path.join(
        tempfile.gettempdir(),
        f"silverbee-skill-edits-{session_id}.jsonl",
    )
    try:
        with open(accumulator_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
    except OSError:
        sys.exit(0)


if __name__ == "__main__":
    main()
