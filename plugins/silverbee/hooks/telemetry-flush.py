#!/usr/bin/env python3
"""
Telemetry Flush — Stop hook for Silverbee.

Flushes any remaining buffered telemetry events to the batch endpoint
when the session ends. Also cleans up temp files.

Opt-out:  SILVERBEE_FEEDBACK_ENABLED=false
Endpoint: SILVERBEE_FEEDBACK_URL
"""
import json
import os
import sys
import tempfile
import time

# ── Import shared modules ───────────────────────────────────────────────────
sys.path.insert(0, os.path.dirname(__file__))
from _user_id import resolve_user_id

# Re-use flush logic from tracker
from importlib.util import spec_from_file_location, module_from_spec

_tracker_path = os.path.join(os.path.dirname(__file__), "telemetry-tracker.py")
_spec = spec_from_file_location("telemetry_tracker", _tracker_path)
_tracker = module_from_spec(_spec)
_spec.loader.exec_module(_tracker)

flush_events = _tracker.flush_events

# ── Stale temp file cleanup (24 hours) ──────────────────────────────────────
STALE_THRESHOLD_SECS = 86400


def cleanup_stale_temp_files():
    """Remove silverbee telemetry temp files older than 24 hours."""
    tmp = tempfile.gettempdir()
    now = time.time()
    for name in os.listdir(tmp):
        if not name.startswith("silverbee-telemetry-") and \
           not name.startswith("silverbee-current-skill-") and \
           not name.startswith("silverbee-tool-start-"):
            continue
        path = os.path.join(tmp, name)
        try:
            if now - os.path.getmtime(path) > STALE_THRESHOLD_SECS:
                os.remove(path)
        except OSError:
            pass


def main():
    if os.environ.get("SILVERBEE_FEEDBACK_ENABLED", "true").lower() == "false":
        sys.exit(0)

    raw = sys.stdin.read()
    try:
        hook_input = json.loads(raw)
    except json.JSONDecodeError:
        sys.exit(0)

    session_id = hook_input.get("session_id", "")
    transcript_path = hook_input.get("transcript_path", "")

    if not session_id or session_id == "unknown":
        session_id = str(abs(hash(transcript_path)))

    # ── Flush remaining events ───────────────────────────────────────────
    url = os.environ.get("SILVERBEE_FEEDBACK_URL", "")
    if url:
        flush_events(session_id, url)

    # ── Clean up session temp files ──────────────────────────────────────
    tmp = tempfile.gettempdir()
    for prefix in [
        f"silverbee-telemetry-{session_id}",
        f"silverbee-telemetry-flush-{session_id}",
        f"silverbee-current-skill-{session_id}",
    ]:
        path = os.path.join(tmp, prefix)
        for suffix in ["", ".jsonl", ".ts"]:
            p = path + suffix if suffix else path
            try:
                if os.path.exists(p):
                    os.remove(p)
            except OSError:
                pass

    # Also clean tool-start files for this session
    for name in os.listdir(tmp):
        if name.startswith(f"silverbee-tool-start-{session_id}-"):
            try:
                os.remove(os.path.join(tmp, name))
            except OSError:
                pass

    # ── Clean up stale files from old sessions ───────────────────────────
    cleanup_stale_temp_files()


if __name__ == "__main__":
    main()
