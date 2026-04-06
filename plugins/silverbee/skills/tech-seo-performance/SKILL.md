---
name: tech-seo-performance
description: Technical SEO performance audit. Use whenever the user mentions slow pages, Core Web Vitals, LCP, CLS, INP, PageSpeed, images, lazy loading, fonts, mobile-first indexing, or any speed/rendering issue — even without explicitly requesting a full audit. Covers CWV field vs. lab data, TTFB, payload, third-party scripts, image optimization, font loading, caching, resource hints, and mobile parity.
---

# Tech SEO — Performance

**Input:** Target URL. Domain → analyze homepage.
**Scope:** Run all sections by default. For scoped requests, run relevant sections only and note what was skipped.
**Output:** Per section: findings table + 2–3 sentence interpretation. Close with **Summary**: all P1s + single highest-impact quick win.
**Guardrail:** Where PSI provides no remediation, report the problem and evidence, do not invent fixes. Recommended Action must be directly supported by a PSI diagnostic or explicit resource evidence.

---

## Parallel Execution (MANDATORY)

When auditing multiple URLs, batch all PageSpeed Insights calls into a single `run_multi_actions` call — one action per URL. When fetching both GSC and Ahrefs data for the same domain, batch those in a single `run_multi_actions` call. Never call `run_action` sequentially for independent lookups — that is a performance bug.

---

## 1. Core Web Vitals

**Field data (CrUX) = real-user data = Google's ranking input. Lab data (Lighthouse) = diagnostic only.** Prioritize field data for all priority decisions. If absent, note Google falls back to origin-level or no data.

Run PSI for **mobile** (required) and desktop. Identify the LCP element (type, URL, loading mechanism) and note affected resources per diagnostic.

| Metric | Field Data | Lab Data | PSI Diagnostics to Match | Recommended Action | Priority |
|---|---|---|---|---|---|
| LCP | | | "Largest Contentful Paint element", "Preload largest contentful paint image", "Eliminate render-blocking resources" | | |
| CLS | | | "Avoid large layout shifts", "Image elements do not have explicit width and height" | | |
| INP | | | "Avoid long main-thread tasks", "Reduce JavaScript execution time", "Minimize third-party usage" | | |
| TTFB | | | "Initial server response time", "Avoid multiple page redirects" | | |

> INP findings pointing to JS execution or CSR issues → refer to **tech-seo-rendering**.
> TTFB findings pointing to redirect chains → refer to **tech-seo-redirects**.

---

## 2. Payload & Third-Party Scripts

From PSI network data extract: total weight, request count, largest resources, third-party origins + their TBT contribution.

Flag: weight > 2–3MB · requests > 100 · third-party scripts blocking render or inflating TBT · missing caching ("Serve static assets with efficient cache policy") · missing compression ("Enable text compression") · missing `preconnect`/`dns-prefetch` on critical third-party origins · missing `preload` on LCP resource.

| Resource / Origin | Size / TBT Impact | Issue | Recommended Action | Priority |
|---|---|---|---|---|
If network requests show redirect chains affecting critical resources or TTFB, read_skill:("tech-seo-redirects").
If resource loading or scripts appear to block crawlable links or navigation discovery, read_skill:("tech-seo-crawl").
---

## 3. Images

Scrape page. Collect image URLs and alt text.

Identify **LCP image** (from PSI) and **up to 5 above-the-fold images**. If running this section only, run PSI first to identify the LCP element. Evaluate all of these:

| Check | Pass Condition |
|---|---|
| Alt text | Present, accurate, ≤125 chars, naturally keyword-relevant |
| Format | WebP or AVIF; flag JPEG/PNG without modern format |
| Responsive delivery | `srcset` present |
| Lazy loading | LCP/hero images must NOT have `loading="lazy"` |
| Fetch priority | LCP image must have `fetchpriority="high"` |
| Size efficiency | Flag if PSI signals significant oversizing |

All other images: flag format and missing alt text only. Do not keyword-stuff alt suggestions.

| Image | Issue | Evidence | Recommended Action | Priority |
|---|---|---|---|---|

---

## 4. Font Loading

From page source `<link>` tags and PSI network data, identify all web font files (URL, format, loading method).

Flag: missing `font-display: swap` · render-blocking font requests · files > ~50KB · more than 4–5 variants · missing `preconnect` to font CDN origin.

| Font File | Issue | Impact | Recommended Action | Priority |
|---|---|---|---|---|

---

## 5. Mobile Parity

Google indexes from the mobile version — use mobile PSI + mobile-rendered source.

| Check | Pass Condition |
|---|---|
| Content parity | Headings, body content, structured data present on mobile |
| Viewport | `<meta name="viewport">` correctly set |
| Tap targets | Interactive elements adequately sized and spaced |
| Font readability | Base font ≥ 16px |
| Navigation | Mobile nav crawlable (not JS-gated) |

| Issue | Evidence | Recommended Action | Priority |
|---|---|---|---|
If primary content or navigation is missing in the rendered mobile DOM, read_skill ("tech-seo-rendering") for deeper analysis.
If important content or structured data is missing on mobile, read_skill:("tech-seo-indexation").
