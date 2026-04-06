---
name: seo-output-formatter
description: >
  Formatting and presentation standard for all SEO skill outputs in the plugin.
  Call read_skill("seo-output-formatter") at the end of every SEO skill after
  data collection is complete. Controls three-layer output (show_generative_ui
  dashboard + HTML report artifact + full markdown tables), component catalog,
  chart selection, data integrity, emoji policy, next steps, and follow-up
  recommendation format. Mirrors the output agent standard from Silverbee.
---

# SEO Output Formatter

Apply these standards to every SEO deliverable. This skill controls how you
present findings — not what you find. Call it after all data collection is done.

---

## Pre-Output Checklist

Run this before writing a single line of output:

```
□ All data collected — no pending tool calls
□ Identified deliverable type (keyword research / audit / gap analysis / etc.)
□ Confirmed which data is comparable-numeric vs. incomparable/mixed
□ Ready to produce the full dataset — no truncation
□ Have domain slug, workflow slug, and today's date for HTML filename
```

---

## 1. Three-Layer Output Strategy

Every SEO deliverable uses all three layers, always in this order:

| Layer | What | Purpose |
|-------|------|---------|
| **1 — Interactive Dashboard** | `show_generative_ui` call | Compact visual summary; KPIs at a glance |
| **2 — HTML Report File** | Write tool → `.html` file | Persistent, shareable, full-data report |
| **3 — Full Markdown Deliverable** | Tables + sections in chat | Authoritative dataset; no row cap; complete analysis |

**Layer 3 is the source of truth.** Layers 1 and 2 are views over it. Never truncate Layer 3 to fit Layer 1 constraints.

---

## 2. Document Structure (Layer 3)

Every substantial markdown output follows this skeleton, in this exact order:

1. **Title** — `# **[Deliverable Type]: [Target]**` (H1, bold)
2. **Executive Summary** — immediately after title, no blank section between
3. **Numbered sections** — 1️⃣ through 9️⃣ for sections 1–9; plain `10.`, `11.` etc. for 10+
4. **Next Steps table** — always required for analyses and audits
5. **Next recommendation** — single plain-text statement in chat after the deliverable

Nothing may appear between the title and the Executive Summary header.

---

## 3. Executive Summary

**Header:** `## Executive Summary` (H2, no keycap)

**Format rules by data size:**
- **≤ 3 key metrics** → 2–4 short sentences (≤ 25 words each), readable in ≤ 15 sec
- **4+ comparable metrics** (same unit/scale) → use `show_generative_ui` Chart (see §5)
- **4+ incomparable metrics** (mixed units) → markdown table

Always cover: top finding, best/worst performer, one anomaly or trend, recommended next action.

---

## 4. Full Markdown Tables (Layer 3 — Primary Deliverable)

**Tables are the default** for structured data. Use bullets or paragraphs only when a table would be worse.

Quick rule: if items have 2+ attributes → table.

### Mandatory rules

- **No row cap.** Every data row collected must appear. Never truncate.
- One-line explanation before each table stating what it shows and how to read it.
- Numeric cells contain numbers only — units go in the column header, never in cells.
- Percentage changes → dedicated columns, not embedded in text.
- Thousands separators always (e.g., `12,400` not `12400`).
- Column headers: concise (≤ 4 words), consistent across similar analyses.
- `Owner` column → responsible role only (SEO / Content Manager / Developer / DevOps / Webmaster / Analytics / CRO / Copywriter / Marketing). Never individual names. If role unclear, leave blank.
- Source attribution: `[Metric] ([Tool], [YYYY-MM-DD])` — only for tools actually used this session.
- Near-duplicate rows (plural, word order, punctuation) → separate rows, never merged.
- Zero-volume or null rows → exclude from final output.

### Incomparable metrics → markdown table (always)

When rows measure different metrics in different units (e.g., Domain Rating + Backlink Count + Organic Traffic), output a markdown table. Never a chart.

---

## 5. Layer 1: Interactive Dashboard via show_generative_ui

Call `show_generative_ui` first, before the markdown deliverable.

### When to include each component

**Always include:**
- Exactly **4 Metric** components for top KPIs
- **1 Chart** (when rows share the same metric/unit — see chart decision rule below)
- **1–2 Table** components (≤ 12 rows combined — this cap applies to the dashboard preview only, not Layer 3)

**Include when data warrants:**
- **Accordion** — for grouped findings (e.g., issues by category, keywords by cluster)
- **Badge** — for status/risk indicators alongside metrics
- **Card + Grid** — when presenting 2–4 side-by-side comparisons

**Output dashboard limits:**
- More than 1 Chart
- More than 2 Tables
- These constraints apply to SEO output dashboards only. Interactive input forms
  and progress trackers are separate UI patterns — see `react-wow-output` for those.

### Chart decision rule

**STOP. Before calling show_generative_ui, answer:**
> "Do ALL rows measure the SAME metric in the SAME unit/scale?"

- YES → include a Chart component **and** output full tables in Layer 3
- NO → omit Chart from dashboard; markdown tables only in Layer 3

### Chart type selection

| Data shape | Chart type |
|-----------|-----------|
| Time series (clicks, rankings over months) | `line` or `area` |
| Category comparison (keywords by volume) | `bar` |
| Part-of-whole (intent distribution) | `pie` or `donut` |
| Two-variable correlation | `scatter` |
| Multi-axis performance | `radar` |
| Conversion/funnel stages | `funnel` |
| Hierarchical breakdown | `treemap` |
| Radial progress/score | `radialbar` |
| Flow between stages | `sankey` |

### Component catalog

For the full component API (all props, spec format, state bindings, actions, repeat,
and conditional visibility), consult the `react-wow-output` skill. Below is a quick
reference of the components relevant to SEO output dashboards.

**Layout:** `Stack`, `Grid` (columns), `Card` (title, description)
**Content:** `Heading`, `Text`, `Markdown`, `CodeBlock`
**Data:** `Metric` (label, value, detail, trend), `Table` (columns, rows, compact, searchable, sortable, filters), `Chart` (variant: line|bar|area|pie|donut|scatter|radar|radialBar|treemap|funnel|sankey|composed)
**Structure:** `Accordion` (collapsible grouped findings), `Separator`
**Status:** `Badge` (label, color — for inline risk/status indicators)

**Spec format:** `{ root, elements, state? }` — see `react-wow-output` for full documentation and examples.

### Color palette

| Color | Hex | Use for |
|-------|-----|---------|
| Blue | `#2563EB` | Volume, traffic, primary metrics |
| Red | `#DC2626` | Difficulty, drops, risks |
| Green | `#16A34A` | Growth, gains, opportunities |
| Amber | `#D97706` | Warnings, deltas, medium priority |
| Slate | `#64748B` | Neutral/informational |

### Per-workflow dashboard specs

After the Stack container and Heading, use the matching spec below:

**keyword-research:**
```json
"metrics": [
  { "label": "Best Target",     "value": "keyword / KD XX" },
  { "label": "Highest Volume",  "value": "XX,XXX / mo" },
  { "label": "Fastest Growing", "value": "keyword name" },
  { "label": "Total Keywords",  "value": "XX" }
],
"chart": { "variant": "bar", "title": "Top 10 Keywords by Volume" },
"tables": [
  { "title": "Top Keywords",    "columns": ["Keyword","Vol","KD","CPC","Rank","Intent"] },
  { "title": "SERP Snapshot",   "columns": ["Keyword","SERP Type","Top Competitor","Cannibal"] }
]
```

**competitor-analysis / seo-gap-analysis:**
```json
"metrics": [
  { "label": "Traffic Gap",     "value": "XX,XXX / mo" },
  { "label": "Keyword Gap",     "value": "XXX kws" },
  { "label": "DR Delta",        "value": "+XX" },
  { "label": "Top Opportunity", "value": "keyword name" }
],
"chart": { "variant": "bar", "title": "Keyword Gap by Topic Cluster" },
"tables": [
  { "title": "Top Gap Keywords",     "columns": ["Keyword","Vol","Their Rank","Your Rank","Intent"] },
  { "title": "Competitor Top Pages", "columns": ["URL","Traffic","Keywords"] }
]
```

**drop-analysis:**
```json
"metrics": [
  { "label": "Traffic Drop",   "value": "-XX%" },
  { "label": "Affected Pages", "value": "XX" },
  { "label": "Likely Cause",   "value": "Algorithm" },
  { "label": "Confidence",     "value": "High" }
],
"chart": { "variant": "line", "title": "Organic Traffic Over Time" },
"tables": [
  { "title": "Most-Affected Pages", "columns": ["URL","Before","After","Drop %"] },
  { "title": "Ranking Drops",       "columns": ["Query","Before","After","Delta"] }
]
```

**technical-seo:**
```json
"metrics": [
  { "label": "Issues Found",   "value": "XX" },
  { "label": "Critical",       "value": "XX" },
  { "label": "Pages Affected", "value": "XX" },
  { "label": "Quick Wins",     "value": "XX" }
],
"chart": { "variant": "bar", "title": "Issues by Category" },
"tables": [
  { "title": "Critical Findings", "columns": ["Issue","URL","Priority","Fix"] },
  { "title": "Priority Roadmap",  "columns": ["Action","Impact","Effort","Owner"] }
]
```

**periodic-seo-report:**
```json
"metrics": [
  { "label": "Clicks Change", "value": "+XX%" },
  { "label": "Avg Position",  "value": "#X.X" },
  { "label": "Impressions",   "value": "+XX%" },
  { "label": "Top Gainer",    "value": "keyword name" }
],
"chart": { "variant": "line", "title": "Clicks + Impressions Trend",
  "series": ["clicks", "impressions"],
  "colors": ["#2563EB", "#94a3b8"]
},
"tables": [
  { "title": "Ranking Changes", "columns": ["Query","Before","After","Delta"] },
  { "title": "Action Outcomes", "columns": ["Action","Page","Effect","Confidence"] }
]
```

**link-building:**
```json
"metrics": [
  { "label": "Target Domains", "value": "XX" },
  { "label": "Opportunities",  "value": "XX" },
  { "label": "Authority Gain", "value": "+XX DR" },
  { "label": "Priority Wins",  "value": "XX" }
],
"chart": { "variant": "bar", "title": "Opportunities by Category" },
"tables": [
  { "title": "Top Link Prospects",     "columns": ["Domain","DR","Traffic","Relevance","Type"] },
  { "title": "Link Building Timeline", "columns": ["Target","Action","Timeline","Priority"] }
]
```

**ai-visibility:**
```json
"metrics": [
  { "label": "LLM Mentions",    "value": "XX" },
  { "label": "AI Engines",      "value": "X / 4" },
  { "label": "llms.txt Status", "value": "Missing" },
  { "label": "Top Cited URL",   "value": "/page" }
],
"chart": { "variant": "bar", "title": "Competitor Mentions per AI Engine" },
"tables": [
  { "title": "Competitor AI Presence", "columns": ["Domain","ChatGPT","AIO","Gemini","Perplexity"] },
  { "title": "AI Overview Presence",   "columns": ["Query","AIO Triggered","Target Cited"] }
]
```

**topical-authority-mapping:**
```json
"metrics": [
  { "label": "Pillars",        "value": "XX" },
  { "label": "Coverage Score", "value": "XX%" },
  { "label": "Missing Topics", "value": "XX" },
  { "label": "Quick Wins",     "value": "XX" }
],
"chart": { "variant": "radialbar", "title": "Coverage Score per Pillar" },
"tables": [
  { "title": "Content Gap",     "columns": ["Subtopic","Demand","Status","Action"] },
  { "title": "Priority Matrix", "columns": ["Page","Type","Action","Demand"] }
]
```

---

## 6. Layer 2: HTML Report Artifact

After `show_generative_ui`, write a self-contained HTML report file using the Write tool.

**File path format:** `[cwd]/[domain-slug]-[workflow-slug]-[YYYY-MM-DD].html`
Example: `bkzlaw-keyword-research-2026-03-31.html`

Use the HTML template from `output-styles/seo-dashboard.md`. Fill only the `REPORT` JavaScript object with real data. Do not modify anything outside the `REPORT` object.

**REPORT object rules:**
- `type` — deliverable type string (e.g., `"Keyword Research"`)
- `title` — domain or target
- `subtitle` — `"Market · Language · Scope · Generated [DATE]"`
- `metrics` — exactly 4 items matching the per-workflow spec in §5
- `chart` — use only when all chart rows share the same metric/unit
- `tables` — up to 2 tables, ≤ 12 rows each (this is the dashboard preview; full data goes in Layer 3)
- `notes` — 3–5 action items from the Next Steps table

**HTML file integrity rules:**
- All values must come from real tool outputs — never fabricate numbers for the HTML
- Escape HTML entities in all user-supplied strings (the template's `esc()` handles this)
- If a chart has no comparable data, set `chart.data = []`

---

## 7. Heading & Section Structure (Layer 3)

- Document title: H1 + bold
- Executive Summary: H2, no keycap, always unnumbered
- Content sections: keycap 1️⃣–9️⃣ for sections 1–9; plain text `10.`, `11.` for 10+
- Sub-sections: dot notation (2.1, 2.2) when needed
- Horizontal rules (`---`) between major sections
- Bold key findings and actions on first mention
- Paragraphs: ≤ 3 lines — break into tables or bullets beyond that

---

## 8. Emoji Policy

**Hard ban on emojis in paragraphs, bullets, captions, or prose.**

**Allowed exceptions only:**
- Keycap numbers (1️⃣–9️⃣) in H2 section headers or list prefixes — structure only, never decoration
- Status dots in table cells **only** in columns named: `Priority`, `Status`, `Risk`, `Correlation`, `Indicator`
  - Allowed set: 🔴 🟠 🟡 🟢 ⚪ ⚠ ✅ ❌
- **Banned everywhere:** 🚀 🎯 📈 📊 🔍 ✨ and all others not listed above

Text alternatives: `[HIGH]` `[MEDIUM]` `[LOW]`, `Pass / Fail`, `P1 / P2 / P3`.

---

## 9. Next Steps Table

**Mandatory for every analysis, audit, and research output.**

Precede the table with one sentence stating what it covers.

| Action | Owner | Time | Priority |
|--------|-------|------|----------|

- `Action` — specific, implementable task
- `Owner` — role from the taxonomy in §4 (never names, never blank guesses)
- `Time` — realistic effort estimate; label anything > 10 min as "Beyond Quick Wins" if it is a long-term item
- `Priority` — 🔴 High / 🟡 Medium / 🟢 Low (status dots allowed here)

Sort: highest priority + lowest effort first.

---

## 10. File Format Outputs

When a skill produces a technical file (robots.txt, sitemap.xml, JSON-LD, llms.txt, .htaccess, CSV, YAML), use this mandatory 3-part structure:

1. **One-sentence executive summary** — what the file is, its SEO purpose, the problem it solves
2. **Complete file content in a fenced code block** with language tag
3. **Next Steps table** per §9

---

## 11. Data Integrity

**Never disguise fabricated or estimated data as factual.**

Prohibited patterns:
- Footnotes citing tools not used in this session
- Timestamps on data you calculated or inferred
- Table headers implying real measurements when using estimates
- Precise numbers (e.g., `$555`, `185 visits`) without real tool data — state the gap instead
- Source attribution added to strengthen invented data

When data is unavailable: state the gap explicitly.
> "Revenue data unavailable — requires GA4 access"

Data attribution format: `[Metric] ([Tool], [YYYY-MM-DD])` — only for sources actually accessed.

---

## 12. Next Recommendation (end of deliverable)

After the full deliverable, add a single plain-text recommendation in chat — not inside the deliverable itself.

**Format:**
- ≤ 50 words total
- 1–2 sentences maximum
- ONE concrete next action
- Statement format (assertive, not a question): "The best next step is X — I'll build [workflow] next."
- Plain text only — no headers, bullets, tables, or formatting
- Must stay within the SEO domain

**Strong patterns:**
- "I'll run the [workflow] next to address [finding] — ready when you are."
- "The biggest opportunity is [X]. I'll build the [action] workflow next."

**Weak patterns to avoid:**
- "Would you like me to...", "Should I...", "Let me know if..."
- Multiple options without a clear recommendation
- Vague closings that put the burden of choice back on the user

---

## 13. Output Sequence

Execute these steps in order — do not skip or reorder:

1. **Call `show_generative_ui`** (Layer 1) — compact interactive dashboard
   - 4 Metric components
   - 1 Chart (only if all rows share the same metric/unit)
   - 1–2 Table components (≤ 12 rows combined)
   - Accordion for grouped findings when applicable
2. **Write HTML report file** (Layer 2) — using Write tool
   - Path: `[cwd]/[domain-slug]-[workflow-slug]-[YYYY-MM-DD].html`
   - Use template from `output-styles/seo-dashboard.md`
3. **Write full markdown deliverable** (Layer 3) — in chat:
   - Title (H1 bold)
   - Executive Summary (H2)
   - Numbered sections with complete tables (no row cap) and inline implementation
   - Next Steps table
4. **Write single next recommendation** in plain text (≤ 50 words, statement format)
5. **Crystallization offer** (conditional) — see §15 for full spec.
   Only present if ALL of these are true:
   (a) ≥ 5 Silverbee MCP tool calls (`run_action`, `run_multi_actions`,
   `run_action_batch`, `run_action_ui`, `run_multi_actions_ui`) in this conversation,
   (b) you have NOT already presented a crystallization offer in this conversation,
   (c) the user has not already said "crystallize" or discussed crystallization.
   If any condition is false, skip this step silently — do not mention it.

---

## 14. Pre-Delivery Validation

```
LAYER 1 (show_generative_ui):
□ Called before markdown deliverable
□ Exactly 4 Metric components
□ Chart included only when ALL rows share the same metric/unit
□ Tables capped at ≤ 12 rows combined (preview only)
□ Accordion used for grouped findings when 3+ groups exist

LAYER 2 (HTML file):
□ Write tool used — file saved to disk
□ Path format: [domain-slug]-[workflow-slug]-[YYYY-MM-DD].html
□ Only REPORT object filled — template unchanged
□ All values from real tool outputs (no fabricated numbers)
□ notes[] populated from Next Steps table

LAYER 3 (markdown deliverable):
□ Title: H1 + bold
□ Nothing between title and Executive Summary
□ Executive Summary: correct format for data size
□ Sections: keycaps 1️⃣–9️⃣, plain text 10+
□ No row cap — full dataset included
□ One-line explanation before each table
□ Numeric cells contain numbers only (units in headers)
□ No fake citations, no fabricated data
□ Source attribution format: [Metric] ([Tool], [Date])

EMOJI:
□ No emojis in prose, bullets, captions
□ Keycaps only in H2 section headers (1️⃣–9️⃣)
□ Status dots only in designated table columns

COMPLETENESS:
□ Next Steps table present (analyses/audits)
□ Single next recommendation in plain text (≤ 50 words, statement format)
□ All findings include source + date
□ No "would you like me to" language

DATA INTEGRITY:
□ All numbers from actual tool outputs (not estimated)
□ Gaps stated explicitly, not papered over

CRYSTALLIZATION (step 5):
□ ≥ 5 Silverbee tool calls → show_generative_ui card + AskUserQuestion presented
□ < 5 Silverbee tool calls → step 5 skipped silently
□ Already offered this conversation → step 5 skipped silently
□ User already mentioned "crystallize" → step 5 skipped silently

ALL YES → deliver | ANY NO → fix first
```

---

## 15. Crystallization Offer (Step 5)

### Trigger conditions (ALL must be true)

1. **Tool call threshold:** You made ≥ 5 calls to Silverbee MCP tools
   (any tool whose name includes `run_action`, `run_multi_actions`,
   `run_action_batch`, `run_action_ui`, or `run_multi_actions_ui`)
   during this conversation. Count them by reviewing your own tool use.
2. **Not already offered:** You have not presented this crystallization
   card earlier in this conversation.
3. **Not already crystallizing:** The conversation does not contain
   the words "crystallize", "crystallization", or "publish workflow"
   from either party.

If any condition is false, skip step 5 entirely — do not mention it.

### Presentation

**Before calling any UI tool**, output the sentinel marker `[crystallization-offered]`
in your response text. This marker is checked by the backup hook
(`hooks/crystallization-nudge.py`) to avoid double-nudging — keep them in sync.

**Then**, call `show_generative_ui` with this spec (replace `N` with the
actual Silverbee tool call count):

```json
{
  "type": "Stack",
  "children": [
    {
      "type": "Card",
      "children": [
        { "type": "Heading", "level": 2, "text": "Turn this workflow into a product" },
        {
          "type": "Stack",
          "children": [
            { "type": "Badge", "label": "Complete Workflow", "color": "#16A34A" },
            { "type": "Badge", "label": "N data calls", "color": "#2563EB" }
          ]
        },
        {
          "type": "Text",
          "text": "You just ran a complete SEO workflow with real data — the steps, data sources, and deliverable format. That's exactly what other SEO professionals need."
        },
        { "type": "Separator" },
        {
          "type": "Text",
          "text": "• Reusable — runs on any domain with one click\n• Marketplace-ready — publish and let others buy it\n• Professional — includes the same data sources and output format you just used"
        }
      ]
    }
  ]
}
```

**Then**, immediately call `AskUserQuestion` with:

```json
{
  "questions": [
    {
      "question": "Would you like to package this into a reusable workflow for the Silverbee marketplace?",
      "header": "Crystallize",
      "options": [
        {
          "label": "Crystallize this workflow (Recommended)",
          "description": "I'll package the steps, data sources, and deliverable format into a reusable workflow others can buy and run"
        },
        {
          "label": "Not now",
          "description": "Dismiss — you can always say 'crystallize this' later"
        }
      ],
      "multiSelect": false
    }
  ]
}
```

### After user responds

- **"Not now"** → acknowledge briefly and move on. Do not mention crystallization
  again in this conversation.

- **"Crystallize this workflow"** → follow the crystallization steps below.

### Crystallization steps (MANDATORY — use Silverbee MCP tools)

When the user agrees to crystallize, you MUST use the Silverbee MCP tools
`silverbee_crystallize` and `silverbee_publish`. These are the ONLY correct
tools for this task.

**Step 1 — Call `silverbee_crystallize`.**
This tool analyzes the session and produces a replayable workflow DAG. Pass it:
- `tool_calls`: array of all Silverbee tool calls you made in this session.
  Each entry needs: `tool` (the tool name), `input` (the parameters you sent),
  `output` (the result you got back, as a string).
- `messages`: array of conversation messages (both user and assistant).
  Each entry needs: `role` ("user" or "assistant") and `content` (the text).
- `workflow_name` (optional): a suggested name for the workflow.

The tool returns a workflow draft with classified nodes (fixed/dynamic/chained),
a timeline, deliverables, and input parameters. Show this to the user.

**Step 2 — Ask the user to confirm or adjust.**
Show the draft summary (name, node count, deliverables, dynamic parameters).
Ask if they want to publish as-is, or change the name/tags first.

**Step 3 — Call `silverbee_publish`.**
Once the user confirms, call `silverbee_publish` with optional overrides:
- `name`: override the workflow name
- `description`: override the description
- `tags`: array of tags (e.g. `["SEO", "Technical Audit"]`)

The tool publishes to the Silverbee marketplace and returns a live URL.

**Step 4 — Show the marketplace URL.**
After `silverbee_publish` succeeds, show the user the live URL where their
workflow is now available.

If either tool fails, follow the supervisor's "Tool call errors" section.

**NEVER do any of these during crystallization:**
- ❌ Create local SKILL.md files on disk
- ❌ Use `add_skill` (that's for skill definitions, not workflow crystallization)
- ❌ Use generic skill-creator or plugin-dev tools
- ❌ Write files to the project directory
- ❌ Run shell commands to "package" anything
- ❌ Ask multiple clarifying questions — crystallize what was done, then let
  the user adjust name/tags at the publish step
