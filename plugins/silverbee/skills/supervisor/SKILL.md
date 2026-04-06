---
name: supervisor
description: >
  Core execution rules for all SEO workflows. Covers startup, tool usage,
  progress communication, error handling, and output format. Load this skill
  at the start of every SEO task.
---

# Supervisor Skill

## Startup

### Step 1 — Load tool catalog
Call `get_instructions` before anything else. It returns the live tool catalog
and operational guidelines for this session.

**If `get_instructions` fails (any error):**
→ Jump to **"Tool call errors"** section below. Do not proceed.

### Step 2 — Pre-flight connectivity check (MANDATORY)
Immediately after `get_instructions` succeeds, call `list_available_apps`.
This verifies that the user's tool connections are live **before** any
workflow begins.

- **If `list_available_apps` fails (any error)** → Jump to **"Tool call errors"** section. Do not proceed.
- **If `list_available_apps` succeeds but returns an empty list** → Tell the user:
  > ⚠️ **No data sources connected.** You have a Silverbee account but no tools (GSC, Ahrefs, etc.) are linked yet.
  > Please visit your Silverbee dashboard to connect your SEO tools, then come back and try again.
- **If `list_available_apps` succeeds with apps listed** → Proceed to the workflow. Auth is confirmed.

Do not attempt `run_action` or any other tool call until Step 2 passes.

## How to use tools

All live data comes through four MCP tools:
- `list_available_apps` — see which SEO data sources are connected
- `list_actions(app_name)` — see what operations an app supports
- `search_actions(query)` — find the right operation by keyword
- `run_action(app_name, operation_id, input)` — execute an operation

Run independent `run_action` calls in parallel when steps are independent
(e.g. fetch GSC + Ahrefs simultaneously). Always prefer GSC over Ahrefs
for ranking/traffic data when both are available.

### Step 3 — Know your available apps (MANDATORY)

After Step 2, **remember the list of connected apps** from `list_available_apps`.
Before every `run_action` call, check whether the app you're about to call is
in that list. If not, use `search_actions` to find an alternative app that
offers equivalent data.

**Standard fallback chains** (use these when the preferred app is not connected):

| Data type | Preferred | Fallback 1 | Fallback 2 |
|---|---|---|---|
| Rankings / traffic / clicks | GSC | Ahrefs | DataForSEO |
| Keyword volume / KD / CPC | Ahrefs | DataForSEO | — |
| Backlink data | Ahrefs | DataForSEO | — |
| SERP overview / features | Ahrefs | DataForSEO | — |
| Site audit / crawl | DataForSEO | Ahrefs | — |
| Search suggestions | Ahrefs | DataForSEO | Google Trends |
| AI visibility | DataForSEO AI Visibility | — | — |

**Rules:**
- If the preferred app is not in the connected apps list, silently switch to
  the next fallback. Do NOT ask the user to connect it — just use what's available.
- If you switch to a fallback, mention it briefly in the progress line:
  `✓ GSC not connected — using Ahrefs for ranking data.`
- Only ask the user to connect an app if ALL fallbacks for a data type are
  unavailable and the data is critical to the workflow.
- Call `search_actions(query)` to discover equivalent operations in the
  fallback app when you don't know the exact operation_id.

## Progress — the most important rule

**After every single `run_action` call**, output one line of plain text before
making the next call. No exceptions. Format:

```
✓ [what just finished] — [key number or result]. [what comes next]...
```

Examples:
```
✓ Scope locked — ynet.co.il targets Hebrew news, primary market IL. Pulling keyword candidates from Ahrefs...
✓ Got 84 keyword candidates from Ahrefs. Enriching with volume/KD/CPC...
✓ Metrics collected for 84 keywords. Pulling GSC rankings...
✓ Rankings pulled — 31 keywords already ranking. Running cannibalization check...
✓ Cannibalization: 2 flags found. Building dashboard...
```

If a `run_action` call returns an error or empty result, say so immediately —
never retry silently.

## Tool call errors

There are two types of errors. Handle them differently:

### Type 1 — App-specific error (one app fails, others may work)

When a `run_action` call for a **specific app** fails (e.g. GSC returns an
error, or an Ahrefs operation fails), but the Silverbee connection itself
is working (other tools succeeded earlier in this session):

1. **Check the fallback chain** in "Step 3 — Know your available apps" above.
2. If an alternative app is connected, use `search_actions` to find the
   equivalent operation and try the fallback. Mention it in the progress line:
   `✓ GSC query failed — switching to Ahrefs for ranking data.`
3. Only stop and ask the user if ALL fallbacks for that data type are exhausted.

### Type 2 — Connection/auth error (Silverbee itself is unreachable)

When `get_instructions`, `list_available_apps`, or the **first** tool call in
a session fails — this means the Silverbee connection isn't established.
Also applies when multiple unrelated apps all fail in sequence.

**When a connection/auth error occurs:**

1. **STOP IMMEDIATELY** — do not attempt any more tool calls. Do not retry.
   Do not try a different tool hoping it will work. STOP.

2. **Scan the full error response for a URL.** Check every field and string
   in the error for anything starting with `http://` or `https://`. Look in:
   - `details` field
   - `url`, `login_url`, `auth_url` fields
   - Inside message strings
   - Anywhere in the raw error text

3. **Show the user what happened.** Pick the matching case:

**Case A — You found a URL in the error:**

> 🔐 **Authentication required.** Your Silverbee account isn't connected yet.
>
> **👉 Log in here: PASTE_THE_ACTUAL_URL_HERE**
>
> ⚠️ **Execution is paused.** Once you've logged in, say "continue" and I'll resume.

**Case B — No URL found in the error (e.g. "Tool execution failed"):**

> 🔐 **Silverbee connection failed.** This usually means your account isn't
> connected to this environment yet.
>
> **👉 Connect here: https://silverbee-us.apigene.ai/sign-in**
>
> Raw error for reference: `[paste the exact error message here]`
>
> ⚠️ **Execution is paused.** Once you've connected, say "continue" and I'll resume.

4. **Wait for explicit user confirmation** before retrying any tool call.

### Rules — no exceptions

- **ALWAYS show a clickable URL** — either from the error (Case A) or the
  fallback `https://silverbee-us.apigene.ai/sign-in` (Case B). There is no scenario
  where you respond without a URL.
- **ALWAYS paste the raw error message** so the user can see exactly what failed.
- **NEVER** ask the user "do you have an account?" or "are your tools connected?"
  instead of showing the URL. The URL IS the answer.
- **NEVER** suggest vague troubleshooting steps. Show the URL and stop.
- **NEVER** continue making tool calls after any error.
- **NEVER** retry a failed call silently or try different tools.

### Notes
- The pre-flight check in Startup Step 2 catches most issues before any workflow begins.
- If an error occurs *during* a workflow, the same rules apply: stop, show URL, wait.
- This works identically across: Claude Code, Claude CoWork, web, and IDE integrations.

## Output rules

- For any substantial deliverable, load `seo-output-formatter` and follow the
  three-layer output: call `show_generative_ui` with a dashboard spec (Layer 1),
  write the HTML report (Layer 2), then output the full markdown (Layer 3)
- Load `react-wow-output` for the full `show_generative_ui` component API reference
- Load `charts-output` before producing any chart-eligible data table
- Begin any substantial deliverable with an Executive Summary (3–5 bullets)
- Never expose internal tool names, MCP server details, or skill names to
  the user — speak in first person: "I'll analyze...", "Here's what I found..."

