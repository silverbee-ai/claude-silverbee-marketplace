#!/usr/bin/env python3
"""
Telemetry Tracker — PostToolUse hook for Silverbee.

Captures two event types:
  - skill-usage:     fires when the Skill tool is invoked
  - tool-execution:  fires when a Silverbee MCP tool completes

Events are buffered in a JSONL temp file and flushed to the batch
endpoint when the buffer reaches 20 events or 30 seconds have elapsed
since the last flush.

Opt-out:  SILVERBEE_FEEDBACK_ENABLED=false
Endpoint: SILVERBEE_FEEDBACK_URL (no default — events accumulate but
          are never sent if unset)
"""
import json
import os
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timezone

# ── Import shared user ID resolver ──────────────────────────────────────────
sys.path.insert(0, os.path.dirname(__file__))
from _user_id import resolve_user_id

# ── Production defaults ─────────────────────────────────────────────────────
DEFAULT_FEEDBACK_URL = "https://web-production-991bd.up.railway.app"
DEFAULT_FEEDBACK_TOKEN = "4kjxV0oSog_mzaKzXy1yPvLec-lZGWYRJ953jZl1T34"

# ── Buffer flush thresholds ─────────────────────────────────────────────────
BATCH_SIZE = 20
FLUSH_INTERVAL_SECS = 30

# ── Skip tools (metadata / UI — not worth tracking) ────────────────────────
SKIP_KEYWORDS = [
    "get_instructions", "list_available_apps", "list_actions",
    "search_actions", "show_generative_ui",
    "get_context", "list_contexts", "add_context",
    "search_contexts",
]


def _buffer_path(session_id: str) -> str:
    return os.path.join(
        tempfile.gettempdir(),
        f"silverbee-telemetry-{session_id}.jsonl",
    )


def _flush_ts_path(session_id: str) -> str:
    return os.path.join(
        tempfile.gettempdir(),
        f"silverbee-telemetry-flush-{session_id}.ts",
    )


def _current_skill_path(session_id: str) -> str:
    """Tracks the most recently invoked skill for attribution."""
    return os.path.join(
        tempfile.gettempdir(),
        f"silverbee-current-skill-{session_id}",
    )


def _start_time_path(session_id: str, tool_name: str) -> str:
    """Per-tool start timestamp for duration calculation."""
    safe = tool_name.replace("/", "_").replace(" ", "_")[:80]
    return os.path.join(
        tempfile.gettempdir(),
        f"silverbee-tool-start-{session_id}-{safe}.ts",
    )


def _read_current_skill(session_id: str) -> str:
    try:
        with open(_current_skill_path(session_id), "r") as f:
            return f.read().strip()
    except OSError:
        return ""


def _write_current_skill(session_id: str, skill_name: str):
    try:
        with open(_current_skill_path(session_id), "w") as f:
            f.write(skill_name)
    except OSError:
        pass


def _append_event(session_id: str, event: dict):
    """Append an event to the session buffer."""
    try:
        with open(_buffer_path(session_id), "a") as f:
            f.write(json.dumps(event, ensure_ascii=False) + "\n")
    except OSError:
        pass


def _read_and_clear_buffer(session_id: str) -> list:
    """Read all buffered events and truncate the file."""
    path = _buffer_path(session_id)
    events = []
    try:
        with open(path, "r") as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        events.append(json.loads(line))
                    except json.JSONDecodeError:
                        continue
        # Truncate
        with open(path, "w") as f:
            pass
    except OSError:
        pass
    return events


def _buffer_size(session_id: str) -> int:
    path = _buffer_path(session_id)
    try:
        with open(path, "r") as f:
            return sum(1 for line in f if line.strip())
    except OSError:
        return 0


def _last_flush_time(session_id: str) -> float:
    try:
        with open(_flush_ts_path(session_id), "r") as f:
            return float(f.read().strip())
    except (OSError, ValueError):
        return 0.0


def _update_flush_time(session_id: str):
    try:
        with open(_flush_ts_path(session_id), "w") as f:
            f.write(str(time.time()))
    except OSError:
        pass


def _should_flush(session_id: str) -> bool:
    if _buffer_size(session_id) >= BATCH_SIZE:
        return True
    last = _last_flush_time(session_id)
    if last == 0.0:
        return False
    return (time.time() - last) >= FLUSH_INTERVAL_SECS


def flush_events(session_id: str, url: str) -> bool:
    """Send buffered events to the batch endpoint. Returns True on success."""
    events = _read_and_clear_buffer(session_id)
    if not events:
        return True

    token = os.environ.get("SILVERBEE_FEEDBACK_TOKEN", DEFAULT_FEEDBACK_TOKEN)
    payload = {"events": events}
    body = json.dumps(payload, ensure_ascii=False)

    cmd = [
        "curl", "-s", "-o", "/dev/null", "-w", "%{http_code}",
        "-X", "POST",
        "-H", "Content-Type: application/json",
        "-d", body,
    ]
    if token:
        cmd.extend(["-H", f"Authorization: Bearer {token}"])
    cmd.append(f"{url}/events/batch")

    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        status = proc.stdout.strip()
        if status.startswith("2"):
            _update_flush_time(session_id)
            return True

        # On failure, re-buffer the events so they aren't lost
        for event in events:
            _append_event(session_id, event)
        return False
    except Exception:
        # Re-buffer on error
        for event in events:
            _append_event(session_id, event)
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
    tool_input = hook_input.get("tool_input", {})
    session_id = hook_input.get("session_id", "")
    transcript_path = hook_input.get("transcript_path", "")

    if not session_id or session_id == "unknown":
        session_id = str(abs(hash(transcript_path)))

    now = datetime.now(timezone.utc).isoformat()
    user_id = resolve_user_id()

    # ── Skill invocation tracking ────────────────────────────────────────
    if tool_name == "Skill":
        skill_name = ""
        if isinstance(tool_input, dict):
            skill_name = tool_input.get("skill", "")
        if skill_name:
            _write_current_skill(session_id, skill_name)
            _append_event(session_id, {
                "type": "skill-usage",
                "user_id": user_id,
                "skill_name": skill_name,
                "session_id": session_id,
                "timestamp": now,
                "duration_ms": None,
                "metadata": {},
            })
            # Initialize flush timer on first event if needed
            if _last_flush_time(session_id) == 0.0:
                _update_flush_time(session_id)

    # ── Silverbee MCP tool execution tracking ────────────────────────────
    tool_lower = tool_name.lower()
    if "silverbee" in tool_lower:
        if not any(kw in tool_lower for kw in SKIP_KEYWORDS):
            # Determine status from tool_response
            tool_response = hook_input.get("tool_response", {})
            status = "success"
            if isinstance(tool_response, dict):
                if tool_response.get("is_error") or tool_response.get("isError"):
                    status = "error"
            elif isinstance(tool_response, str) and "error" in tool_response.lower():
                status = "error"

            # Read duration from start timestamp if available
            duration_ms = None
            start_path = _start_time_path(session_id, tool_name)
            try:
                with open(start_path, "r") as f:
                    start_ts = float(f.read().strip())
                duration_ms = int((time.time() - start_ts) * 1000)
                os.remove(start_path)
            except (OSError, ValueError):
                pass

            current_skill = _read_current_skill(session_id)

            _append_event(session_id, {
                "type": "tool-execution",
                "user_id": user_id,
                "tool_name": tool_name,
                "skill_name": current_skill or None,
                "session_id": session_id,
                "timestamp": now,
                "status": status,
                "duration_ms": duration_ms,
                "metadata": {},
            })
            # Initialize flush timer on first event if needed
            if _last_flush_time(session_id) == 0.0:
                _update_flush_time(session_id)

    # ── Conditional flush ────────────────────────────────────────────────
    url = os.environ.get("SILVERBEE_FEEDBACK_URL", DEFAULT_FEEDBACK_URL)
    if url and _should_flush(session_id):
        flush_events(session_id, url)


if __name__ == "__main__":
    main()
