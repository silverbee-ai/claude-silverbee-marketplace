---
name: seo-cannibalization-diagnosis
description: Diagnoses keyword cannibalization risk — identifies whether multiple URLs
  are competing for the same query in a way that creates measurable ranking or traffic loss. Use when user asks for "a cannibalization report", "which URL should be primary",
  "why are my rankings unstable", "should I merge these pages", "can I create a new page
  for this keyword", or mentions "two pages ranking for the same query" or "anchor text
  conflict". 
---

# Skill: Keyword Cannibalization Diagnosis

---

## Core Definitions

**Keyword cannibalization** — two or more URLs competing for the same query with the same search intent, resulting in measurable ranking instability or traffic dilution.

**SERP dominance**
Multiple URLs from the same domain appear in the SERP for the same query. This reflects normal domain coverage in search results and **must not be classified as cannibalization**.

**Stable dominance**
One URL consistently leads performance for the query across the analysis window — typically holding the top position in most weeks and capturing the majority of clicks (≥60%). **This indicates a clear primary page and must not be classified as cannibalization**.

**All three conditions must be present to classify as cannibalization:**
- Multiple meaningful competing URLs — defined as URLs with ≥10% of total impressions for that query, minimum 50 impressions in the analysis window, ranking in top 20, Click share ≥5% of total query clicks AND at least 3 clicks in the analysis window
- Overlapping search intent
- Ranking instability or traffic dilution — instability means either ranking swaps (position leader changes in ≥30% of weeks) or ranking ceiling (all competing URLs consistently outside top 10 with week-to-week fluctuation)

**Never classify as cannibalization if:**
- One URL clearly leads on click share (≥60% or above) and holds top position in most weeks — this is stable dominance
- Competing URLs serve different search intents — this is intent separation and normal SERP coverage
- Indented results (one URL nested under the primary in SERP) — positive topical authority signal
- Pure navigational brand queries — excluded before analysis begins

**Expected outcome**
Cannibalization is not universal. If the data and analysis shows stable dominance, intent separation, or no qualifying conflicts, conclude **No cannibalization risk detected**.

---

## 1) Input & Pre-Processing

**Required:** target queries or keyword clusters; client brand name and variants. If brand name is missing, ask before proceeding. Do not proceed without it.  
**Optional:** specific URLs, date range.

**Brand filter (run first):**  
Classify each query:
- **Pure navigational brand query** — brand name alone or typo variant, with no modifier that adds topical or intent specificity → exclude from analysis and stop processing for this query.
- **Brand + modifier query** — brand name combined with any term that adds topical, intent, or audience specificity → include in analysis.

If all queries are pure navigational brand queries, inform user and stop. If brand name overlaps a generic term, assess from query context; if ambiguous, treat as non-branded and note it.

**Query set preparation:**  
- If the user provides queries → analyze them directly
- If the user provides URLs → retrieve the queries generating impressions for those pages via GSC or Ahrefs
- If the user requests a general report → retrieve the site's top queries by clicks from GSC for the analysis window
- If a single query is provided → expand into close semantic variants via Ahrefs or DataForSEO, keeping only variants with the same search intent. If a variant returns a different intent, exclude it and diagnose separately

**Performance data source:** GSC (preferred) → Ahrefs → DataForSEO. State which is active. If Ahrefs or DataForSEO, note that figures are estimates.

**Scope:**
- Cannibalization diagnosis only — no keyword recommendations or content plans
- Minimum 3–6 month window; note if under 3 months
- Never diagnose from single-week data
- If no analysis window is provided, default to the last 3 months of available data

---

## 2) Conflict Detection

Run per query. Do not aggregate across the cluster before completing this section.

For each query, pull: all URLs with impressions, clicks, avg position, weekly position. If total query clicks = 0, skip click-share evaluation and rely on impression share and ranking behavior only when assessing conflict signals.

Calculate:
```
impression share = URL impressions / total impressions for that query
click share      = URL clicks / total clicks for that query
```

**Meaningful contributor** — URL qualifies if all conditions below are met:

- Impression share ≥10% of total impressions for that query
- Minimum 50 impressions in the analysis window
- Ranks in top 20
- Click share ≥5% of total query clicks AND at least 3 clicks in the analysis window

URLs that receive impressions but negligible clicks should not be treated as competing results.
Exclude URLs failing any condition. Note exclusions and their impression share.

- One qualifier → no conflict for this query. Remove from analysis and move to next query
- Multiple qualifiers → conflict signal present. If one qualifying URL meets the stable dominance condition (≥60% click share and top ranking position in most weeks), treat the pattern as stable dominance and skip Sections 3–5 for this query. If conflict signal is present read_skill("canonical-url-and-domain-validation") for all competing URLs

Record: canonical relationships, conflicts, self-canonicals, missing canonicals. If skill unavailable, note gap and proceed.

After running per query, group queries with conflict signals by shared competing URLs for output.

---
## 3) Intent Assessment

### 3a — Intent Classification

If only a single query is being analyzed, evaluate intent overlap across the competing URLs directly. Otherwise, run intent classification per query — including each variant in the cluster — before grouping.

Fallback chain:
1. **Ahrefs** — keyword intent for target query
2. **LLM inference** — if Ahrefs unavailable; flag as low-confidence. Use observable page signals only: title, H1, page type, primary CTA, content structure. Never infer intent solely from query wording.

Valid types: Informational / Transactional / Commercial investigation / Navigational

If a cluster variant returns a different intent than the input query, remove it and note it as a separate diagnosis candidate.

### 3b — Internal Anchor Text Audit (Ahrefs)

Pull all internal links to each competing URL. Check for:
- **Exact-match conflict:** target query (or variant) used as anchor pointing to a non-primary URL
- **Split signals:** same anchor text pointing to different competing URLs

Report all URLs involved — not just the primary. Each URL receiving the conflicting anchor text must be listed with the anchor text and source page.

Conflict found → flag as a contributing signal. Include in recommended actions only if the query is classified as Potential Risk or Confirmed Risk.

Ahrefs unavailable → note gap. Do not attempt to infer anchor signals without data.

### 3c — Intent Overlap Decision

- Intents clearly differ → **Not Cannibalization (intent separation)**. Stop analysis for this query
- Intents overlap → proceed to **Section 4 (60% Assessment)**.

## 4) Stability Assessment

```
click share per URL = URL clicks / total clicks across competing URLs
```

Assess the overall pattern per query. Click share is the primary signal. Positional behavior is supporting context.

**Read the pattern:**

- One URL captures ≥60% or more of clicks and holds top position in most weeks → **Stable dominance (Not Cannibalization)**. Stop cannibalization analysis for this query. Minor fluctuations do not override a clear click-share leader.
- Click share is split with no clear leader, OR position leader changes in ≥30% of weeks → **unstable**
- One URL leads on clicks but margin is narrow and position swaps are frequent → **grey zone** — do not classify. Report the pattern, recommend monitoring for 60 days before acting. No SEO action should be taken on grey zone findings.

This rule overrides impression overlap, ranking comparisons, and internal linking signals.
State the classification and the specific evidence that drove it.

---

## 5) Risk Classification

| Classification | Required Evidence |
|---|---|
| **Not Cannibalization** | Pure navigational brand query, OR clear intent separation, OR SERP dominance (multiple URLs from the same domain appear for the query in the SERP), OR stable dominance (one URL at ≥60% click share holding top position in most weeks) |
| **Potential Risk** | Overlapping intent + unstable pattern (click share split, or position leader changes in ≥30% of weeks) |
| **Confirmed Risk** | Potential Risk criteria + clear traffic fragmentation: no URL consistently dominates click share, AND multiple URLs each meet the meaningful contributor thresholds (≥10% impression share, ≥50 impressions, top-20 ranking, ≥5% click share and at least 3 clicks), AND ranking leadership changes across weeks |

**Confidence modifiers (any apply → Low):**
- Performance data from Ahrefs or DataForSEO (estimates only — does not affect confidence in intent data)
- Mixed intent signals during intent assessment
- Intent determined via LLM inference (Ahrefs unavailable)

Never classify by URL count alone. Never upgrade to Confirmed without clear fragmentation evidence across all three conditions.

---

## 6) Primary URL Decision

Run only if section 5 returns Potential or Confirmed risk, or user explicitly requested a primary URL decision.

Select primary URL by criteria in priority order. If criteria conflict, state the conflict and ask the user. Skip any criterion where data is unavailable — note the gap and proceed to the next.

1. **Intent match** — best satisfies intent Google is serving
2. **Conversion rate** — higher CVR wins (GA4 or CRO tool); state figures. Skip if unavailable
3. **Engaged Sessions** — GA4 tiebreaker when CVR unavailable or close; state figures. Skip if unavailable
4. **Historical clicks** — more clicks over the window
5. **Average position** — stronger avg ranking
6. **Backlink profile** — stronger referring domain authority (Ahrefs); skip if unavailable
7. **Strategic business value** — ask user if unclear

**Non-primary URL assignments:**
- **Consolidation candidate** — overlapping topic and intent; merge into primary and redirect
- **Redirect candidate** — duplicates primary with minimal unique value; redirect. read_skill("tech-seo-redirects")
- **Intent differentiation candidate** — could serve a clearly distinct intent (must be supported by the detected intent signals)
- **Supporting content** — only if demonstrably serves a different funnel stage or audience angle AND cannot fit above categories. Justify explicitly; not a default

---

## 7) Output

Report only keywords classified as **Potential Risk** or **Confirmed Risk**.

If no keywords meet these conditions, explicitly state: **No cannibalization risk detected based on the available data.**

Exclude from the report:
- Not Cannibalization
- SERP Dominance
- Stable Dominance
- Pure navigational brand queries

Sort findings from **strongest cannibalization evidence to weakest**.

---

### Cannibalization Findings

**| Keyword | Search Volume | Total Query Clicks | Classification | Confidence | Primary URL | Recommended Action |**
|---|---|---|---|---|---|---|

- **Keyword** — analyzed query
- **Search Volume** — monthly search volume from Ahrefs or DataForSEO (mark N/A if unavailable)
- **Total Query Clicks** — total clicks the analyzed domain received from this keyword across all ranking URLs within the analysis window (from GSC or Ahrefs).
- **Classification** — Potential Risk or Confirmed Risk
- **Confidence** — High / Medium / Low
- **Primary URL** — page that should own the keyword
- **Recommended Action** — consolidation, redirect, intent differentiation, monitoring

---

### Evidence (per keyword)

**Keyword:** [query]  
**Search Volume:** [value]

**Data source:** [GSC / Ahrefs]  
**Analysis window:** [date range]

| URL | Avg Position | Intent | Stability | Clicks | Impression Share | Click Share |
|---|---|---|---|---|---|---|

All URLs must appear as **fully clickable URLs**.

**Intent overlap:** [Yes / No] — short rationale  

**Stability pattern:**  
[Stable / Unstable / Grey zone] with supporting metrics

**Anchor text conflicts:**  
[Conflict / None / Not analyzed]

**Primary URL decision:**  
Explain briefly why the selected URL should own the keyword

**Recommended actions for other URLs:**

- [URL] — consolidation / redirect / differentiation / monitor

**Evidence summary:**  
2–3 concise sentences linking the data to the classification.
---

## Dashboard Template

Use `render_template("competitor-analysis", data)` via the silverbee-mcp MCP.

This template is repurposed for cannibalization diagnosis. Field mapping:

| Field | Type | Maps to |
|---|---|---|
| `title` | string | Dashboard heading |
| `metrics.trafficGap` | string | Cannibalized Queries (count) |
| `metrics.keywordGap` | string | Affected URLs (count) |
| `metrics.drDelta` | string | Traffic at Risk (estimate) |
| `metrics.topOpportunity` | string | Primary Action (recommendation) |
| `chart.data[]` | `{cluster: string, competitor: number, you: number}` | Per-cluster click share comparison between competing URLs |
| `gapKeywords.rows` | string[][] | Cannibalized query detail rows |
| `topPages.rows` | string[][] | Affected URL detail rows |

All metric values are **strings** (not numbers). Table `rows` are `string[][]` (arrays of string arrays, not objects).

> **Note:** The `competitor-analysis` template is the closest layout match for cannibalization output. The gap/competitor fields are repurposed as described above. When populating `chart.data`, use `competitor` for the non-primary URL's click share and `you` for the primary URL's click share.

For custom specs or troubleshooting, load the `show-generative-ui` skill.

---

## 8) Guardrails

1. Minimum 3-month window. State window used
2. Never infer intent from query wording alone — use observable page signals
3. Run intent classification per query before cluster grouping. Exclude variants with different intent
4. Always state primary URL selection rationale and the criterion that drove it
5. Do not conflate SERP feature click absorption with cannibalization — flag as alternative explanation first and read_skill("ai-visibility")
6. Anchor text conflict → always include in recommended actions, regardless of classification
7. Do not infer anchor signals without Ahrefs data — note gap and stop
8. Grey zone → no SEO action. Monitor and re-evaluate after 60 days
9. **No Cannibalization** is a valid conclusion. If the analysis shows stable dominance, intent separation, or no qualifying conflicts, report that no cannibalization risk was detected — do not force a finding
10. Canonical or 301 redirect recommendations are out of scope — use read_skill("tech-seo-redirects") or read_skill("canonical-url-and-domain-validation")
