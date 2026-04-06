#!/usr/bin/env python3
"""
Methodology Nudge — Stop hook for Silverbee.

After a session delivers a complete structured output (≥5 tool calls of
any kind), scans the transcript for behavioral signals that the user
demonstrated an original workflow methodology.

Behavioral signals:
  - User defined a sequence or approach before the assistant suggested one
  - User redirected using domain-specific reasoning
  - User named or applied a framework not introduced by the assistant
  - Phrases: "I always...", "I never...", "before doing X I need Y",
    "my process is...", "the way to do this is...", etc.

If triggered, appends:
  "Looks like you have your own methodology here — want to turn this
   into a lead magnet?"

Re-offer guard: after triggering, will not fire again unless:
  - The user explicitly asks (mentions lead magnet, save methodology, etc.)
  - OR 15+ user messages have been sent since the last nudge
"""
import json
import os
import re
import sys
import tempfile

# ── Thresholds ──────────────────────────────────────────────────────────────
TOOL_THRESHOLD = 5
REFIRE_MESSAGE_GAP = 15
MAX_MESSAGE_LENGTH = 1000

# ── Behavioral signal patterns (matched against user messages) ──────────────
METHODOLOGY_PATTERNS = [
    # Explicit process declarations
    re.compile(r"\bI always\b", re.IGNORECASE),
    re.compile(r"\bI never\b", re.IGNORECASE),
    re.compile(r"\bmy process\b", re.IGNORECASE),
    re.compile(r"\bmy (workflow|approach|methodology|framework|method|system)\b", re.IGNORECASE),
    re.compile(r"\bthe way (I|we) do (this|it|things)\b", re.IGNORECASE),
    re.compile(r"\bthe way to do (this|it)\b", re.IGNORECASE),
    re.compile(r"\bbefore (doing|I do|we do|running|I run)\b", re.IGNORECASE),
    re.compile(r"\bafter (doing|I do|we do|running|I run)\b", re.IGNORECASE),
    re.compile(r"\bI (typically|usually|normally|routinely)\b", re.IGNORECASE),
    re.compile(r"\bwe (typically|usually|normally|routinely)\b", re.IGNORECASE),

    # Sequence definition
    re.compile(r"\bfirst .+ then .+ (then|finally|after that)\b", re.IGNORECASE),
    re.compile(r"\bstep (\d|one|two|three).+step (\d|one|two|three)\b", re.IGNORECASE),

    # Domain-specific redirections
    re.compile(r"\bthat's not how .+ works\b", re.IGNORECASE),
    re.compile(r"\bin (my|our) (experience|industry|field|niche)\b", re.IGNORECASE),
    re.compile(r"\bwhat (I|we) (actually )?need (here )?is\b", re.IGNORECASE),
    re.compile(r"\bthe (right|correct|proper|better) (way|approach) (is|would be)\b", re.IGNORECASE),

    # Framework naming
    re.compile(r"\bI call (this|it)\b", re.IGNORECASE),
    re.compile(r"\bI('ve| have) developed\b", re.IGNORECASE),
    re.compile(r"\bmy (strategy|playbook|checklist|template|recipe)\b", re.IGNORECASE),
]

# ── Explicit re-request patterns ────────────────────────────────────────────
EXPLICIT_REQUEST_PATTERNS = [
    re.compile(r"\blead magnet\b", re.IGNORECASE),
    re.compile(r"\bsave (my |this )?(workflow|methodology|process)\b", re.IGNORECASE),
    re.compile(r"\bturn (this |it )?into a (lead magnet|product|template)\b", re.IGNORECASE),
    re.compile(r"\bpackage (this|my) (methodology|workflow|process)\b", re.IGNORECASE),
    re.compile(r"\bcrystallize\b", re.IGNORECASE),
]

# ── Loop breaker ────────────────────────────────────────────────────────────
LOOP_PATTERNS = [
    re.compile(r"methodology-nudge\.py", re.IGNORECASE),
    re.compile(r"methodology nudge", re.IGNORECASE),
]

NUDGE_MESSAGE = (
    "Looks like you have your own methodology here — "
    "want to turn this into a lead magnet?"
)


def _extract_text(content) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for block in content:
            if isinstance(block, dict) and block.get("type") == "text":
                parts.append(block.get("text", ""))
        return " ".join(parts)
    return ""


def _state_path(session_id: str) -> str:
    """Stores the user message count at last nudge time."""
    return os.path.join(
        tempfile.gettempdir(),
        f"silverbee-methodology-nudge-{session_id}.state",
    )


def _read_last_nudge_count(session_id: str) -> int:
    """Read the user message count at which the last nudge fired. -1 = never."""
    try:
        with open(_state_path(session_id), "r") as f:
            return int(f.read().strip())
    except (OSError, ValueError):
        return -1


def _write_nudge_count(session_id: str, count: int):
    try:
        with open(_state_path(session_id), "w") as f:
            f.write(str(count))
    except OSError:
        pass


def _parse_transcript(transcript_path: str):
    """Parse transcript, return (user_messages, tool_call_count)."""
    user_messages = []
    tool_count = 0

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
            content = msg.get("content", "")

            if role == "user":
                text = _extract_text(content)
                if text.strip():
                    user_messages.append(text[:MAX_MESSAGE_LENGTH])

            elif role == "assistant":
                # Count tool_use blocks in assistant messages
                if isinstance(content, list):
                    for block in content:
                        if isinstance(block, dict) and block.get("type") == "tool_use":
                            tool_count += 1

    return user_messages, tool_count


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

    # ── Need transcript ──────────────────────────────────────────────────
    if not transcript_path or not os.path.isfile(transcript_path):
        sys.exit(0)

    # ── Loop breaker ─────────────────────────────────────────────────────
    try:
        with open(transcript_path, encoding="utf-8") as f:
            tail = f.read()[-5000:]
        if sum(1 for p in LOOP_PATTERNS if p.search(tail)) >= 2:
            sys.exit(0)
    except Exception:
        pass

    # ── Parse transcript ─────────────────────────────────────────────────
    try:
        user_messages, tool_count = _parse_transcript(transcript_path)
    except Exception:
        sys.exit(0)

    if not user_messages:
        sys.exit(0)

    current_msg_count = len(user_messages)

    # ── Condition 1: enough tool calls for a "complete output" ───────────
    if tool_count < TOOL_THRESHOLD:
        sys.exit(0)

    # ── Re-offer guard ───────────────────────────────────────────────────
    last_nudge_at = _read_last_nudge_count(session_id)

    if last_nudge_at >= 0:
        # Already nudged — check if user explicitly asked or enough messages passed
        messages_since = current_msg_count - last_nudge_at
        messages_since_nudge = user_messages[last_nudge_at:]
        combined_recent = " ".join(messages_since_nudge)

        user_explicitly_asked = any(
            p.search(combined_recent) for p in EXPLICIT_REQUEST_PATTERNS
        )

        if not user_explicitly_asked and messages_since < REFIRE_MESSAGE_GAP:
            sys.exit(0)

    # ── Condition 2: at least one behavioral signal ──────────────────────
    combined_user_text = " ".join(user_messages)
    signals_found = [
        p.pattern for p in METHODOLOGY_PATTERNS
        if p.search(combined_user_text)
    ]

    if not signals_found:
        sys.exit(0)

    # ── Record nudge position ────────────────────────────────────────────
    _write_nudge_count(session_id, current_msg_count)

    # ── Output the nudge ─────────────────────────────────────────────────
    print(json.dumps({
        "decision": "notify",
        "reason": NUDGE_MESSAGE,
    }))


if __name__ == "__main__":
    main()
