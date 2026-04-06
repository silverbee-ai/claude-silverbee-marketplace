#!/usr/bin/env python3
"""
Auth URL Resolver — PostToolUse hook for Silverbee MCP tools.

When any Silverbee MCP tool call returns an error response, this hook
makes a direct HTTP request to the Silverbee MCP server to retrieve the
authentication URL. It then injects the URL into the conversation via
additionalContext so the LLM can show it to the user — even when the
original error was a generic "Tool execution failed" with no URL.

On successful tool calls, this hook exits silently with no output.
"""
import json
import os
import re
import sys
import urllib.request
import urllib.error


# MCP server URL — read from .mcp.json or use default
DEFAULT_MCP_URL = "https://silverbee-us.apigene.ai/globalagent/codex-seo-agent/mcp"

# Strings that indicate a tool call failed (case-insensitive check)
ERROR_INDICATORS = [
    "tool execution failed",
    "error",
    "failed",
    "511",
    "authentication required",
    "unauthorized",
    "not authenticated",
    "connection failed",
]


def find_url_in_text(text: str) -> str | None:
    """Extract the first https:// URL from a string."""
    match = re.search(r'https://[^\s"\'<>\])\},]+', text)
    return match.group(0).rstrip(".,;:") if match else None


def looks_like_error(tool_response: str) -> bool:
    """Check if the tool response looks like an error."""
    lower = tool_response.lower()
    return any(indicator in lower for indicator in ERROR_INDICATORS)


def get_mcp_url() -> str:
    """Read the Silverbee MCP server URL from .mcp.json if available."""
    plugin_root = os.environ.get("CLAUDE_PLUGIN_ROOT", "")
    if plugin_root:
        mcp_path = os.path.join(plugin_root, ".mcp.json")
        try:
            with open(mcp_path, "r") as f:
                config = json.load(f)
            return config.get("mcpServers", {}).get("silverbee", {}).get("url", DEFAULT_MCP_URL)
        except (OSError, json.JSONDecodeError):
            pass
    return DEFAULT_MCP_URL


def try_get_auth_url(mcp_url: str) -> str | None:
    """
    Make a lightweight request to the MCP server.
    If the user isn't authenticated, the server returns a 511 (or similar)
    with the auth redirect URL in the response body.
    """
    payload = json.dumps({
        "jsonrpc": "2.0",
        "method": "initialize",
        "params": {"capabilities": {}},
        "id": 1,
    }).encode("utf-8")

    req = urllib.request.Request(
        mcp_url,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            body = resp.read().decode("utf-8", errors="replace")
            return find_url_in_text(body)
    except urllib.error.HTTPError as e:
        body = ""
        try:
            body = e.read().decode("utf-8", errors="replace")
        except Exception:
            pass
        url = find_url_in_text(body)
        if url:
            return url
        location = e.headers.get("Location", "")
        if location.startswith("http"):
            return location
        return None
    except Exception:
        return None


def main():
    raw = sys.stdin.read()
    try:
        hook_input = json.loads(raw)
    except json.JSONDecodeError:
        sys.exit(0)

    tool_name = hook_input.get("tool_name", "")

    # Only handle Silverbee MCP tools (name format varies by environment)
    if "silverbee" not in tool_name.lower():
        sys.exit(0)

    # Get the tool response — could be in tool_response, error, or tool_output
    tool_response = hook_input.get("tool_response", "")
    error_msg = hook_input.get("error", "")

    # Stringify the response for inspection
    if isinstance(tool_response, dict):
        response_text = json.dumps(tool_response)
    else:
        response_text = str(tool_response)

    combined_text = f"{response_text} {error_msg}"

    # If this looks like a successful call, exit silently
    if not error_msg and not looks_like_error(combined_text):
        sys.exit(0)

    # --- This is an error. Resolve the auth URL. ---

    # 1. Check if the error/response itself contains a URL
    auth_url = find_url_in_text(combined_text)

    # 2. If no URL found, probe the MCP server directly
    if not auth_url:
        mcp_url = get_mcp_url()
        auth_url = try_get_auth_url(mcp_url)

    # 3. Fallback: use the known redirect base
    if not auth_url:
        auth_url = "https://silverbee-us.apigene.ai/sign-in"

    display_error = error_msg or response_text[:200]

    # Output context for the LLM — block the tool and inject auth message
    output = {
        "decision": "block",
        "reason": (
            f"Silverbee authentication required. "
            f"Show the user this EXACT message:\n\n"
            f"🔐 **Authentication required.** Your Silverbee account isn't connected yet.\n\n"
            f"**👉 Log in here: {auth_url}**\n\n"
            f"⚠️ **Execution is paused.** Once you've logged in, say \"continue\" and I'll resume.\n\n"
            f"Raw error: `{display_error}`\n\n"
            f"DO NOT rephrase this message. DO NOT ask the user questions. "
            f"Just show the message above exactly as written, including the clickable URL."
        ),
    }

    json.dump(output, sys.stdout)
    sys.exit(0)


if __name__ == "__main__":
    main()
