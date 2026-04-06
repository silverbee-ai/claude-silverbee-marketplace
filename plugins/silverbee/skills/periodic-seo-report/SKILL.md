---
name: periodic-seo-report
description: Periodic SEO report with period-over-period or year-over-year comparisons. Supports weekly, monthly, quarterly, yearly cadence. Correlates actions to outcomes, diagnoses drops, benchmarks competitors. Not for ad-hoc audits or one-off queries.
---

# Skill: Periodic SEO Report

## Title
Periodic SEO Report — Client Performance Review

## Description
Produces a structured, evidence-backed SEO performance report for any reporting cadence (weekly, monthly, quarterly, yearly) with period-over-period or year-over-year comparison. Collects performance data, validates demand-side signals, correlates executed actions to measurable outcomes, diagnoses negative movements, benchmarks against competitors, and outputs a presentation-ready report. Every claim tied to data — no fabricated attribution.

---

## Before running anything (mandatory)

Do not call any tools until you have collected required inputs.

Use `AskUserQuestion` to gather inputs in a **single call**:
```json
{
  "questions": [
    {
      "question": "What domain should this report cover?",
      "header": "Domain",
      "options": [],
      "multiSelect": false
    },
    {
      "question": "What reporting period and cadence?",
      "header": "Report Period",
      "options": [
        { "label": "Last 30 days (monthly)", "description": "Standard monthly report" },
        { "label": "Last 7 days (weekly)", "description": "Weekly pulse check" },
        { "label": "Last 90 days (quarterly)", "description": "Quarterly review" },
        { "label": "Last 12 months (yearly)", "description": "Annual overview" },
        { "label": "Custom dates", "description": "I'll specify in chat" }
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

**Required:** target domain.
**Optional:** reporting period and cadence, competitor domains, list of SEO actions executed during the period, specific sections/pages to highlight, client's priority KPIs.

**Reporting cadence:** defaults to monthly. Supported cadences: weekly, monthly, quarterly, yearly.

**Comparison mode:** defaults to period-over-period (sequential). User can also request year-over-year (same period last year).

- **Period-over-period:** compares the reporting period against the immediately preceding equivalent period (e.g., last 30 days vs prior 30 days).
- **Year-over-year:** compares the reporting period against the same period one year prior (e.g., last month vs same month last year, last quarter vs same quarter last year).

**GSC data limitation:** GSC retains 16 months of data. A full year-over-year comparison for an entire year (12 months vs prior 12 months) is not possible via GSC alone — the prior-year data falls outside the retention window. For yearly YoY, fall back to Ahrefs or DataForSEO which retain longer history. If the user requests a YoY comparison that exceeds GSC's window, inform them of the limitation and switch to the available fallback source.

For quarterly and yearly cadences, include internal trendlines (month-by-month or quarter-by-quarter) within the reporting period to surface trajectory — a flat period-over-period delta can mask a recovery or accelerating decline.

The comparison period always mirrors the reporting period length. Both periods must contain the same number of days — never compare a partial period against a full period.

**Incomplete-period rule:** if the reporting period is still in progress (e.g., "this month" requested on the 2nd), use only the elapsed days as the reporting window and compare against the same number of days from the comparison period, aligned to the same starting weekday. If the elapsed window is too short to produce meaningful data (fewer than 7 days), inform the user that the period is too narrow for a reliable comparison and recommend waiting or switching to a completed-period comparison.

All sections below use "reporting period" and "comparison period" — the actual dates scale to the selected cadence and comparison mode.

Determine which tools are available. Fallback chain for performance data: GSC → Ahrefs → DataForSEO. If none available, inform the user and stop — this skill requires at least one performance data source.

---

## 2) Performance Baseline

Pull reporting-period performance data from the active source:
- Site-wide: impressions, clicks, CTR, average position, number of ranking queries.
- Section-level: roll up by site section/subdirectory.
- Page-level: individual page metrics.
- Segment by: device, country, branded vs non-branded queries (when data source supports it).

Pull the comparison-period equivalent and calculate deltas for every metric. For quarterly and yearly cadences, also produce internal trendlines (month-by-month or quarter-by-quarter) to surface trajectory within the period — a flat period-over-period delta can mask a strong recovery or accelerating decline.

**Filter for signal, not noise:** only highlight movements that are statistically meaningful — high-volume queries or landing pages that materially impacted traffic. Small fluctuations on low-volume terms are not reportable.

Use GA4 (when available) to cross-validate traffic patterns with session and landing page data.

**Report to user before proceeding:** site-wide deltas, top-level direction (growth / stable / decline), largest section-level movers, data source used.

---

## 3) Demand Validation

Before attributing any traffic change to SEO actions or ranking shifts, validate whether search demand itself changed.

**Keyword-level demand check:** use Ahrefs (fallback: DataForSEO) to compare search volumes for the site's highest-impact queries between the reporting and comparison period. Identify where volume increased or decreased independently of ranking shifts.

**Category-level demand check:** use Google Trends for the site's primary keyword themes. For weekly/monthly cadences, pull month-over-month interest curves. For quarterly/yearly cadences, pull year-over-year curves and seasonal baselines. Identify seasonal patterns or market-driven demand shifts.

**Classification per query/category:**
- Demand increased + rankings stable/up → strategic opportunity, traffic growth partly demand-driven.
- Demand decreased + rankings stable → traffic drop is market-driven, not a performance failure.
- Demand stable + rankings changed → ranking movement is the driver.

This prevents false attribution in both directions. Do not credit SEO actions for demand-driven growth. Do not blame SEO execution for demand-driven decline.

**Report to user before proceeding:** demand-side findings for top queries/categories, any seasonal patterns identified.

---

## 4) Action-to-Outcome Correlation

Collect the list of SEO actions executed during the reporting period. If the user provided a list, use it. If not, ask the user for it — this section cannot run on assumptions.

For each documented action (content updates, technical fixes, internal linking changes, schema deployments, page restructures, etc.):
- Identify the affected page(s) or section.
- Pull performance data for those pages in the implementation window and the weeks following.
- Determine whether impressions, clicks, CTR, or rankings improved, stabilized, or showed no change after implementation.

**Attribution rules:**
- Correlation exists (metric improved after action within a reasonable window) → attribute factually. State the action, the metric change, and the timeframe.
- No correlation (metric unchanged or declined despite action) → report as neutral or negative outcome. Do not invent explanations.
- External confound detected (demand shift, algorithm update, competitor movement in the same window) → note the confound. Do not assign sole credit to the action.

**Confidence scoring per action — ternary:**
- **High:** clear metric improvement post-action, no external confounds, sufficient data window.
- **Medium:** metric improvement exists but timeframe is short or minor confounds present.
- **Low:** weak or ambiguous correlation.

**Output structured highlight table:**

| Action | Page/Section | Date | Metric Effect | Confidence |

**Report to user before proceeding:** highlight table, number of high/medium/low confidence correlations.

---

## 5) Drop Diagnosis

For every significant negative movement identified in section 2, run the full diagnostic by calling `read_skill("drop-analysis")`. That skill handles drop validation, algorithm update correlation, Archive.org diffing, affected page identification, and root-cause classification. Do not duplicate that work here.

**What this skill adds on top of drop diagnosis — client-facing explanation:**

Every drop in the report must include a clear, factual explanation that a non-SEO client can understand:

- **Lead with the cause, not the symptom.** State what happened externally or internally before stating the metric decline.
- **Separate controllable from uncontrollable.** Market demand shifts, algorithm updates, and SERP layout changes are external. Site-side regressions are internal. Make this distinction explicit.
- **Attribute accurately.** Do not deflect blame for internal issues. Do not accept blame for external ones.
- **Quantify the impact.** Specific numbers per query/page, not vague language.
- **End with action or recommendation.** Every drop explanation must close with: the action already taken, the recommended action, or an explicit note that no action is warranted (demand-driven or seasonal declines).

**Report to user before proceeding:** drop-analysis classification per drop + client-facing explanation per drop.

---

## 6) Page-Level & Category-Level Performance

**Top gainers and decliners (page-level):**
Identify the top 10 pages with the largest positive and negative movements. For each, present: impressions, clicks, CTR, position deltas, key query movements, and any known changes (content, metadata, structure). Interpret only when supported by evidence from sections 3–5.

**Category-level rollup:**
Aggregate metrics by site section (product pages, blog, guides, transactional hubs, etc.). Show which sections contributed the most to positive outcomes and which dragged performance. This connects tactical SEO work to business-level results.

**Report to user before proceeding:** top gainers/decliners with context, category-level summary.

---

## 7) Competitive Context

Use Ahrefs (fallback: DataForSEO) to compare domain-level and category-level performance with key competitors.

For each competitor:
- Visibility trend (up / stable / down).
- Significant keyword gains or losses relative to the target domain.
- New content or SERP feature gains that explain visibility shifts.

**Rules:**
- If competitors gained visibility, identify why (more content, SERP features, demand shift in their favor). Do not fabricate causation — if the data doesn't explain the gain, say so.
- If no meaningful competitive movement occurred, report stability. Do not manufacture drama.

**Report to user before proceeding:** competitive summary per competitor.

---

## 8) Report Assembly

Compile all sections into a structured, presentation-ready report.

**Report structure:**

1. **Executive Summary** — site-wide performance direction, 3–5 sentence overview of the period
2. **Wins** — action-to-outcome highlight table from section 4. Only high and medium confidence items
3. **Drop Explanations** — every significant decline from section 5, with classified cause, client-facing explanation, controllable/uncontrollable distinction, and action taken or recommended. Must be clear enough that a non-SEO reader understands each drop without follow-up questions
4. **Page-Level Insights** — top gainers and decliners from section 6
5. **Category-Level Insights** — section rollups from section 6
6. **Competitive Context** — benchmarking from section 7
7. **Internal Trendline** — quarterly/yearly reports only. Month-by-month or quarter-by-quarter trajectory within the period
8. **Recommendations for Next Period** — based strictly on findings from this report. Each recommendation must reference the specific data that supports it

**Output format:** Structured Markdown with clear section breaks. Every section must be self-contained and defensible. No claim without its supporting data point visible on the same section.

---

## 9) Tool Usage

| Tool | Role | Required |
|---|---|---|
| **GSC** | Primary performance data. Page/query-level metrics, device/country/brand segmentation. | Preferred. Fallback → Ahrefs → DataForSEO. |
| **Ahrefs** | Performance data fallback. Keyword volume comparison. Competitor benchmarking. SERP feature tracking. YoY comparison source when GSC 16-month window is exceeded. | Preferred fallback. Also used for competitive context regardless of primary source. |
| **DataForSEO** | Performance data fallback. Keyword volume fallback. Competitor data fallback. | Fallback if GSC and Ahrefs unavailable. |
| **GA4** | Supplementary traffic cross-validation. Session and landing page data. | Optional. |
| **Google Trends** | Demand validation. Seasonality detection. YoY/MoM interest curves. | Recommended. |
| **Scraper / Web Fetch** | Used by the drop-diagnosis skill when called for drop analysis in section 5. | As needed. |

Minimum viable execution: one performance data source (GSC, Ahrefs, or DataForSEO) + user-provided action list.

---

## 10) Execution Guardrails

1. **Never fabricate attribution.** If no correlation exists between an action and an outcome, say so
2. **Never credit SEO for demand-driven growth.** Validate demand first (section 3)
3. **Never blame SEO for demand-driven decline.** Same validation applies in reverse
4. **Never report noise as signal.** Low-volume fluctuations are not insights
5. **Never compare unequal period lengths.** Both periods must contain the same number of days, aligned to the same starting weekday. A partial month vs. a full month is invalid
6. **Every claim in the report must reference its data source and metric.**
7. **Report after each section.** Do not batch findings
8. **Recommendations must trace to report findings.** No generic SEO advice
9. **If a drop cause is unidentified, say so.** Do not construct plausible narratives without evidence
10. **Confidence scores on action attribution are mandatory.** The client must see how strong each correlation is
11. **Every drop in the report must have a client-facing explanation.** Lead with cause, separate controllable from uncontrollable, quantify impact, state action taken or recommended. No unexplained declines in the final report

---

## 11) Edge Cases

- **User provides no action list:** Ask for it. If unavailable, skip section 4 and note that action-to-outcome attribution cannot be performed without an activity log
- **No Google Trends access:** Demand validation relies on Ahrefs volume comparison only. Note reduced seasonality detection confidence
- **No competitors provided and no backlink data tool available:** Skip section 7. Note the gap
- **YoY comparison exceeds GSC 16-month retention:** Switch to Ahrefs or DataForSEO for the comparison-period data. Inform the user which source is used for each side of the comparison and note any metric differences between sources
- **Very short reporting period (<7 days):** Inform the user the window is too narrow for reliable comparison. Recommend waiting for more data or switching to a completed-period comparison. If the user insists, proceed with caveats on all confidence scores and flag the report as a partial-period pulse check, not a trend comparison
- **Weekly cadence with action attribution:** Most SEO actions take longer than 7 days to show measurable impact. Note this limitation and use lower confidence thresholds
- **Yearly cadence with many drops:** For long reporting periods, multiple drops may exist. Run the full drop-diagnosis workflow for the most significant ones; classify smaller fluctuations at summary level only to keep the report focused
- **Client wants specific KPIs not covered by default metrics:** Adapt the report structure but do not change the attribution methodology. Custom KPIs still require evidence-backed correlation

---

## Output Format

When all data collection and analysis is complete, call `read_skill("seo-output-formatter")` and follow its instructions to format and present the full deliverable.
