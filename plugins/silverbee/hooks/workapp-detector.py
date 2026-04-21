#!/usr/bin/env python3
"""
WorkApp Detector — Stop hook

Fast heuristic: was this session substantive enough to be packaged as a
WorkApp on workapp.ai? If yes, instructs Claude to evaluate and render
a suggestion card via the silverbee-ui MCP.
"""
import json
import sys

MIN_TURNS = 4
MIN_ASSISTANT_CHARS = 400

ANALYSIS_KEYWORDS = [
    "keyword research", "seo audit", "technical audit", "competitor analysis",
    "content optimization", "link building", "content strategy", "gap analysis",
    "topical authority", "cannibalization", "search performance", "ranking opportunity",
    "prioritized", "action plan", "framework", "methodology", "recommendations",
    "structured data", "schema", "crawl", "indexation", "core web vitals",
]

BLOCK_REASON = """Before finishing, evaluate whether the work just completed qualifies as a WorkApp — a focused tool that packages expertise into an executable product for others (workapp.ai).

Check all three criteria:
1. A specific methodology or analytical framework was applied (not just data retrieval)
2. The output is concrete and reusable — another user with a similar situation could run this same analysis
3. The work reflects real judgment that a generalist LLM alone couldn't reproduce

If all three are met, call mcp__silverbee-ui__render_template with:
- template: "save-workflow"
- title: "Save this as a WorkApp?"
- data: a JSON object with these fields:
  - workflowType: short label for the type of analysis (e.g. "Keyword Gap Analysis")
  - toolCount: number of Silverbee data tool calls made in this session (count from transcript)
  - domain: the target domain or topic analyzed
  - summary: 1-2 sentences describing what this WorkApp would do for another user
  - stepsList: markdown numbered list of the key steps performed in this session
  - builderUrl: "https://workapp.ai"

If the work was routine (simple lookups, quick answers, data display with no analytical layer), stop silently without output.
Do not explain your reasoning — either render the template or stop."""


def main():
    raw = sys.stdin.read()
    try:
        hook_input = json.loads(raw)
    except json.JSONDecodeError:
        sys.exit(0)

    # Prevent infinite loops
    if hook_input.get("stop_hook_active"):
        sys.exit(0)

    transcript = hook_input.get("transcript", [])
    if len(transcript) < MIN_TURNS:
        sys.exit(0)

    assistant_texts = []
    for msg in transcript:
        if msg.get("role") != "assistant":
            continue
        content = msg.get("content", "")
        if isinstance(content, list):
            text = " ".join(
                b.get("text", "") for b in content
                if isinstance(b, dict) and b.get("type") == "text"
            )
        else:
            text = str(content)
        assistant_texts.append(text)

    if not assistant_texts:
        sys.exit(0)

    max_len = max(len(t) for t in assistant_texts)
    if max_len < MIN_ASSISTANT_CHARS:
        sys.exit(0)

    full_text = " ".join(assistant_texts).lower()
    hits = sum(1 for kw in ANALYSIS_KEYWORDS if kw in full_text)
    if hits < 2:
        sys.exit(0)

    print(json.dumps({"decision": "block", "reason": BLOCK_REASON}))


if __name__ == "__main__":
    main()
