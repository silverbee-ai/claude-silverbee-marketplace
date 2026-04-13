---
name: drop-analysis
description: Diagnoses confirmed sudden organic drops in traffic, rankings, impressions, or visibility. Correlates GSC/Ahrefs data, Archive.org snapshots, and Google algorithm updates to determine root cause. Use only after a drop has been detected and validated via period comparison, or when a user explicitly requests drop analysis for a specific event. Not for routine performance comparisons, threshold-based flagging, gradual decay, or paid traffic.
---

# Skill: SEO Drop Diagnosis

## Title
SEO Drop Root-Cause Diagnosis

## Description
Investigates the root cause of a confirmed sudden organic drop event (detected via comparison or explicitly specified by the user). Correlates performance data (GSC → Ahrefs → DataForSEO), Archive.org site snapshots, and Google algorithm update timelines. Optionally enriched with GA4, Google Trends, Ahrefs Brand Radar, and SERP history. Minimum viable analysis requires one performance data source + Archive.org + Google algorithm update list.

---

## Before running anything (mandatory)

Do not call any tools until you have collected required inputs.

Use `AskUserQuestion` to gather inputs in a **single call**:
```json
{
  "questions": [
    {
      "question": "What domain or URL(s) should I analyze for the traffic drop?",
      "header": "Domain/URL",
      "options": [],
      "multiSelect": false
    },
    {
      "question": "Do you have an approximate date range for the drop?",
      "header": "Date Range",
      "options": [
        { "label": "Last 30 days", "description": "Recent drop detection" },
        { "label": "Last 90 days", "description": "Wider window for context" },
        { "label": "Specific dates", "description": "I'll specify in chat" },
        { "label": "Unknown — scan all available data", "description": "Agent identifies significant drops" }
      ],
      "multiSelect": false
    }
  ]
}
```

After collecting inputs, confirm them in a short text message and **wait for the user's go-ahead** before making any tool calls.

---

## Tool execution

Use this pattern for all data fetching:
1. `list_available_apps` — confirm which data sources are connected
2. `search_actions(query)` or `list_actions(app_name)` — find the right operation
3. `run_action(app_name, operation_id, input)` — execute

**MANDATORY — parallel execution:** Batch all independent queries into a single `run_multi_actions` call. Never call `run_action` in a sequential loop — that is a performance bug. On any app-specific error, try the fallback chain (see supervisor "Step 3") before stopping. On connection/auth errors (all tools failing), follow the supervisor's "Tool call errors" section.

---

## 1) Input

**Required:** target domain or URL(s).
**Optional:** approximate drop date range.

If the user provides a date range, scope the analysis to that window. If no date range is provided, the agent is responsible for identifying all significant drops in the available data and analyzing each one.

Determine the primary performance data source using this fallback chain:
1. GSC (preferred) → 2. Ahrefs → 3. DataForSEO.
Use whichever is available. Inform the user which source is active and note that Ahrefs and DataForSEO data are estimates, not absolute.

---

## 2) Drop Identification & Validation

Pull performance data from the active source (GSC → Ahrefs → DataForSEO) covering minimum 90 days before the reported drop through present — or, if no date range was provided, pull the maximum available history and scan for all significant drops. A significant drop must meet all three conditions:

1. **Magnitude:** ≥15% week-over-week decline in at least one of: clicks, impressions, or average position (position increase = rank loss).
2. **Persistence:** the decline does not recover within 2 weeks of the inflection point.
3. **Shape:** the decline is a step-function — a clear inflection — not a gradual slope. If the data shows gradual erosion without a visible inflection point, stop and inform the user: this skill diagnoses sudden drops; gradual decline requires a different analysis.

A one-week dip that recovers is volatility, not a drop. A gradual 15% decline over 6 months is decay, not an event. This skill is built for diagnosable events.

If multiple qualifying drops are found, list them all for the user and proceed through sections 3–6 for each one. Use GA4 as supplementary cross-check when available — it validates patterns but is not required.

**Seasonality gate:** Pull Google Trends data for the site's primary keyword themes over the same period. If the drop pattern mirrors a seasonal trend (same dip in the same period in prior years), report this to the user. If seasonal pattern is confirmed, stop the diagnostic and report findings. Do not proceed unless the user requests analysis regardless.

**Characterize the drop:**

- **What dropped** — traffic (clicks), impressions, rankings, or a combination. The drop type narrows the diagnostic path:
  - Impressions down + rankings stable → indexing or SERP feature displacement
  - Rankings down + impressions stable → position losses on existing queries
  - Rankings down + impressions down → visibility loss (algorithmic or structural)
  - Traffic down + impressions/rankings stable → CTR erosion (SERP layout change, title/snippet regression)
- **Inflection point** — the specific date or narrow range where a step-function drop is visible.
- **Scope** — site-wide, specific subdirectory/section, or specific page cluster.

**Report to user before proceeding:** seasonality check result (seasonal / not seasonal / insufficient data), number of significant drops identified (if agent-detected), drop type per inflection, inflection date/range, magnitude (% and absolute), scope.

---

## 3) Algorithm Update Match

Scrape the Google algorithm update history from this URL:
`https://status.search.google.com/products/rGHU1u87FJnkP6W2GwMi/history`

This is the only external dataset not available through existing tools. Extract all logged updates: name, rollout start/end dates, type, description.

If scrape fails → web search for Google algorithm updates covering the drop period. Cross-reference: Search Engine Land, Search Engine Roundtable, Google SearchLiaison.

**Match logic:**
- Inflection falls within or ≤5 days after a confirmed rollout → **match**
- No update aligns with the inflection window → **no match**

Either the timing aligns or it doesn't.

If match → research what that update targets (official Google statements, industry analysis). Distill into a precise update hypothesis: what page types/signals this update re-weights.

**Report to user before proceeding:** updates within ±30 days of inflection with rollout dates, match or no match with the dates that justify the call, update hypothesis if match found.

---

## 4) Site State via Archive.org

Use Archive.org to fetch snapshots of the target URL at four points relative to the inflection: ~30 days before (baseline), ~7 days before, on or near inflection date, ~7 days after.

**Diff snapshots. Only SEO-relevant changes matter:**

- Structural: navigation, internal linking, template/layout, schema/structured data.
- Content: heading hierarchy, content additions/removals, topic focus, meta tags.
- Technical: canonicals, noindex/nofollow, hreflang, JS rendering, redirects.

**Binary classification:**
- **Site changed before the drop:** list exactly what changed.
- **Site did not change:** snapshots are functionally identical.

**Report to user before proceeding:** exact changes found or explicit confirmation of no changes, whether changes preceded or followed the drop.

---

## 5) Affected Pages & SERP Shifts

**Identify losses:**
Using the active performance data source, sort by the declining metric (clicks, impressions, or position change) in the drop window. Top 10–20 losses.

**Group affected pages by:** content type (blog, product, landing, category), topic cluster, shared characteristics (thin, outdated, duplicate intent, affiliate-heavy, weak E-E-A-T).

**SERP before/after comparison for top 3–5 impacted queries:**
- Use DataForSEO or Ahrefs (whichever is available) for historical SERP data from before the inflection. If neither available, search now and note the before-state is inferred, not observed.
- Search those queries now for current SERP state.
- Compare: result type changes, who replaced the affected pages, what those pages do differently, new SERP features displacing organic listings.

**Cross-reference with update hypothesis (if section 3 found a match):** evaluate each affected page against the update hypothesis. Does the page actually exhibit the weakness the update targets? Do not force a fit. If the page doesn't match the update's targeting profile, say so.

**Backlink check on affected pages (when Ahrefs available):** pull backlink profiles of top affected pages. Check for toxic/spammy referring domains, recent link losses, anchor text anomalies. Relevant regardless of update type.

**AI search visibility check (if Ahrefs Brand Radar available):** check if LLM/AI search mentions declined in the same window. Traditional + AI visibility both dropped → stronger content quality/authority signal. Traditional dropped but AI mentions stable → points toward technical/structural or SERP layout causes. Supplementary signal, not primary.

**Competitor substitution for top 3–5 lost queries:** who ranks now, what concrete differences exist (structural, content, authority).

**Report to user before proceeding:** affected pages ranked by loss magnitude, categorization, SERP before vs after per query (data-backed where possible), backlink findings, AI visibility status if available, update hypothesis match assessment if applicable, competitor differences.

---

## 6) Root-Cause Classification

Synthesize all sections into a classification.

| Classification | Required Evidence |
|---|---|
| **Algorithmic re-weighting** | Section 3: confirmed match. Section 4: no significant site changes. Section 5: affected pages fit the update's target profile. |
| **Intent shift** | Section 5: SERP composition changed to different content types/formats. Competitors serve different intent. |
| **Technical/structural signal dilution** | Section 4: Archive.org confirms structural changes before drop. Section 5: affected pages lost link equity or context signals. |
| **Content regression** | Section 4: content thinned/broadened. Section 5: competitors outperform on depth, expertise, freshness. |
| **SERP feature displacement** | Section 2: impressions/rankings stable but clicks dropped. Section 5: new SERP features absorbed clicks. |
| **Indexing/crawl issue** | Section 2: impressions dropped sharply. Section 4: technical changes (noindex, canonical errors, robots changes) detected. |
| **Link profile degradation** | Section 5: significant toxic backlinks, recent link losses, or anchor anomalies on affected pages (requires Ahrefs). |
| **Combined** | Evidence supports multiple classifications. Specify which and how they interact. |

**Confidence — binary:**
- **Confirmed:** evidence from multiple sections converges. Timeline aligns. Affected page profile matches.
- **Inconclusive:** evidence is partial, conflicting, or insufficient. State what was found, what wasn't, and what additional data would resolve it.

The evidence supports the conclusion or it doesn't yet.

**Output:** drop type and magnitude (section 2), seasonality status (section 2), algorithm update match or no match (section 3), site changes or no changes (section 4), affected pages, SERP shifts, backlink status (section 5), root-cause classification with confidence, if inconclusive: what's missing to complete the diagnosis. Brief, structured, no padding.

---

## 7) Tool Usage

| Tool | Role | Required |
|---|---|---|
| **GSC** | Performance data (clicks, impressions, CTR, position by page/query). | Preferred. Fallback → Ahrefs → DataForSEO. |
| **Ahrefs** | Performance data fallback. Backlink analysis. SERP history. | Preferred fallback for GSC. |
| **DataForSEO** | Performance data fallback. Historical SERP data for before/after comparison. | Fallback if GSC and Ahrefs unavailable. |
| **Archive.org** | Site snapshots around the inflection point. | **Mandatory** for code and content change effects. |
| **Scraper / Web Fetch** | Google Search Status page scrape (section 3). Archive.org snapshots. | **Mandatory** for algorithm update list. |
| **Google Search** | Current SERP composition for affected queries. | **Mandatory.** |
| **Google Trends** | Seasonality validation in section 2. | Recommended. |
| **GA4** | Supplementary traffic cross-check. Validates patterns. | Optional. |
| **Ahrefs Brand Radar** | AI/LLM mention changes in the drop window. | Optional. |
| **Web Search** | Algorithm update research, industry analysis. | Fallback for Status page scrape. |

---

## 8) Execution Guardrails

1. **Never fabricate data.** Tool call fails or returns incomplete → state the gap.
2. **Never skip Archive.org.** Even with clear algorithm match.
3. **Never skip seasonality check.** Rule it out before investing in root-cause analysis.
4. **Correlation is not causation.** "Timing aligns with", "consistent with" — never "caused by".
5. **Show the timeline.** User must see the temporal relationship between updates, site changes, and the inflection.
6. **Page-level specificity.** Which pages, which queries, how much.
7. **Report after each section.** Do not batch findings.
8. **Do not speculate.** Inconclusive with a gap list beats a forced narrative.
9. **Do not soften findings.** If the site caused its own drop, say so. If Google's update caused it, say so. If you don't know, say that.

---

## 9) Edge Cases

- **No Archive.org snapshots:** State the gap. Ask user for change logs or CMS history if the insist on code and content modifications effect analysis.
- **Multiple updates overlap the inflection:** Evaluate each against the affected page profile. If both plausible, say so.
- **No SERP history tools available (DataForSEO + Ahrefs both unavailable):** Note reduced confidence in before/after comparison.
- **No backlink tools available:** State the gap. Skip link profile analysis, note it as a missing input in the classification.
- **User disputes findings:** Present the data.

---

## Step Count: 6

| # | Step | Duration Estimate |
|---|------|-------------------|
| 1 | Domain resolution | 2s |
| 2 | GSC performance comparison | 5–8s |
| 3 | Algorithm update correlation | 3–5s |
| 4 | Archive.org snapshots | 5–10s |
| 5 | Ahrefs ranking changes | 3–5s |
| 6 | Output generation | 3–5s |

## Step Criticality

| Step | Critical | Fallback |
|------|----------|----------|
| Domain resolution | Yes | Cannot proceed |
| GSC performance comparison | Yes | Cannot proceed |
| Algorithm update correlation | No | Skip correlation, note in output |
| Archive.org snapshots | No | Skip historical comparison, note in output |
| Ahrefs ranking changes | No | Use GSC data only, note in output |

## Dashboard Template

Use `render_template("drop-analysis", data)` via the silverbee-mcp MCP.

| Field | Type | Description |
|---|---|---|
| `title` | string | Dashboard heading |
| `metrics.trafficDrop` | string | Traffic drop magnitude |
| `metrics.affectedPages` | string | Number of affected pages |
| `metrics.likelyCause` | string | Most likely root cause |
| `metrics.recoveryActions` | string | Recommended recovery actions count |
| `chart.data[]` | array of `{period, traffic}` | Traffic trend chart (period: string, traffic: number) |
| `affectedPages.rows` | string[][] | Affected pages table rows |
| `rankingDrops.rows` | string[][] | Ranking drops table rows |

All metric values are **strings** (not numbers). Table `rows` are `string[][]` (arrays of string arrays, not objects).

For custom specs or troubleshooting, load the `show-generative-ui` skill.

---

## Output Format

When all data collection and analysis is complete, call `read_skill("seo-output-formatter")` and follow its instructions to format and present the full deliverable.
