---
name: preliminary-technical-seo-audit
description: Lightweight technical SEO audit scoped to homepage inspection with mobile CWV. Checks HTTP status, indexability, canonical, robots.txt, schema, redirects, rendering, sitemaps, hreflang.
---

# Skill: Preliminary Technical SEO Audit

## Title
Technical SEO Audit

## Description
Lightweight technical SEO audit scoped to homepage inspection with mobile CWV. Checks HTTP status, indexability, canonical, robots.txt, schema, redirects, rendering, sitemaps, hreflang.

## Core Rule
Execute checks top-down on homepage only. Run mobile CWV on homepage. Avoid multi-page crawling and site-wide DOM analysis. Focus on server response, crawl eligibility, index signals, and performance.

## Parallel Execution (MANDATORY)

Batch all independent tool calls into a single `run_multi_actions` call. For example: PageSpeed mobile + desktop, GSC coverage + Ahrefs domain overview, and robots.txt + sitemap checks can all run simultaneously. Never call `run_action` sequentially for independent lookups — that is a performance bug.

## Execution Scope

Execute checks top-down. Inspect **homepage** markup. Run **CWV on homepage only (mobile mandatory)**. Avoid multi-page crawling and site-wide DOM analysis.

## Server & Response

Confirm homepage returns 200, response headers are valid (text/html), no intermittent 4xx/5xx, protocol and host normalize to a single indexable variant (http→https, www or non-www), no mixed-content assets.

## Crawl & Discovery

Confirm homepage is not blocked by robots.txt, important pages are internally linked from navigation, no obvious orphan important URLs, important pages reachable within three logical clicks, internal links do not point to 404s or redirected URLs.

## Index Eligibility

Confirm homepage is indexable (not blocked by robots.txt, no meta or x-robots noindex), no index/noindex contradictions, internal links are not primarily pointing to noindex pages.

## Metadata Signaling (Homepage Only)

Confirm homepage canonical exists, is self-referencing, is indexable, matches preferred host/protocol, matches sitemap homepage URL.

Confirm exactly one title tag, one meta description, no empty values.

Confirm OG:title, OG:description, OG:image, OG:url exist and og:url matches canonical.

## Structured Data (Homepage Only)

Detect schema on homepage, confirm schema matches visible content, no conflicting schema types, no schema on noindex pages, no fatal syntax errors.

## 6. Duplication (Lightweight)

Confirm homepage is accessible via only one indexable variant (http/https, www/non-www, trailing slash), no uncontrolled duplicate homepage URLs.

## Redirect Integrity

Confirm homepage normalization redirects are single-hop, no redirect chains longer than two hops, redirects resolve to 200 pages, legacy homepage variants do not return 404.

## Rendering (Homepage Only)

Confirm main content exists in raw HTML (not JS-only), navigation uses crawlable `<a href>` links, no hydration failures or placeholder-only content.

## Performance / Core Web Vitals (Homepage Only)

Run PageSpeed Insights (mobile), flag failing LCP/CLS/INP, identify render-blocking CSS/JS, identify LCP element and blocking resource; do not summarize scores.

## Images (Homepage Only)

Confirm meaningful images have non-empty alt attributes, hero image has alt, hero image is not oversized for LCP.

## Mobile Parity

Confirm mobile homepage contains same primary content as desktop, no hidden headings or content, no mobile usability blockers (viewport, tap targets).

## Sitemaps

Confirm sitemap exists and is accessible, homepage included, sitemap homepage URL returns 200, matches canonical, is indexable, no noindex or blocked URLs present.

## International / Hreflang (If Applicable)

If hreflang exists, confirm reciprocal links, valid language-region codes, indexable hreflang URLs.

If site is multilingual and hreflang is missing, flag.

## Parameters & Pagination (Signal-Only)

Confirm homepage does not link to internal search URLs or uncontrolled filter/facet URLs, no parameterized homepage variants indexed.

## Ecommerce (If Applicable)

Confirm homepage does not expose crawl traps via filters, internal search pages not indexable, out-of-stock products not blindly noindexed or removed.

## Releases / Recovery (Conditional)

If traffic drop or deployment is mentioned, compare current vs historical robots.txt, canonical, meta robots, rendering, and CWV using archive snapshots and PSI history; flag regressions aligned with release timing.
