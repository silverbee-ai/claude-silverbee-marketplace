#!/usr/bin/env python3
"""
User Identity Resolution — shared utility for Silverbee hooks.

Resolves user_id using a waterfall:
  1. Claude subscription email (~/.claude/settings.json → "primaryEmail")
  2. Git user email (git config user.email)
  3. Machine fingerprint (SHA-256 of hostname:username)

Import from hook scripts via:
    sys.path.insert(0, os.path.dirname(__file__))
    from _user_id import resolve_user_id
"""
import hashlib
import json
import os
import platform
import subprocess


def _claude_email() -> str:
    """Try to read email from Claude's settings."""
    candidates = [
        os.path.expanduser("~/.claude/settings.json"),
        os.path.expanduser("~/.claude.json"),
    ]
    for path in candidates:
        try:
            with open(path, encoding="utf-8") as f:
                data = json.load(f)
            email = data.get("primaryEmail") or data.get("email", "")
            if email and "@" in email:
                return email
        except (OSError, json.JSONDecodeError, TypeError):
            continue
    return ""


def _git_email() -> str:
    """Try to read email from git config."""
    try:
        result = subprocess.run(
            ["git", "config", "user.email"],
            capture_output=True,
            text=True,
            timeout=3,
        )
        email = result.stdout.strip()
        if email and "@" in email:
            return email
    except (OSError, subprocess.TimeoutExpired):
        pass
    return ""


def _machine_fingerprint() -> str:
    """SHA-256 hash of hostname:username as fallback identifier."""
    hostname = platform.node() or "unknown-host"
    username = os.environ.get("USER") or os.environ.get("USERNAME") or "unknown-user"
    raw = f"{hostname}:{username}"
    return hashlib.sha256(raw.encode()).hexdigest()[:16]


def resolve_user_id() -> str:
    """Resolve user identity using the waterfall strategy."""
    return _claude_email() or _git_email() or _machine_fingerprint()
