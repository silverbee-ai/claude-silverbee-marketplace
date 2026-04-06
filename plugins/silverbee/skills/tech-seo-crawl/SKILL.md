---
name: tech-seo-crawl
description: Technical SEO crawl and discovery efficiency audit. Covers site hygiene, crawl depth, orphan pages, internal link graph, crawl traps, and internal linking strategy. Use when investigating crawl issues, orphaned pages, link equity distribution, or baseline technical hygiene.
---

# Skill: Tech SEO — Crawl & Discovery

## Parallel Execution (MANDATORY)

Batch all independent tool calls into a single `run_multi_actions` call. When checking multiple URLs, fetching GSC + Ahrefs data, or querying multiple pages simultaneously, send all calls at once. Never call `run_action` sequentially for independent lookups — that is a performance bug.

---


## 1) Hygiene Baseline

**Checks:**
- Protocol/domain consistency: http→https, www↔non-www, trailing slash policy. All must normalize to a single indexable variant.
- Status codes: 200/3xx/4xx/5xx distribution on key URLs.
- Header sanity: content-type (text/html), cache-control presence, vary headers where relevant.
- Canonical tag presence and basic validity (deep canonical analysis in `read_skill("tech-seo-indexation")`).
- Meta robots presence and conflicts (deep analysis in `read_skill("tech-seo-indexation")`).
- Duplicate title/description patterns caused by templates (deep analysis in `read_skill("tech-seo-indexation")`).

**Output:** Site Hygiene Summary table:

| Area | Finding | Example URLs | SEO Impact | Priority | Fix |

**Guardrail:** Do not recommend architectural changes if a narrow hygiene fix solves it.

---

## 2) Crawl Depth & Discovery

**Checks:**
- Crawl depth: flag pages deeper than 3 clicks from homepage or primary hubs.
- Orphans: URLs present in sitemap or known lists but with zero internal links.
- Internal link graph: hubs, dead-ends, broken internal links (4xx).
- Redirect waste: internal links pointing to redirected URLs (should point to final destination).
- Crawl traps: infinite URL generation from parameters, pagination, calendars, internal search.
- Duplicate discovery paths: multiple URL variants for same content being linked internally.

**Failure conditions:**
- Depth >3 for high-value pages.
- Orphaned valuable pages (have traffic/impressions in GSC but no internal links).
- Material internal links to redirects or 404s.
- Parameter/pagination generating uncontrolled URL count.

**Output tables:**

Crawl depth: URL | Depth | Primary Path | Fix

Orphan list: URL | How Discovered | Suggested Linking Source | Priority

Wasted crawl: Redirected/404 Internal Links | Source Page | Target | Fix

**Fix patterns:**
- Add links from nearest relevant hub pages (category → subcategory → product).
- Replace internal links to redirect targets with final destination URLs.
- Block or canonicalize crawl trap patterns (details in `read_skill("tech-seo-redirects")`).

**Guardrail:** Do not increase internal linking to pages that are not index-eligible or are intentionally excluded.

---

## 3) Internal Linking Strategy

Triggered when linking recommendations are requested or when crawl depth/orphan issues are detected.

**Output format:**

| Source Page | Target Page | Anchor Text | Context Sentence |

**Rules:**
- Anchors must be natural and contextual, not forced exact-match.
- Prefer non-branded over branded anchors.
- Avoid repetitive anchor patterns across many links.
- Respect hierarchy: important pages receive more internal links.
- Do not link to non-indexable pages unless there is a UX reason.
