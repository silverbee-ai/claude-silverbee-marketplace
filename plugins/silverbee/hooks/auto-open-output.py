#!/usr/bin/env python3
"""
Auto-Open Output — PostToolUse hook for Write tool.

Automatically opens HTML/MD output files after they're written so the
user sees the result immediately. Skips skill files, hooks, configs,
and other internal plugin files.
"""
import json
import os
import platform
import subprocess
import sys

# Directories that contain internal plugin files — never auto-open these
SKIP_DIRS = {
    "skills",
    "hooks",
    "commands",
    "agents",
    ".claude-plugin",
    "server",
    "tests",
    "output-styles",
    "node_modules",
    ".git",
}

# File names that are internal — never auto-open
SKIP_NAMES = {
    "SKILL.md",
    "AGENT.md",
    "hooks.json",
    "plugin.json",
    "package.json",
    ".mcp.json",
    "CLAUDE.md",
    "MEMORY.md",
    "README.md",
}

# Extensions to auto-open
OPEN_EXTENSIONS = {".html", ".md", ".csv"}


def is_internal_file(file_path: str) -> bool:
    """Check if the file is an internal plugin file that shouldn't be opened."""
    basename = os.path.basename(file_path)
    if basename in SKIP_NAMES:
        return True

    parts = file_path.replace("\\", "/").split("/")
    return any(part in SKIP_DIRS for part in parts)


def open_file(file_path: str) -> None:
    """Open a file with the system default application."""
    system = platform.system()
    try:
        if system == "Darwin":
            subprocess.Popen(["open", file_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        elif system == "Windows":
            os.startfile(file_path)
        else:
            subprocess.Popen(["xdg-open", file_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception:
        pass


def main():
    raw = sys.stdin.read()
    try:
        hook_input = json.loads(raw)
    except json.JSONDecodeError:
        sys.exit(0)

    tool_name = hook_input.get("tool_name", "")
    if tool_name != "Write":
        sys.exit(0)

    tool_input = hook_input.get("tool_input", {})
    if not isinstance(tool_input, dict):
        sys.exit(0)

    file_path = tool_input.get("file_path", "")
    if not file_path:
        sys.exit(0)

    _, ext = os.path.splitext(file_path.lower())
    if ext not in OPEN_EXTENSIONS:
        sys.exit(0)

    if is_internal_file(file_path):
        sys.exit(0)

    if not os.path.isfile(file_path):
        sys.exit(0)

    open_file(file_path)


if __name__ == "__main__":
    main()
