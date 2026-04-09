#!/usr/bin/env python3
"""
Returning User Welcome — SessionStart hook for Silverbee.

On session start, checks if the user has saved workflows
(via .silverbee.json in the project directory) and displays
a welcome message with available workflows.

Opt-out: SILVERBEE_FEEDBACK_ENABLED=false
"""
import json
import os
import sys


def main():
    if os.environ.get("SILVERBEE_FEEDBACK_ENABLED", "true").lower() == "false":
        sys.exit(0)

    raw = sys.stdin.read()
    try:
        hook_input = json.loads(raw)
    except json.JSONDecodeError:
        sys.exit(0)

    # Check for .silverbee.json in the project directory
    cwd = hook_input.get("cwd", os.getcwd())
    config_path = os.path.join(cwd, ".silverbee.json")

    if not os.path.isfile(config_path):
        sys.exit(0)

    try:
        with open(config_path, encoding="utf-8") as f:
            config = json.load(f)
    except (OSError, json.JSONDecodeError):
        sys.exit(0)

    workflows = config.get("workflows", [])
    if not workflows:
        sys.exit(0)

    count = len(workflows)
    noun = "workflow" if count == 1 else "workflows"

    print(json.dumps({
        "decision": "notify",
        "reason": (
            f"Welcome back! You have {count} saved {noun} available. "
            f"Run `/silverbee:run-workflow` to see them."
        ),
    }))


if __name__ == "__main__":
    main()
