---
name: competitor-analysis
description: Site-architecture-level competitive analysis. Compares site sections, page types, and content features across the target domain and competitors. Builds a feature presence matrix, then runs per-section keyword gap analysis for each section type competitors have that the target lacks or underinvests in. Use for structural competitive audits, site section gap analysis, or "what are competitors doing that we're not" requests.
---

# Skill: Competitor Feature Gap Analysis

## Title
Competitor Feature Gap — Site Architecture Comparison

## Description
Compares the target domain's site structure against competitors to identify missing or underbuilt site sections. Produces a feature matrix, then runs keyword analysis per section type to quantify the traffic opportunity behind each structural gap.

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
      "question": "What competitor domain(s) should I compare against? (up to 5)",
      "header": "Competitors",
      "options": [],
      "multiSelect": false
    },
    {
      "question": "What should I focus the analysis on?",
      "header": "Focus Area",
      "options": [
        { "label": "Full site architecture", "description": "All section types across both sites" },
        { "label": "Content gaps only", "description": "Blog, guides, resources" },
        { "label": "Product/service pages", "description": "Commercial sections" },
        { "label": "Landing pages & use cases", "description": "Conversion-focused pages" }
      ],
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

**Required:** target domain, validated competitor domains (up to 5).
**Optional:** specific section types to focus on, priority keywords or topics.

Competitors must be validated as direct industry competitors before this skill runs. If called from the parent gap analysis skill, competitor validation (Section 2 of that skill) has already been completed. If called standalone, validate competitors: same vertical, same audience, competing for the same search intent. Discard aggregators, directories, or platforms.

---

## 2) Site Context

Obtain the target domain's site context — from account data, site profile, or homepage extraction. Establish core offering, primary content verticals, and business category. This determines which competitor sections are relevant comparisons vs. irrelevant to the target's business model.

---

## 3) Site Section Inventory

For the target domain and each competitor, extract the site's navigation structure and content architecture. Identify all major section types present.

Common section types (not exhaustive — include any section found):
- Products / Services
- Blog / Resources / Guides
- Case Studies / Portfolio / Success Stories
- Pricing
- Tools / Calculators
- FAQ / Help Center
- About / Team / Careers
- Glossary / Knowledge Base
- Comparison / Alternative pages
- Landing pages by use case, vertical, or audience segment

Record the section URL(s) for each domain where found.

---

## 4) Feature Presence Matrix

Build a matrix: rows = all section types discovered across all domains, columns = target domain (first) then each competitor.

Per cell: present (with URL) or absent. This is a structural inventory — no keyword data yet.

Report matrix to user before proceeding. This is the deliverable that answers "what do competitors have that we don't" at the architecture level.

---

## 5) Per-Section Keyword Gap

For each section type where at least one competitor has content and the target either lacks it entirely or has a significantly thinner version:

1. Pull the top non-branded keywords (by organic traffic) that competitor URLs in that section rank for. Use Ahrefs top pages filtered to the section's URL path.
2. Check whether the target domain ranks for any of those keywords — and if so, with which URL and at what position.
3. Calculate total search volume opportunity the section captures for competitors.

**This is one workflow applied per section type** — not a separate process for each. The section type determines the URL filter; the extraction and comparison logic is identical.

For section types where the target also has content (but thinner), compare keyword coverage breadth: how many of the section's keywords does the target cover vs. competitors?

**Output per section:** keyword table with volume, competitor rankings, target ranking (if any), total gap opportunity.

---

## 6) GSC Cross-Reference (target domain only)

When GSC is available, pull impressions, clicks, and CTR for queries the target does rank for within each section. This surfaces:
- Sections where the target has latent demand (high impressions, low clicks) that better content could convert.
- Queries where the target ranks but underperforms competitors in the same section.

If GSC is unavailable, skip and note the gap.

---

## 7) Output

**Feature Matrix** — the structural inventory from Section 4.

**Per-Section Gap Tables** — one table per section type with keyword gaps, volumes, rankings, and GSC metrics where available.

**Opportunity Summary** — each missing or underbuilt section ranked by:
1. Total search volume opportunity from competitor keyword data
2. Number of competitors with the section (higher overlap = more validated demand)
3. Estimated build effort (new section vs. expansion of existing thin section)


**Recommendations** — which sections to build or expand, ordered by traffic opportunity. Each recommendation must reference the specific keyword data and competitor evidence behind it. All URLs must appear as full clickable URLs

---

## 8) Guardrails

- Never compare against unvalidated competitors. Aggregators and directories are not benchmarks
- Never recommend building a section without keyword evidence. The matrix shows what's missing; the per-section keyword gap determines whether it's worth building
- Section types must be discovered from actual site structures — not assumed from a template list. The common types in Section 3 are starting points, not a fixed checklist
- Per-section keyword extraction uses the same workflow for every section type. Do not create unique processes per section
- Do not recommend sections that are irrelevant to the target's business model. A B2B SaaS company does not need a recipe section just because a competitor has one
- Every opportunity must be quantified. Unquantified structural gaps are observations, not recommendations
- Report the feature matrix before running keyword analysis. The user may want to scope which sections to analyze rather than running all

---

## Step Count: 7

| # | Step | Duration Estimate |
|---|------|-------------------|
| 1 | Domain resolution | 2s |
| 2 | Competitor identification | 3–5s |
| 3 | Site structure comparison | 5–8s |
| 4 | Keyword gap analysis | 5–10s |
| 5 | Backlink comparison | 3–5s |
| 6 | Content feature matrix | 3–5s |
| 7 | Output generation | 3–5s |

## Step Criticality

| Step | Critical | Fallback |
|------|----------|----------|
| Domain resolution | Yes | Cannot proceed |
| Competitor identification | Yes | Cannot proceed |
| Site structure comparison | No | Skip structure section, note in output |
| Keyword gap analysis | No | Show partial data, note gaps |
| Backlink comparison | No | Skip backlinks section, note in output |
| Content feature matrix | No | Show available data only |

## Output Format

When all data collection and analysis is complete, call `read_skill("seo-output-formatter")` and follow its instructions to format and present the full deliverable.
