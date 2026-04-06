#!/usr/bin/env python3
"""
Session Init — SessionStart hook

Runs once when a Silverbee session begins. Performs:
1. Project context detection (is there a .silverbee.json?)
2. Brief status summary shown to Claude
"""
import json
import os
import sys


def main():
    raw = sys.stdin.read()
    try:
        hook_input = json.loads(raw)
    except json.JSONDecodeError:
        sys.exit(0)

    messages = []

    # Check for project config
    cwd = hook_input.get("cwd", os.getcwd())
    config_path = os.path.join(cwd, ".silverbee.json")
    if os.path.isfile(config_path):
        try:
            with open(config_path) as f:
                config = json.load(f)
            domain = config.get("domain", "")
            if domain:
                messages.append(f"Project config loaded: {domain}")
        except Exception:
            messages.append("Warning: .silverbee.json exists but failed to parse")

    if not messages:
        sys.exit(0)

    print(json.dumps({
        "decision": "notify",
        "reason": "Silverbee session context:\n" + "\n".join(f"- {m}" for m in messages),
    }))


if __name__ == "__main__":
    main()
