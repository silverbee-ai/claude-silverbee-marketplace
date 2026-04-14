---
name: supervisor
description: >
  Core execution rules for all SEO workflows. Covers startup, tool usage,
  progress communication, error handling, and output format. Load this skill
  at the start of every SEO task.
---

# Supervisor Skill

## Startup

### Step 1 — Load tool catalog (once per session)
Call `get_instructions` **only if you have not already called it in this
conversation**. It returns the live tool catalog and available operations.

If you already have the catalog from an earlier skill or command in this
session, skip this call entirely.

**Override:** When a single `run_action` returns 511/401/403, classify it as
an **app auth error** (not a connection failure) and follow this skill's
app-auth-error handling below — use the fallback chain and continue.

**If `get_instructions` fails (any error):**
→ Jump to **"Tool call errors"** section below. Do not proceed.

### Step 2 — Pre-flight connectivity check (once per session)
Call `list_available_apps` **only if you have not already called it in this
conversation**. This verifies that the user's tool connections are live.

If you already have the apps list from an earlier call in this session,
reuse it — do not call again.

- **If `list_available_apps` fails (any error)** → Jump to **"Tool call errors"** section. Do not proceed.
- **If `list_available_apps` succeeds but returns an empty list** → Tell the user:
  > ⚠️ **No data sources connected.** You have a Silverbee account but no tools (GSC, Ahrefs, etc.) are linked yet.
  > Please visit your Silverbee dashboard to connect your SEO tools, then come back and try again.
- **If `list_available_apps` succeeds with apps listed** → Proceed to the workflow. Auth is confirmed.

Do not attempt `run_action` or any other tool call until Step 2 passes.

**Session caching rule:** Steps 1 and 2 run at most **once per conversation**.
When a second skill loads the supervisor, it inherits the catalog and apps
list already in context. This applies to all skills — none should re-call
`get_instructions` or `list_available_apps` if the supervisor already ran.

### Step 2b — Load project config (if available)
Check if `.silverbee.json` exists in the working directory. If it does, read it
and use its values as defaults for the workflow (domain, competitors, geo, etc.).

Priority order: (1) user's explicit input > (2) `$ARGUMENTS` > (3) `.silverbee.json`.
If the file doesn't exist, proceed normally — no error, no prompt.

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

**`search_actions` caching:** Once you call `search_actions` for a given query,
remember the results. Do not call `search_actions` with the same or
substantially similar query again in the same conversation.

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
- If you switch to a fallback, mention it briefly in the progress line
  (include step number if available): `✓ GSC not connected — using Ahrefs.`
- Only ask the user to connect an app if ALL fallbacks for a data type are
  unavailable and the data is critical to the workflow.
- Call `search_actions(query)` to discover equivalent operations in the
  fallback app when you don't know the exact operation_id.

## Result Reuse

If you already fetched the same data type for the same domain from the same
source app earlier in this conversation, reuse that result. Do not re-fetch.
Say `✓ Reusing [data] from earlier` in the progress line. Re-fetch if:
the user explicitly asks, the query parameters differ, or the earlier call
returned an error (never reuse failed results).

## Progress — the most important rule

After each **major step** (as defined by the active skill's Step Count table),
output one text line before making the next call. No exceptions.

A major step is a logical phase of the workflow (e.g., "fetch GSC keywords"),
not an individual `run_action` call. Multiple parallel tool calls within one
step count as a single step.

### Format

If the active skill has a **Step Count** table, use numbered progress:

```
[1/7] ✓ Scope locked — ynet.co.il, IL market. Pulling keyword candidates...
[2/7] ✓ 84 keyword candidates from Ahrefs. Enriching with volume/KD/CPC...
[3/7] ✓ Metrics collected. Pulling GSC rankings...
```

If the skill has **no Step Count table**, use plain progress without numbers:
`✓ Fetched GSC keywords (847 results). Running enrichment...`

If a step is skipped (reused data, non-critical failure), still count it:
`[4/7] ✓ Reusing GSC rankings from earlier. Running cannibalization check...`

If a tool call returns an error or empty result, say so immediately in the
progress line.

## Tool call errors

When a tool call fails, classify it and follow the matching rule. There is
one error-handling system — no exceptions.

### Step 1 — Classify the error

**CRITICAL RULE — never pause for a single app auth error.** If `run_action`
fails for one app (GSC, Ahrefs, etc.) with an auth/401/403/511 error, that
is an **app auth error**, not a connection error — even if the error contains
a login URL. Silently switch to the fallback chain and keep going. Only STOP
if `get_instructions` or `list_available_apps` itself fails (meaning the
MCP server is unreachable).

| Signal | Classification | Action |
|--------|---------------|--------|
| `get_instructions` or `list_available_apps` fails | **Connection error** | STOP → show login URL |
| Multiple unrelated apps fail in sequence | **Connection error** | STOP → show login URL |
| `auth` / `401` / `403` / `511` on a single `run_action` | **App auth error** | Fallback chain → continue (NEVER stop) |
| `rate_limit` / `429` / `quota` | **Transient error** | Retry once after 3s |
| `egress` / `blocked` / `network egress` | **Non-retriable block** | Skip step — do NOT retry or fallback |
| `timeout` / `ETIMEDOUT` | **Transient error** | Retry once |
| `not_found` / `404` | **Skip error** | Skip step, note in output |
| `5xx` (single app, others working) | **Transient error** | Retry once |
| 200 OK but empty result / no data | **Skip error** | Skip step, note in output |
| Anything else | **Unknown error** | STOP → show raw error |

### App auth errors — NEVER stop, NEVER pause, ALWAYS fallback

**This is the most common error type.** A single app returning auth/401/403/511
means that app isn't connected. The MCP server works fine. **Do NOT stop.
Do NOT show a login URL. Do NOT ask the user to authenticate. Do NOT pause.**

1. Silently switch to the fallback chain from Step 3:
   `✓ GSC not connected — using Ahrefs for ranking data.`
2. If all fallbacks for that data type also fail, skip the step and note it:
   `⚠️ Ranking data unavailable — GSC and Ahrefs both need connecting.`
3. **Keep the workflow running.** Deliver results from whatever IS available.
4. Track all apps that returned auth errors during the workflow.
5. Only at the **very end** of the output, in a Recommended Next Steps section:

> 🔐 **Connect more tools** — Some data sources ([list apps]) weren't
> available in this analysis. Log in at https://silverbee-us.apigene.ai/sign-in
> to connect them and unlock the full audit.

**Exception — total blackout:** If ALL apps across ALL fallback chains for
ALL data types return auth errors (meaning zero data is available), then
stop and show login links. But this should almost never happen — most users
have at least one source connected.

### Connection errors — STOP immediately

These mean the MCP server itself is unreachable or the user has no Silverbee
account. Nothing can proceed. **Only `get_instructions` or
`list_available_apps` failures trigger this — never a single `run_action`.**

1. Do not retry. STOP.
2. Scan the error response for a URL (`http://` or `https://`).
3. Show the user:

> 🔐 **Authentication required.**
> **👉 Log in here: [URL from error, or https://silverbee-us.apigene.ai/sign-in]**
> Raw error: `[exact error message]`
> Say "continue" once you've logged in.

4. Wait for user confirmation before any further tool calls.

This ensures the user gets maximum value from whatever IS connected, and
knows exactly what they're missing.

### Transient errors — fallback, then retry, then skip or stop

**Circuit breaker:** If 3 or more tool calls have already failed in this
workflow (any error type, any app), skip remaining non-critical steps and
deliver partial results. Do not continue burning calls on a degraded session.

1. **Try fallback first.** Check the fallback chain in Step 3. If an
   alternative app is connected, switch to it instead of retrying:
   `✓ GSC query failed — switching to Ahrefs for ranking data.`
2. **If no fallback available**, report `⟳ Retrying [tool] ([reason])...`,
   wait 3 seconds, retry once. **Max 1 retry per tool call.**
3. If fallback or retry succeeds → continue normally.
4. If both fail → check the active skill's **Step Criticality** table:
   - **Critical step** → stop workflow, deliver whatever was collected so far
   - **Non-critical step** → skip it, note the gap, continue
   - **No Step Criticality table** → treat the step as critical (stop)

**Latency note:** The 3s retry delay only fires on failure when no fallback
exists. Mitigation: max 1 retry, so worst case is +3s per failed call.

### Non-retriable blocks — skip immediately, no fallback

These mean an external restriction (network egress policy, firewall, IP block)
prevents access to a resource. Retrying or switching apps will not help —
the block applies to all outbound requests for that URL/domain.

1. Do **not** retry. Do **not** try the fallback chain.
2. Skip the step and note it in output:
   `⚠️ [step] skipped — network egress blocked for [URL/domain].`
3. If the step is critical (per Step Criticality table), deliver partial
   results from whatever was already collected. Do not stop the entire
   workflow — other data sources (GSC, Ahrefs) that don't require
   fetching the blocked URL may still work.

### Skip errors — note and continue

Skip the step. In the final output, mark the gap:
- Markdown: "⚠️ [data type] unavailable — [source] returned 404"
- Dashboard: "Data unavailable" placeholder
- HTML: warning banner listing missing data

## Output rules

- For any substantial deliverable, load `seo-output-formatter` and follow the
  three-layer output: call `show_generative_ui` with a dashboard spec (Layer 1),
  write the HTML report (Layer 2), then output the full markdown (Layer 3)
- Load `react-wow-output` for the full `show_generative_ui` component API reference
- Load `charts-output` before producing any chart-eligible data table
- Begin any substantial deliverable with an Executive Summary (3–5 bullets)
- Never expose internal tool names, MCP server details, or skill names to
  the user — speak in first person: "I'll analyze...", "Here's what I found..."

