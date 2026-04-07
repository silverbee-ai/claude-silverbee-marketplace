#!/usr/bin/env python3
"""
Auth URL Resolver — PostToolUse hook for Silverbee MCP tools.

When any Silverbee MCP tool call returns an auth error (511, 401, etc.),
this hook resolves the login URL and notifies the agent. The notification
is non-blocking — the agent continues with available tools and surfaces
the login link as a recommended next step.

On successful tool calls, this hook exits silently with no output.
"""
import json
import os
import re
import sys
import urllib.request
import urllib.error


# MCP server URL — read from .mcp.json, env var, or built-in default
DEFAULT_MCP_URL = os.environ.get(
    "SILVERBEE_MCP_URL",
    "https://silverbee-us.apigene.ai/globalagent/codex-seo-agent/mcp",
)

# Indicators split into two groups so the hook can distinguish connection
# failures (should block) from app-level auth errors (should notify).
CONNECTION_INDICATORS = [
    "connection failed",
    "tool execution failed",
]

AUTH_INDICATORS = [
    "authentication required",
    "unauthorized",
    "not authenticated",
    "status 511",
    "511 network authentication",
    "auth",  # intentionally broad to catch varied auth-related error messages
    "login required",
]


def find_url_in_text(text: str) -> str | None:
    """Extract the first https:// URL from a string."""
    match = re.search(r'https://[^\s"\'<>\])\},]+', text)
    return match.group(0).rstrip(".,;:") if match else None


def classify_error(tool_response: str) -> str | None:
    """Classify a tool response as 'connection', 'auth', or None (no error)."""
    lower = tool_response.lower()
    for indicator in CONNECTION_INDICATORS:
        if indicator in lower:
            return "connection"
    for indicator in AUTH_INDICATORS:
        if indicator in lower:
            return "auth"
    return None


def looks_like_error(tool_response: str) -> bool:
    """Check if the tool response looks like an error."""
    return classify_error(tool_response) is not None


def get_mcp_url() -> str:
    """Read the Silverbee MCP server URL from .mcp.json if available."""
    plugin_root = os.environ.get("CLAUDE_PLUGIN_ROOT", "")
    if plugin_root:
        mcp_path = os.path.join(plugin_root, ".mcp.json")
        try:
            with open(mcp_path, "r") as f:
                config = json.load(f)
            return config.get("mcpServers", {}).get("silverbee-tools", {}).get("url", DEFAULT_MCP_URL)
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

    # Exit silently if no explicit error and no specific auth error indicator
    if not error_msg and not looks_like_error(response_text):
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
        auth_url = os.environ.get(
            "SILVERBEE_SIGN_IN_URL",
            "https://silverbee-us.apigene.ai/sign-in",
        )

    display_error = error_msg or response_text[:200]

    # Classify the error to decide between blocking and non-blocking.
    error_class = classify_error(combined_text)

    if error_class == "connection":
        # Connection-level failure — the MCP server is unreachable or the
        # tool runner itself broke.  Block so the agent stops and shows a
        # login / retry message.
        output = {
            "decision": "block",
            "reason": (
                f"Connection error — the tool call could not reach the server. "
                f"STOP the workflow and ask the user to verify connectivity or "
                f"log in at {auth_url} before retrying.\n\n"
                f"Raw error: `{display_error}`"
            ),
        }
    else:
        # App-level auth error (or unclassified error treated as auth) —
        # non-blocking so the agent continues with fallback data sources.
        output = {
            "decision": "notify",
            "reason": (
                f"App authentication needed for this tool call. "
                f"This is NOT a connection error — the MCP server is reachable, "
                f"but the specific app (e.g. GSC, Ahrefs) requires the user to log in.\n\n"
                f"**Do NOT stop execution.** Continue the workflow using fallback "
                f"data sources per the supervisor skill's fallback chains. "
                f"At the end of the workflow, include this in Recommended Next Steps:\n\n"
                f"**Connect more tools** — Some data sources weren't available. "
                f"Log in at {auth_url} to unlock the full analysis.\n\n"
                f"Raw error: `{display_error}`"
            ),
        }

    json.dump(output, sys.stdout)
    sys.exit(0)


if __name__ == "__main__":
    main()
