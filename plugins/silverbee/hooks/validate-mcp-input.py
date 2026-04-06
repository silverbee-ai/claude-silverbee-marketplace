#!/usr/bin/env python3
"""
Validate MCP Input — PreToolUse hook

Fires before Silverbee MCP tool calls. Validates:
1. Domain format is valid (not empty, not a URL path)
2. Warns on suspicious inputs (e.g., localhost, IP addresses)
"""
import json
import re
import sys


def main():
    raw = sys.stdin.read()
    try:
        hook_input = json.loads(raw)
    except json.JSONDecodeError:
        sys.exit(0)

    tool_name = hook_input.get("tool_name", "")

    if "silverbee" not in tool_name.lower():
        sys.exit(0)

    tool_input = hook_input.get("tool_input", {})
    if not isinstance(tool_input, dict):
        sys.exit(0)

    params = tool_input.get("params", {})
    if not isinstance(params, dict):
        sys.exit(0)

    domain = params.get("domain", "") or params.get("target", "")
    if not domain:
        sys.exit(0)

    if domain.startswith("http"):
        print(json.dumps({
            "decision": "notify",
            "reason": (
                f"Warning: '{domain}' looks like a URL, not a domain. "
                f"The tool expects a bare domain (e.g., 'example.com')."
            ),
        }))
        return

    LOCAL_NAMES = {"localhost", "127.0.0.1", "0.0.0.0", "::1", "[::1]"}
    is_ip = re.match(r"^\d+\.\d+\.\d+\.\d+$", domain) or domain.startswith("[")
    if domain in LOCAL_NAMES or is_ip:
        print(json.dumps({
            "decision": "notify",
            "reason": (
                f"Warning: '{domain}' is a local/IP address. "
                f"SEO tools need a public domain."
            ),
        }))
        return

    sys.exit(0)


if __name__ == "__main__":
    main()
