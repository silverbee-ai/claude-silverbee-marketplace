#!/bin/bash
# Ensure Silverbee MCP connectors are registered.
# Runs on SessionStart — idempotent, silent, fast.

CLAUDE_JSON="$HOME/.claude.json"

# Check if silverbee-tools exists in user MCP config
if ! command -v claude &>/dev/null; then
  exit 0
fi

needs_tools=false
needs_ui=false

if [ -f "$CLAUDE_JSON" ]; then
  if ! python3 -c "import json; d=json.load(open('$CLAUDE_JSON')); assert 'silverbee-tools' in d.get('mcpServers',{})" 2>/dev/null; then
    needs_tools=true
  fi
  if ! python3 -c "import json; d=json.load(open('$CLAUDE_JSON')); assert 'silverbee-ui' in d.get('mcpServers',{})" 2>/dev/null; then
    needs_ui=true
  fi
else
  needs_tools=true
  needs_ui=true
fi

if [ "$needs_tools" = true ]; then
  claude mcp add --transport http -s user silverbee-tools https://silverbee-us.apigene.ai/globalagent/codex-seo-agent/mcp >/dev/null 2>&1
fi

if [ "$needs_ui" = true ]; then
  claude mcp add --transport http -s user silverbee-ui https://generative-ui-mcp-production.up.railway.app/mcp >/dev/null 2>&1
fi
