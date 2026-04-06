---
name: seo-gap-analysis
description: Competitive SEO gap analysis. Identifies keyword coverage gaps, ranking position gaps, content gaps, and SERP feature gaps between a domain and its competitors. Dispatches to specialized skills for backlink, schema, indexation, performance, internal linking, AI visibility, and site-feature gap analyses. Use for any competitor comparison, content gap, keyword gap, or competitive audit request.
---

# Skill: SEO Gap Analysis

## Title
SEO Competitive Gap Analysis

## Description
Identifies where competitors outperform the target domain and why. Runs four core analyses (keyword/topic coverage, ranking position, content, SERP features) and dispatches to specialized skills for technical, structural, and authority gaps. Every finding tied to traffic opportunity — no gaps reported without quantified impact.

---

## Before running anything (mandatory)

Do not call any tools until you have collected required inputs.

Use `AskUserQuestion` to gather inputs in a **single call**:
```json
{
  "questions": [
    {
      "question": "What is your domain?",
      "header": "Your Domain",
      "options": [],
      "multiSelect": false
    },
    {
      "question": "What competitor domain(s) should I compare against? (leave blank to auto-identify)",
      "header": "Competitor(s)",
      "options": [],
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
**Optional:** competitor domains (up to 5), target market/country, specific gap types to focus on, priority pages or sections.

If competitors are not provided, identify them in Section 2 before proceeding.

---

## 2) Competitor Identification

**Skip if the user provided competitor domains.**

Use Ahrefs organic competitors for the target domain. Select the top 5 by keyword overlap relevance — not by domain size. Validate each: competitors must operate in the same vertical, target the same audience, and compete for the same search intent. Discard aggregators, directories, or platforms that rank broadly but are not true competitors.

If the user provided competitors, validate them using the same criteria. Flag any that are not direct competitors and explain why — proceed only with validated domains.

Report validated competitor list to user before proceeding.

---

## 3) Keyword / Topic Coverage Gap

The anchor analysis — all subsequent sections build on this data.

Use Ahrefs content gap (or equivalent keyword intersection data) to identify queries where one or more competitors rank in the top results but the target domain does not rank at all.

**Keyword-level output:**
- Queries competitors rank for that the target does not.
- Search volume per query.
- Number of competitors ranking per query (overlap density — higher overlap = more validated opportunity).
- Dominant intent per query (informational / commercial / transactional).

**Topic-level rollup:**
- Cluster the keyword-level gaps into topic groups using shared semantic themes.
- For each topic cluster: total volume opportunity, number of missing keywords, whether the target has any existing content that could be expanded vs. needs entirely new pages.
- Identify topics where multiple competitors have dedicated content hubs and the target has nothing — these are authority gaps, not just keyword gaps.

**Output:** keyword gap table + topic cluster summary with estimated traffic opportunity per cluster.

---

## 4) Ranking Position Gap

Covers shared keywords where both the target and competitors rank, but competitors consistently rank higher.

Pull ranking positions for shared keywords from Ahrefs (or GSC for the target domain's side). For each keyword:
- Target domain position vs. best competitor position.
- Position delta and estimated click-share difference based on CTR curves.
- Volume-weighted traffic opportunity (what the target would gain by closing the position gap).

**Prioritize by actionable opportunity:**
- Keywords where the target ranks positions 4–20 and a competitor ranks top 3 — these are within striking distance.
- Keywords where the target ranks page 2+ with high volume — these require more effort but higher payoff.

**Root-cause signals per keyword group** (do not fabricate — flag only when data supports it):
- Content depth difference (competitor page covers more subtopics).
- Authority difference (competitor has stronger backlink profile for this page).
- SERP feature capture (competitor holds a featured snippet or other element the target does not).
- Freshness difference (competitor content is more recently updated).

**Output:** position gap table sorted by traffic opportunity, grouped by root-cause signal where identifiable.

---

## 5) Content Gap

Compares what exists on competitor sites vs. the target at the page level — not just which keywords rank, but what content assets competitors have built.

### 5.1 Page inventory comparison
Identify content types competitors publish that the target does not have:
- Missing page categories (guides, comparisons, calculators, glossaries, case studies, landing pages by use case, etc.).
- Missing content depth — pages where competitors cover subtopics the target's equivalent page does not address.

Use Ahrefs top pages per competitor filtered to organic traffic, cross-referenced against the target's existing page inventory.

### 5.2 Content quality signals
For pages competing on the same queries, evaluate where competitor pages are stronger:
- **Depth:** competitor page covers more sections, subtopics, or supporting data.
- **Freshness:** competitor page updated more recently and freshness appears to contribute to ranking advantage.
- **Rich media:** competitor page includes images, videos, diagrams, or interactive elements that the target page lacks.

These are evaluation criteria within the content gap — not standalone analyses. Flag only when the quality difference is visible and likely contributes to the ranking delta from Section 4.

**Output:** missing content types with traffic opportunity, page-level depth/freshness/media gaps for top competing pages.

---

## 6) SERP Feature Gap

For the top shared keywords (from Sections 3 and 4), analyze which SERP features appear and who owns them.

**Features to check:** featured snippets, People Also Ask, FAQ rich results, video carousels, image packs, knowledge panels, local packs, shopping results, AI Overviews.

For each feature:
- Does a competitor own it? Which one?
- Does the target domain have the structural prerequisites to compete for it (schema markup, content format, video assets, etc.)?
- What specific changes would the target need to become eligible?

**Output:** SERP feature ownership table per keyword, prerequisite gaps, actionable changes.

---

## 7) Specialized Gap Dispatch

These gap types require full skill-level analysis. Run only when relevant to the user's request or when findings from Sections 3–6 indicate the gap is a contributing factor.

| Gap Type | Trigger | Skill |
|---|---|---|
| **Backlink / Authority Gap** | Position gap exists without content or SERP feature explanation; competitors have stronger link profiles for competing pages. | `read_skill("link-building-outreach")` — run with competitor comparison scope. |
| **Structured Data Gap** | SERP feature gap shows competitors winning rich results the target is not eligible for; schema differences identified. | `read_skill("tech-seo-schema")` — run with competitor schema comparison. |
| **Indexation Gap** | Competitors expose significantly more pages to search engines; target has thin index relative to content. | `read_skill("tech-seo-indexation")` — run with competitor index size comparison. |
| **Technical Performance Gap** | Core Web Vitals or rendering differences identified as potential ranking factor in position gaps. | `read_skill("tech-seo-performance")` — run with competitor benchmarking. |
| **Internal Linking Gap** | Key pages on target receive weak internal link support compared to equivalent competitor pages. | `read_skill("tech-seo-crawl")` — run with competitor internal link analysis. |
| **AI Visibility Gap** | Competitors appear in LLM responses or AI Overviews for target queries; target domain does not. | `read_skill("ai-visibility")` — run with competitor benchmarking. |
| **Competitor Feature Gap** | User requests site-architecture-level comparison or full competitive audit; determines which site sections/features competitors have that the target lacks. | `read_skill("competitor-feature-gap")` — full site-section inventory and per-section keyword comparison. |

Do not run all dispatched skills by default. Run them when:
- The user explicitly requests a full audit.
- Findings from Sections 3–6 point to a specific gap type as a contributing cause.
- The user asks about a specific gap type directly.

---

## 8) Output

**Executive Summary:** overall competitive position (leading / competitive / trailing / significant gaps), top 3 highest-impact opportunities by estimated traffic, primary gap types identified.

**Section-by-section findings** from Sections 3–7, each with specific gaps and quantified opportunity.

**Priority action list** ordered by traffic impact:
1. **Quick wins** — ranking position gaps where the target is within striking distance (positions 4–20 vs. competitor top 3). Highest ROI for least effort.
2. **Content builds** — missing content types or topic clusters with validated demand and multiple competitors ranking.
3. **Structural fixes** — SERP feature eligibility, schema implementation, internal linking reinforcement.
4. **Authority investment** — backlink gaps requiring outreach or content-led link acquisition.
5. **New capabilities** — site features or tools competitors offer that the target lacks entirely.

Every recommendation must reference the specific gap finding and estimated traffic opportunity that justifies it.
All URLs must appear as full clickable URLs including https:// (no relative paths or truncated domains).

---

## 9) Guardrails

- Never report a gap without quantifying its traffic impact. Unquantified gaps are not actionable
- Never fabricate root-cause attribution. If the data does not explain why a competitor outranks the target, say so
- Never treat domain authority alone as an explanation. "They have more backlinks" is not a root cause — specify which pages, which keywords, and whether the link profile difference is actually the differentiator
- Competitor validation is mandatory. Do not compare against non-competitors — aggregators, directories, and platforms that rank broadly are not competitive benchmarks
- Topic clusters must be derived from keyword data, not invented. Clusters must share semantic overlap in the actual keyword set
- SERP feature gaps must check structural prerequisites before recommending pursuit. Do not recommend targeting featured snippets if the content format cannot support them
- Dispatched skills run only when triggered — not by default. A gap analysis is not a full site audit unless the user requests one
- Every recommendation must trace to a specific finding. No generic competitive advice
- Report findings progressively after each section. Do not batch
- All URLs must appear as full clickable URLs including https:// (no relative paths or truncated domains)

---

## Output Format

When all data collection and analysis is complete, call `read_skill("seo-output-formatter")` and follow its instructions to format and present the full deliverable.
