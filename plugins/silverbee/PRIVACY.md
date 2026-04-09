# Silverbee Plugin — Data Collection Summary

This document summarizes what data the Silverbee Claude plugin collects, how it is used, and how to opt out.

For the full privacy policy and terms of service, see:
- **Privacy Policy:** https://silverbee.ai/privacy-policy
- **Terms of Service:** https://silverbee.ai/terms

## What Data Is Collected

### Telemetry (tool usage analytics)

When enabled, the plugin collects usage data for **Silverbee tools only** — Claude's built-in tools and other plugins are not tracked. Each telemetry event includes:

- **Tool name** — which Silverbee MCP tool was called (e.g., `run_action`, `list_available_apps`)
- **Skill name** — which Silverbee skill was active (e.g., `silverbee:keyword-research`)
- **Status** — whether the tool call succeeded or errored
- **Duration** — how long the tool call took (milliseconds)
- **Session ID** — an ephemeral identifier for the current session
- **User ID** — derived from environment variables if available, otherwise an anonymous machine fingerprint (SHA-256 hash of hostname and username)
- **Timestamp**

For Silverbee MCP tools specifically, the app name and operation ID are also captured to understand which integrations are used.

### Skill edit feedback

If you modify a Silverbee skill file (SKILL.md) during a session, the plugin collects:

- Which skill was edited
- The edit diffs (old text vs. new text, truncated to 2000 characters)
- Session and user identifiers (same as telemetry)

**No conversation transcript, chat history, or user messages are collected.**

## What Data Is NOT Collected

- Conversation content or chat history
- File paths, URLs, or search queries from non-Silverbee tools
- Claude's private settings or configuration files
- Git configuration or email addresses from git config
- Bash commands or terminal output
- Content of files you read or write

## How Data Is Used

Collected data is used to:

- Understand which Silverbee tools and skills are most used
- Identify errors and improve reliability
- Improve skill quality based on edit patterns

Data is not sold to third parties or used for advertising.

## Third-Party Services

Telemetry and feedback data is sent to:

- `https://web-production-991bd.up.railway.app` — Silverbee's analytics backend (hosted on Railway)

The plugin connects to these MCP servers for its core functionality:

- `https://silverbee-us.apigene.ai` — Silverbee tools MCP server
- `https://generative-ui-mcp-production.up.railway.app` — Silverbee UI rendering

## How to Opt Out

Set the following environment variable to disable all telemetry and feedback collection:

```bash
export SILVERBEE_FEEDBACK_ENABLED=false
```

When disabled, no data is collected or sent. The plugin's core functionality continues to work normally.

## Contact

For privacy concerns or data deletion requests:

- **Email:** info@silverbee.ai
- **Website:** https://silverbee.ai
- **Privacy Policy:** https://silverbee.ai/privacy-policy
- **Terms of Service:** https://silverbee.ai/terms
