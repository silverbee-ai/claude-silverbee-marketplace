---
name: search-performance-monitoring
description: On-demand comparison of organic search performance metrics across two defined periods. Detects and flags significant changes in rankings, clicks, impressions, and conversions at site, folder, URL, or keyword level. Designed for performance monitoring and change detection — not root-cause analysis.
---

# Skill: Search Performance Monitoring

## Title
Search Performance Monitoring

## Description
On-demand tracking of organic search performance for a domain or URL. Detects significant shifts in rankings, traffic, and conversions. Reports *what changed* — does not diagnose *why*.

---

## 1) Input

**Required:**
- Domain or specific URL
- Comparison timeframe (e.g., DoD, WoW, MoM)

**Auto-inferred from GSC** (override only if the user specifies):
- Target geo / country, language, currency

---

## 2) Definitions & Thresholds

Internalize before executing. These govern all decisions in subsequent sections.

- **Sharp Change:** Any metric shift exceeding 15% vs. the comparison period — applies to increases and decreases equally.
- **Drop Validation** A change is a drop only if the comparison period value is lower than the baseline period value and meets the Sharp Change threshold (15%+). If the value increased or stayed the same, it is not a drop. If the baseline value is zero or missing, do not classify as a drop.
- **Stable:** Any metric shift under 3%. Do not flag unless a Top 3 keyword is affected.
- **Low Signal:** Keywords that account for less than 1% of total domain impressions in the baseline period, or URLs that account for less than 1% of total domain clicks in the baseline period. Report separately — do not mix with main findings.
- **Baseline:** The previous 90 days, used solely to calculate each keyword's and URL's share of total domain impressions/clicks for Low Signal filtering. Not used for delta calculations — those use the user-defined comparison period.
- **CTR Evaluation:** Read CTR changes alongside current average position. A CTR drop is only meaningful if position held Stable. If position dropped, the CTR drop is expected — do not flag independently.
- **Position Evaluation:** Average Position in GSC is impression-weighted. Evaluate position shifts alongside Impressions change. If Impressions grew significantly, average position may drop due to new low-ranking queries entering the data — not because existing rankings fell.
- **Branded vs. Non-Branded:** Traffic and position metrics must be segmented by branded and non-branded queries. A total traffic drop driven entirely by branded query decline is a different problem from a non-branded drop and must not be reported as a single finding.
- **Device Segmentation:** Clicks, Impressions, CTR, and Position must be broken down by device (Mobile / Desktop / Tablet). Mobile and Desktop can move in opposite directions — a combined metric can mask both a loss and a gain.
- **Date Granularity:** For DoD monitoring or daily trend analysis, pull data using dimension=date from the GSC API. Do not rely on aggregated period totals when daily patterns are relevant.
- **Position Scope:** Only report average position for keywords with sufficient impressions to produce a reliable signal. Suppress long-tail keywords with very low impressions from position reporting — flag as Low Signal.

---

## 3) Guardrails

Apply throughout the entire execution without exception.

- Pull all data directly from GSC and GA4 APIs. No manual entry or estimates.
- Before flagging any drop, check for seasonal context. Label each alert as **Seasonal** or **Anomalous**. For MoM or longer comparisons, account for day-of-week composition differences — a month with more weekend days than the previous one may naturally show lower traffic for B2B sites.
- Always segment findings by Branded vs. Non-Branded before reporting. Never report a combined traffic figure as a single finding.
- Always segment Clicks, Impressions, CTR, and Position by device. Flag device-level divergence explicitly.
- Do not flag CTR drops when position also dropped — this is expected behavior.
- Do not flag average position drops without checking whether Impressions volume also changed.
- Suppress Low Signal findings from main tables. Report them in a dedicated Low Signal section at the end of the output.
- Before flagging a conversion drop, note whether GA4 tracking integrity can be confirmed. If the conversion drop is disproportionately larger than the traffic drop, flag as **Tracking Check Required**.
- If data is unavailable or an API call fails, state this explicitly in the output. Do not infer or substitute missing data.

---

## 4) Scope Lock

Resolve both before proceeding. Do not begin analysis until confirmed.

- **Monitoring Level:** Site-wide, Folder-specific, or URL-specific?
- **Comparison Dates:** Confirm the exact date ranges being compared.

---

## 5) Keyword Monitoring

Pull from GSC API. Segment all findings by Branded / Non-Branded:

- List keywords with a Sharp Change in average position — only include keywords above the Low Signal threshold.
- List keywords with a Sharp Change in CTR — flag only if position held Stable. Note current average position alongside every CTR finding.
- Separate all findings into **Gainers** and **Losers**.
- Prioritize keywords in or near Top 10.
- Collect Low Signal keywords separately.

---

## 6) Traffic Monitoring

Pull from GSC API at the URL level. Segment all findings by Device (Mobile / Desktop / Tablet):

- List URLs with a Sharp Change in Clicks or Impressions — only include URLs above the Low Signal threshold.
- List URLs with a Sharp Change in CTR — flag only if position held Stable.
- Separate all findings into **Gainers** and **Losers**.
- For Losers, note whether the drop is in Clicks only, Impressions only, CTR only, or a combination.
- Flag any URL where Mobile and Desktop trends diverge significantly.
- Collect Low Signal URLs separately.

---

## 7) Conversion Monitoring

Pull from GA4. **Skip this section entirely and state so in the output if GA4 is not connected.**

- Check whether traffic changes on key pages correspond to conversion changes.
- Flag pages where traffic held but conversions dropped, or vice versa.
- If the conversion drop is disproportionately larger than the traffic drop, flag as **Tracking Check Required** — do not assume an SEO issue without ruling out a GA4 event tracking problem first.

---

## 8) Output

Begin with an **Executive Summary** — one sentence stating overall status (**Stable / Needs Attention / Critical**) and the single most important finding. Include a one-line Branded vs. Non-Branded split summary.

Then produce the following tabs:

### Tab 1 — Performance Overview

| Metric | Current Period | Previous Period | Delta (%) | Status |
|---|---|---|---|---|
| Clicks (Total) | | | | |
| Clicks (Branded) | | | | |
| Clicks (Non-Branded) | | | | |
| Impressions | | | | |
| Avg. CTR | | | | |
| Avg. Position | | | | |
| Organic Conversions (GA4) | | | | |

### Tab 2 — Keyword Shifts

| Keyword | Type | Previous Position | Current Position | Position Delta | Impressions Change | Previous CTR | Current CTR | CTR Delta | CTR Flag | Label |
|---|---|---|---|---|---|---|---|---|---|---|
| "keyword x" | Non-Branded | 4 | 11 | -7 | Stable | 8% | 3% | -5% | — | Loser |
| "keyword y" | Non-Branded | 3 | 3 | 0 | Stable | 12% | 6% | -6% | CTR Drop | Loser |
| "brand name" | Branded | 1 | 1 | 0 | -40% | 35% | 34% | -1% | — | Loser |

### Tab 3 — Page-Level Traffic Shifts

| URL | Device | Previous Clicks | Current Clicks | Delta (%) | Impressions Change | CTR Change | CTR Flag | Label |
|---|---|---|---|---|---|---|---|---|
| /example-page/ | Mobile | 900 | 450 | -50% | -49% | Stable | — | Loser |
| /example-page/ | Desktop | 300 | 310 | +3% | Stable | Stable | — | Stable |
| /another-page/ | Mobile | 800 | 780 | -2.5% | Stable | -30% | CTR Drop | Loser |

### Tab 4 — Conversion Impact *(skip if GA4 unavailable)*

| URL | Traffic Change | Conversion Change | Note |
|---|---|---|---|
| /product-page/ | -30% | -55% | Tracking Check Required |

### Tab 5 — Low Signal (for reference only)

| Entity | Type | Reason Suppressed | Delta (%) |
|---|---|---|---|
| "obscure keyword" | Keyword | <1% of domain impressions | -60% |
| /tiny-page/ | URL | <1% of domain clicks | -80% |

Add a short escalation block at the end of Section 8 (Output), after the Low Signal tab:

---

**Escalation Paths**

**Drop detected → Root-cause diagnosis:**
If any URL or keyword shows a Sharp Change loss, call `read_skill("drop-analysis")` and pass: the affected URLs/keywords, the inflection date range, and the metric type that dropped (clicks, impressions, rankings, or CTR). Monitoring identifies *what* dropped — drop diagnosis identifies *why*.

**Multiple losses or Critical status → Full periodic report:**
If the executive summary status is **Critical**, or if 3 or more Sharp Change losers are identified, recommend triggering `read_skill("periodic-seo-report")` for full diagnostic coverage — including action-to-outcome attribution, demand validation, competitive context, and client-facing narrative. Monitoring does not diagnose or attribute — escalate when detection alone is insufficient.

**Do not escalate automatically.** Both escalations are recommendations to the user/agent. The decision to run a full report or drop diagnosis involves context (client cadence, available action logs, resource constraints) that Monitoring has no visibility into.

---

The two escalations serve different triggers — drop diagnosis is page/keyword-specific and can run off a single Sharp Change loser, while the periodic report escalation is threshold-based and cadence-aware. Keep them separate so the agent doesn't conflate them.
