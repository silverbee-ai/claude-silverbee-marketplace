---
name: topical-authority-mapping
description: Maps a domain's topical authority structure. Identifies pillar topics, supporting subtopics, coverage completeness, internal linking architecture, and content priority order. Use for content strategy, topic cluster planning, authority gap identification, "what should I write about", "content architecture", "pillar content", "topic clusters", or any request about building topical authority in a subject area.
---

# Skill: Topical Authority Mapping

## Title
Topical Authority Mapping & Content Architecture

## Description
Produces a complete content architecture for a domain within a topic area. Identifies which pillar topics the site should own, maps supporting subtopics per pillar, scores coverage completeness against what exists, defines internal linking relationships, and prioritizes what to build or expand. The strategic layer between keyword research (individual keywords) and content optimization (individual pages).

---

## Before running anything (mandatory)

Do not call any tools until you have collected required inputs.

Use `AskUserQuestion` to gather inputs in a **single call**:
```json
{
  "questions": [
    {
      "question": "What domain should I map topical authority for?",
      "header": "Domain",
      "options": [],
      "multiSelect": false
    },
    {
      "question": "What topic cluster or area should I focus on? (leave blank to derive from site context)",
      "header": "Topic Cluster",
      "options": [],
      "multiSelect": false
    }
  ]
}
```

After collecting inputs, confirm them in a short text message and **wait for the user's go-ahead** before making any tool calls.

---

## Tool execution

Follow the supervisor skill's tool usage rules (Steps 1–3, error handling,
result reuse). **Do not** re-call `get_instructions`, `list_available_apps`,
or `search_actions` if they already ran in this conversation — reuse the
cached results.

**MANDATORY — parallel execution:** Batch all independent queries into a
single `run_multi_actions` call. Never call `run_action` in a sequential
loop — that is a performance bug.

---

## 1) Input

**Required:** target domain.
**Optional:** specific topic area to map (if not provided, derive from site context), competitor domains, existing content inventory, priority business goals.

---

## 2) Site Context & Existing Authority Baseline

Obtain site context — from account data, site profile, or homepage extraction.

**Existing authority scan:** use GSC (preferred) or Ahrefs to identify all topic areas the domain currently ranks for. Group ranking queries into broad themes. For each theme, capture total impressions, clicks, number of ranking queries, and number of ranking URLs.

This produces a rough authority map of what the site *already* owns. Some themes will be strong (deep coverage, many ranking queries), others thin (a few incidental rankings), others absent entirely.

If the user specified a topic area, scope all subsequent sections to that area only. If not, present the full theme inventory and let the user select which areas to map in depth — mapping every topic area at once is wasteful.

Report existing authority baseline to user before proceeding.

---

## 3) Pillar Identification

For the scoped topic area, identify the core pillar topics. A pillar is a broad subtopic that warrants its own primary page and has enough search demand to anchor a content cluster around it.

**Method:**
- Pull keyword data for the topic area via Ahrefs. *For the full keyword research methodology, call `read_skill("keyword-research")` with the topic area as input.*
- From the keyword research output, use the Category groupings (Section 10 of that skill) as candidate pillars.
- Validate each candidate: does it have sufficient search demand, distinct intent from other pillars, and enough subtopic depth to build a cluster around?
- Cross-reference against competitors: use Ahrefs top pages for competitor domains filtered to the topic area. Identify pillar-level pages competitors have built. *For systematic competitor comparison, call `read_skill("seo-gap-analysis")` Section 3.*

**Output:** list of confirmed pillars with total search demand, existing page (if any), and competitor coverage status.

---

## 4) Subtopic Mapping Per Pillar

For each pillar, identify the supporting subtopics that a complete authority position requires.

**Method:**
- Use the Sub-Category groupings from keyword research as candidate subtopics within each pillar.
- Expand with Ahrefs Search Suggestions and People Also Ask data scoped to the pillar topic.
- For each subtopic: classify intent (informational / commercial / transactional), estimate search demand, and determine content type (guide, comparison, how-to, FAQ, tool, case study, landing page).

**Subtopic completeness check:** compare against competitor topic coverage. If competitors consistently cover a subtopic and the target does not, it's a coverage gap. If no competitors cover it and demand is low, it may not be worth building.

**Output per pillar:** subtopic list with intent, demand, content type, and existing page status (covered / thin / missing).

---

## 5) Coverage Scoring

Score each pillar's completeness based on the subtopic mapping.

**Per pillar:**
- Total subtopics identified.
- Subtopics with existing coverage (page exists and ranks for relevant queries).
- Subtopics with thin coverage (page exists but ranks poorly or covers the subtopic superficially).
- Subtopics entirely missing (no existing page).

**Coverage score:** percentage of subtopics with adequate coverage. This is the core diagnostic — it tells the user where their authority is strong, where it's thin, and where it's absent.

**Output:** pillar coverage matrix:

| Pillar | Total Subtopics | Covered | Thin | Missing | Coverage Score |

---

## 6) Existing Page Overlap Check

Before recommending new content, check whether existing pages already cover the same intent.

**Per subtopic marked "missing" or "thin":**
- Check whether any existing page on the domain already targets the subtopic's primary intent. Use GSC query-to-URL mapping: which URLs rank (even weakly) for the subtopic's keywords?
- If an existing page covers the intent → recommendation is "expand existing page," not "create new."
- If no existing page covers the intent → recommendation is "create new page."
- If multiple existing pages cover the same subtopic intent → flag as potential cannibalization. *For full diagnosis, call `read_skill("seo-cannibalization-diagnosis")` on the affected queries and URLs.*

This prevents the mapping from recommending new pages that would compete with existing content.

---

## 7) Internal Linking Architecture

Define how pillar and supporting pages connect.

**Structure per pillar:**
- Pillar page links to all its supporting subtopic pages.
- Each subtopic page links back to its pillar.
- Subtopic pages link laterally to closely related subtopics within the same cluster where contextually natural.
- Cross-cluster links only where genuinely relevant — do not force links between unrelated pillars.

**Output:** linking blueprint per pillar:

| Source Page | Target Page | Direction | Relationship |

This is the architectural plan. *For page-level linking implementation (anchor text, context sentences, crawl depth fixes), call `read_skill("tech-seo-crawl")` Section 3.*

---

## 8) Content Priority Matrix

Order what to build or expand by impact.

**Priority factors (in order):**
1. **Pillar pages missing or thin** — a cluster cannot build authority without its anchor page. Build pillars first.
2. **High-demand subtopics with no coverage** — largest search volume opportunity among missing content.
3. **Thin subtopics with existing pages** — expansion is faster than creation and preserves existing ranking signals.
4. **Subtopics where competitors dominate and the target has nothing** — competitive pressure makes these time-sensitive.
5. **Low-demand subtopics needed for cluster completeness** — these complete the authority signal but individually drive little traffic. Build last.

**Dependency rule:** if a supporting subtopic page requires context from its pillar page (e.g., it's a deep-dive on a concept the pillar introduces), the pillar must be built or updated first. Flag dependencies explicitly.

**Output:**

| Priority | Page | Type (Pillar/Subtopic) | Action (Create/Expand) | Demand | Dependency | Rationale |

---

## 9) Output

**Authority Baseline** — existing topic themes with strength indicators (Section 2).

**Pillar Map** — confirmed pillars with demand and competitor coverage (Section 3).

**Subtopic Maps** — per-pillar subtopic lists with intent, demand, content type, and coverage status (Section 4).

**Coverage Matrix** — pillar-level completeness scores (Section 5).

**Overlap Findings** — pages to expand vs. create, cannibalization flags (Section 6).

**Linking Blueprint** — architectural connections between pillar and supporting pages (Section 7).

**Priority Matrix** — ordered build/expand plan (Section 8).

---

## 10) Guardrails

- Pillars and subtopics must be derived from keyword data and competitor evidence, not invented. If there's no search demand or competitive precedent for a subtopic, do not include it.
- Never recommend creating a new page without checking for existing intent overlap first (Section 6). Skipping this check creates cannibalization.
- Coverage scoring must use actual ranking data, not assumptions about page quality. A page "covers" a subtopic only if it ranks for relevant queries.
- Internal linking architecture defines relationships, not implementation. Do not duplicate `tech-seo-crawl` linking methodology.
- Keyword-level data per cluster comes from `keyword-research`. Do not rebuild keyword research logic here — call the skill.
- Competitor topic coverage comes from `seo-gap-analysis`. Do not rebuild gap analysis logic here — call the skill.
- Cannibalization diagnosis on existing overlapping pages comes from `seo-cannibalization-diagnosis`. Do not rebuild diagnosis logic here — flag and dispatch.
- The priority matrix must account for dependencies. Do not recommend building a subtopic page before its pillar exists.
- Report the authority baseline and pillar map before mapping subtopics. The user may want to scope which pillars to map in depth.
- Topic authority is built over time. Do not present the full map as a single sprint — distinguish between immediate priorities and longer-term completeness.

---

## Dashboard Template

Use `render_template("topical-authority", data)` via the silverbee-mcp MCP.

| Field | Type | Description |
|---|---|---|
| `title` | string | Dashboard heading |
| `metrics.pillars` | string | Number of pillar topics identified |
| `metrics.coverageScore` | string | Overall coverage percentage |
| `metrics.missingTopics` | string | Count of missing subtopics |
| `metrics.quickWins` | string | Quick-win opportunities count |
| `chart.data[]` | `{pillar: string, coverage: number}` | Coverage score per pillar |
| `contentGap.rows` | string[][] | Content gap detail rows |
| `priorityMatrix.rows` | string[][] | Priority matrix rows |

All metric values are **strings** (not numbers). Table `rows` are `string[][]` (arrays of string arrays, not objects).

For custom specs or troubleshooting, load the `show-generative-ui` skill.

---

## Output Format

When all data collection and analysis is complete, call `read_skill("seo-output-formatter")` and follow its instructions to format and present the full deliverable.
