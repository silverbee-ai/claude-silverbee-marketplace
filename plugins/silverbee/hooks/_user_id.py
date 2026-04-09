#!/usr/bin/env python3
"""
User Identity Resolution — shared utility for Silverbee hooks.

Resolves user_id using a compliant waterfall:
  1. Environment variables officially exposed to plugins
  2. Anonymous machine fingerprint (SHA-256 of hostname:username)

Does NOT read Claude's private settings files (~/.claude/settings.json,
~/.claude.json) or git config — this would violate Directory Policy §1F
and §1C.

Import from hook scripts via:
    sys.path.insert(0, os.path.dirname(__file__))
    from _user_id import resolve_user_id
"""
import hashlib
import os
import platform


def _env_email() -> str:
    """Check environment variables that Claude/Cowork may officially expose."""
    for env_key in ("CLAUDE_USER_EMAIL", "CLAUDE_ACCOUNT_EMAIL"):
        email = os.environ.get(env_key, "")
        if email and "@" in email:
            return email
    return ""


def _machine_fingerprint() -> str:
    """SHA-256 hash of hostname:username as anonymous fallback identifier."""
    hostname = platform.node() or "unknown-host"
    username = os.environ.get("USER") or os.environ.get("USERNAME") or "unknown-user"
    raw = f"{hostname}:{username}"
    return hashlib.sha256(raw.encode()).hexdigest()[:16]


def resolve_user_id() -> str:
    """Resolve user identity using the compliant waterfall strategy."""
    return _env_email() or _machine_fingerprint()
