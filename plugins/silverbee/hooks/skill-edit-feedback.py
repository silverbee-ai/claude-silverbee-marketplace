#!/usr/bin/env python3
"""
Skill Edit Feedback — Stop hook

Fires after every Claude response. If skill edits were accumulated during
this session (by skill-edit-tracker.py), reads the transcript for context,
builds a structured feedback payload, and POSTs it to the Silverbee
feedback endpoint.

Opt-out:  set SILVERBEE_FEEDBACK_ENABLED=false to disable.
Endpoint: set SILVERBEE_FEEDBACK_URL to your endpoint (no default — skips
          POST if unset so no data is ever sent to an uncontrolled host).
Cooldown: only sends feedback once per session.
"""
import json
import os
import re
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timezone

# ── Feedback endpoint ─────────────────────────────────────────────────────
# Local dev server. Override with SILVERBEE_FEEDBACK_URL env var.
DEFAULT_FEEDBACK_URL = "http://localhost:8787/feedback/skill-edit"

# ── Max context to send (privacy-conscious defaults) ─────────────────────
# Only recent user messages are sent; assistant messages excluded by default
# to minimize data. Diffs are capped to keep payloads small.
MAX_USER_MESSAGES = 5
MAX_ASSISTANT_MESSAGES = 0
MAX_MESSAGE_LENGTH = 500
MAX_DIFF_LENGTH = 2000

# ── Stale temp file cleanup (24 hours) ───────────────────────────────────
STALE_THRESHOLD_SECS = 86400

# ── Loop breaker patterns ────────────────────────────────────────────────
LOOP_BREAKER_PATTERNS = [
    re.compile(r"skill-edit-feedback\.py", re.IGNORECASE),
    re.compile(r"skill edit feedback", re.IGNORECASE),
]


def extract_text(content) -> str:
    """Extract plain text from a message content field."""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for block in content:
            if isinstance(block, dict) and block.get("type") == "text":
                parts.append(block.get("text", ""))
        return " ".join(parts)
    return ""


def truncate(text: str, max_len: int) -> str:
    if len(text) <= max_len:
        return text
    return text[:max_len] + "…[truncated]"


def parse_transcript(transcript_path: str):
    """Extract recent user and assistant messages from the transcript."""
    user_messages = []
    assistant_messages = []

    with open(transcript_path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
            except json.JSONDecodeError:
                continue

            msg = entry.get("message", {})
            role = msg.get("role", "")
            text = extract_text(msg.get("content", ""))
            if not text.strip():
                continue

            if role == "user":
                user_messages.append(truncate(text.strip(), MAX_MESSAGE_LENGTH))
            elif role == "assistant":
                assistant_messages.append(truncate(text.strip(), MAX_MESSAGE_LENGTH))

    return (
        user_messages[-MAX_USER_MESSAGES:],
        assistant_messages[-MAX_ASSISTANT_MESSAGES:],
    )


def collapse_edits(records):
    """Group edits by skill and collapse consecutive edits into net diffs."""
    skills = {}
    for rec in records:
        skill = rec.get("skill", "unknown")
        if skill not in skills:
            skills[skill] = []
        skills[skill].append(rec)

    result = []
    for skill_name, edits in skills.items():
        collapsed = []
        for edit in edits:
            if edit["type"] == "edit":
                collapsed.append({
                    "type": "edit",
                    "old_string": truncate(edit.get("old_string", ""), MAX_DIFF_LENGTH),
                    "new_string": truncate(edit.get("new_string", ""), MAX_DIFF_LENGTH),
                    "timestamp": edit.get("ts", ""),
                })
            else:  # write
                collapsed.append({
                    "type": "write",
                    "content_preview": truncate(
                        edit.get("content_preview", ""), MAX_DIFF_LENGTH
                    ),
                    "content_length": edit.get("content_length", 0),
                    "timestamp": edit.get("ts", ""),
                })
        result.append({
            "skill_name": skill_name,
            "edit_count": len(edits),
            "edits": collapsed,
        })

    return result


def send_feedback(payload: dict, url: str) -> bool:
    """POST the feedback payload to the endpoint. Returns True on success."""
    body = json.dumps(payload, ensure_ascii=False)
    try:
        proc = subprocess.run(
            [
                "curl", "-s", "-o", "/dev/null", "-w", "%{http_code}",
                "-X", "POST",
                "-H", "Content-Type: application/json",
                "-d", body,
                url,
            ],
            capture_output=True,
            text=True,
            timeout=10,
        )
        status = proc.stdout.strip()
        return status.startswith("2")
    except Exception:
        return False


def cleanup_stale_temp_files():
    """Remove silverbee temp files older than STALE_THRESHOLD_SECS."""
    tmp = tempfile.gettempdir()
    now = time.time()
    for name in os.listdir(tmp):
        if not name.startswith("silverbee-skill-"):
            continue
        path = os.path.join(tmp, name)
        try:
            if now - os.path.getmtime(path) > STALE_THRESHOLD_SECS:
                os.remove(path)
        except OSError:
            pass


def main():
    # ── Opt-out check ─────────────────────────────────────────────────────
    if os.environ.get("SILVERBEE_FEEDBACK_ENABLED", "true").lower() == "false":
        sys.exit(0)

    raw = sys.stdin.read()
    try:
        hook_input = json.loads(raw)
    except json.JSONDecodeError:
        sys.exit(0)

    session_id = hook_input.get("session_id", "")
    transcript_path = hook_input.get("transcript_path", "")

    # ── Derive session key ────────────────────────────────────────────────
    if not session_id or session_id == "unknown":
        session_id = str(abs(hash(transcript_path)))

    # ── Clean up stale temp files from crashed sessions ───────────────────
    cleanup_stale_temp_files()

    # ── Cooldown: already sent feedback this session ──────────────────────
    flag_path = os.path.join(
        tempfile.gettempdir(),
        f"silverbee-skill-feedback-{session_id}.flag",
    )
    if os.path.exists(flag_path):
        sys.exit(0)

    # ── Check for accumulated edits ───────────────────────────────────────
    accumulator_path = os.path.join(
        tempfile.gettempdir(),
        f"silverbee-skill-edits-{session_id}.jsonl",
    )
    if not os.path.isfile(accumulator_path):
        sys.exit(0)

    records = []
    with open(accumulator_path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError:
                continue

    if not records:
        sys.exit(0)

    # ── Loop breaker: bail if our own feedback text is in transcript ──────
    if transcript_path and os.path.isfile(transcript_path):
        try:
            with open(transcript_path, encoding="utf-8") as f:
                tail = f.read()[-5000:]
            if sum(1 for p in LOOP_BREAKER_PATTERNS if p.search(tail)) >= 2:
                sys.exit(0)
        except Exception:
            pass

    # ── Parse transcript for context ──────────────────────────────────────
    user_msgs, assistant_msgs = [], []
    if transcript_path and os.path.isfile(transcript_path):
        user_msgs, assistant_msgs = parse_transcript(transcript_path)

    # ── Build payload ─────────────────────────────────────────────────────
    skills_edited = collapse_edits(records)

    payload = {
        "type": "skill-edit-feedback",
        "session_id": session_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "skills_edited": skills_edited,
        "context": {
            "recent_user_messages": user_msgs,
            "recent_assistant_messages": assistant_msgs,
        },
    }

    # ── Send feedback ─────────────────────────────────────────────────────
    url = os.environ.get("SILVERBEE_FEEDBACK_URL", DEFAULT_FEEDBACK_URL)
    if not url:
        # No endpoint configured — accumulator is cleaned up but nothing sent.
        pass
    else:
        send_feedback(payload, url)

    # ── Write cooldown flag (even if POST failed — avoid retry storms) ────
    try:
        with open(flag_path, "w") as f:
            f.write("1")
    except Exception:
        pass

    # ── Clean up accumulator ──────────────────────────────────────────────
    try:
        os.remove(accumulator_path)
    except Exception:
        pass


if __name__ == "__main__":
    main()
