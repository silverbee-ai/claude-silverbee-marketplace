---
name: gsc-query-planning
description: Deterministic planning rules for Google Search Console search performance queries, including intent-based grouping, explicit sorting hierarchy, date safety, retention limits, and searchType constraints. Property injection handled by the executor agent.
---

> **Note:** This is a planning skill for GSC date alignment. No direct tool calls or user input needed — it is invoked by other skills.

# Skill: Google Search Console Query Planning

## Purpose
Plan Google Search Console search performance queries for clicks, impressions, CTR, and position.  
Choose summary, breakdown, trend, or filtered subset strictly by user intent.  
Enforce explicit sorting when row limits are applied.  
Respect date safety, retention limits, and searchType constraints.  
Property and searchType are injected by the executor.

---

# Intent → Planning Rules

## 0. Search Type Selection (Intent Map)

Map user intent to `searchType`:

- Default (web results, keywords, pages) → `web`
- Image search performance → `image`
- Video search performance → `video`
- News search performance → `news`
- Discover feed performance → `discover`

### searchType Constraints

- For `discover` and `news`: do not use `["query"]` dimension (omit it)
- For `discover`: `position` is not available (do not request or present it)

---

## 1. Summary (Totals)

Use when user asks for overall performance, total traffic, or general SEO health.

Plan:
- Omit `dimensions`
- Use defined time range (see Date Rules)
- Returns single aggregated row

Rule: If the user expects one total number or summary, never include dimensions.

---

## 2. Breakdown / Top Lists

Use when user asks for ranking, comparison, or segmentation.

Map intent to dimension:

- Keywords → `["query"]` (not allowed for `news` and `discover`)
- Pages → `["page"]`
- Country → `["country"]`
- Device → `["device"]`
- Time-based trend → `["date"]`

Row control:
- If user specifies X → `rowLimit = X`
- If unspecified → `rowLimit = 100`

Sorting requirement:
When `rowLimit` is applied, sorting must be explicitly defined.

### Sorting Priority (Deterministic)

1. `clicks` descending (default)
2. `impressions` descending only if user intent is visibility-focused
3. `ctr` only if explicitly requested
4. `position` only if explicitly requested (not available for `discover`)

If intent is unclear → always sort by `clicks` descending.

Rule: Never apply `rowLimit` without explicit sorting.

---

## 3. Trend

Use when user asks for performance over time.

Plan:
- Use `["date"]`
- Apply defined time range

When grouping by `["date"]`, results are naturally chronological.  
Do not apply performance-based sorting.

---

## 4. Filtered Subset

Triggered when user restricts scope (blog, mobile, USA, brand, specific page).

Step 1: Apply filter.  
Step 2: Determine grouping strictly by intent:

- Wants total → filter + no dimensions  
- Wants breakdown → filter + relevant dimension  
- Wants trend → filter + `["date"]`

If `rowLimit` is applied → sorting rules apply.

Rule: Filters narrow scope. Intent determines grouping.

### 5. Brand Filtering (Optional)
Triggered when the user or the calling skill requires branded or non-branded query analysis.
Brand filtering must be applied in the initial GSC query plan, not during later analysis.
Use dimensionFilterGroups on the query dimension.
The planner does not define brand terms.
Brand terms and variants must be provided by the executor or calling skill.

Selection Rule
- Choose the filtering mode based on the requested dataset scope:
- Use Mode A when the goal is a strictly non-branded dataset.

Use Mode B when the goal is to remove pure brand queries but keep brand + modifier queries for analysis.
If the user or calling skill requires keeping brand + modifier queries, always use Mode B.

Mode A — Exclude All Branded Queries
Exclude queries containing the brand name or its variants.
Purpose: retrieve a non-branded dataset directly from GSC.
Rule: do not retrieve branded queries first and filter them later.
Implementation guidance:

Use notContains or excludingRegex on the query dimension.

Mode B — Exclude Exact Brand Queries but Keep Brand + Modifier Queries
Exclude only queries that exactly match a brand term or exact brand variant.
Keep queries where a brand term appears together with additional terms.
Examples:
Exclude

- brand
- brand name
Keep

- brand product
- brand review
- brand category

Purpose: preserve brand + modifier queries required for analysis (e.g., cannibalization).

Implementation guidance:
Use notEquals for exact brand terms when possible.
Use excludingRegex when multiple exact brand variants must be excluded.


Planner Rule
- The planner must determine the filtering mode before the first GSC search performance query is planned. If Mode B is required, the planner must not apply a broad brand exclusion that removes all queries containing the brand.
- The executor is responsible for determining the brand terms and variants used for filtering. It may use terms provided by the calling skill or derive them from available user, brand, site, or query context. The planner must decide the filtering mode, but must not define the brand terms itself.

---

# Date Rules

## Default Range
If user does not specify a time range → default to last 30 days (date-safe adjusted).

## Relative Ranges ("Last X Days")
- `endDate = today - 2`
- `startDate = endDate - (X - 1)`
- Never use today or yesterday

## Explicit Dates
- Use exactly as provided
- Format: `YYYY-MM-DD`
- Timezone: Pacific Time

## Retention Limit
- Maximum 16 months
- Do not plan queries beyond retention window

## GSC Freshness Alignment
When a workflow includes Google Search Console, align the date ranges of all other tools to GSC’s freshness limit. GSC data is reliable only up to X-2 days from today, so the effective end date for all tools must be X-2, even if other tools support fresher data. Example: if the user requests the last 7 days, use X-9 → X-2 across all tools.

---

# Property Handling
- Planner never resolves or fetches properties
- Executor injects authenticated `siteUrl`
- Planner specifies property only if user explicitly names or compares properties

---

# Endpoint Boundary
If user intent concerns indexing, coverage, crawl status, canonical issues, or inspection:
- Do not use search performance query
- Use URL Inspection tool instead

---

# Hard Constraints
- `endDate ≤ today - 2`
- Omit dimensions for summaries
- Always define sorting when `rowLimit` is applied
- Default `rowLimit = 100` if unspecified
- Never exceed 16 months
- `news` and `discover`: no `["query"]`
- `discover`: no `position`
