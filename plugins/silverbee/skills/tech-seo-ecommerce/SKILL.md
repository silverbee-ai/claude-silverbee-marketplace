---
name: tech-seo-ecommerce
description: Technical SEO ecommerce-specific audit. Covers faceted navigation, product variants, category-product linking depth, out-of-stock handling, duplicate product descriptions, internal search indexing, XML sitemap strategy, ecommerce structured data, and AI Overview exposure. Use only when the target site is an ecommerce site. Not for non-ecommerce sites.
---

# Skill: Tech SEO — Ecommerce

## Parallel Execution (MANDATORY)

Batch all independent tool calls into a single `run_multi_actions` call. When checking multiple URLs, fetching GSC + Ahrefs data, or querying multiple pages simultaneously, send all calls at once. Never call `run_action` sequentially for independent lookups — that is a performance bug.

---


**Conditional module.** Run only when the target site is ecommerce. Skip entirely for non-ecommerce sites.

## 1) Checks

- **Faceted navigation:** indexing policy must be controlled. Uncontrolled facets generate crawl traps and duplication. Reference`read_skill("tech-seo-redirects"` for parameter handling methodology.

- **Pagination:** validate crawlability and canonical behavior for category series (page 2+). Do not recommend canonicalizing paginated pages to page 1 — this blocks discovery of products that appear only on deeper pages. Do not recommend noindexing paginated pages for the same reason. `rel=next/prev` is no longer supported by Google — do not flag its absence as an issue or recommend its implementation.

- **Product variants:** evaluate canonical/URL strategy per variant pattern (color, size, etc.). For each variant cluster assess: canonical URL integrity (one canonical per cluster), internal linking exposure (are non-canonical variants being linked to directly?), sitemap inclusion (non-canonical variants should be excluded), and indexability alignment (noindex and canonical signals must not conflict). Reference read_skill("canonical-url-and-domain-validation") for target URL integrity verification.

  **Parameterized variants** (e.g. `?color=red&size=M`): treat as a crawl trap risk — all parameter combinations must canonicalize to the clean base URL. Verify GSC parameter handling is configured. Exclude all parameterized URLs from sitemaps. Do not conflate with faceted navigation — parameterized variants are product-level; faceted filters are category-level.

- **Category → product linking depth:** products should be reachable within 3 clicks from category hubs. Deep nesting wastes crawl budget and dilutes equity.

- **Out-of-stock / discontinued handling:**
  - **Out-of-stock:** recommend keeping the page live and treating it as a lobby — must clearly communicate out-of-stock status, surface similar in-stock products, and include a "notify me" feature where the platform supports it. Include restock date if available. Recommend adding `ItemAvailability: OutOfStock` in Product schema. Never recommend a 301 to the homepage.
  - **Discontinued:** recommend a redirect only when replaced by a specific successor URL. If no direct successor exists, recommend keeping the page live with similar product recommendations. Never recommend redirecting to homepage or category root as a substitute for a real replacement.

- **Duplicate product descriptions:**
  - **Internal duplication (always run):** using crawl data or Ahrefs, cluster near-identical product descriptions across the site. Flag pages with duplicated or near-duplicate copy and recommend differentiation or unique editorial framing.
  - **External duplication (run only when user explicitly requests it):** check whether descriptions match manufacturer or competitor copy. Run as a sampled batch only — select 10–15 representative products across category and traffic tiers, run exact-phrase search checks, extrapolate the pattern. Do not check every URL.

- **Internal search pages:** noindex policy mandatory. Internal search results should not compete with category pages.

- **XML sitemap strategy:** large catalogs require a sitemap index structure with separate sitemaps for products and categories. Faceted URLs must be excluded from sitemaps by default — they are crawl waste unless explicitly designated as indexable facets (i.e., long-tail SEO pages with unique optimized content, crawl budget allocated, and canonical set to self). Check that: discontinued URLs with a redirect recommendation are excluded, out-of-stock pages remain included, sitemap reflects current crawl priority, and update frequency matches catalog volatility.

- **Structured data:** Product, Offer, AggregateRating — only if matching content exists on the page. Reference read_skill("tech-seo-schema") for validation methodology.

- **AI Overview exposure:**
  - *Schema angle:* structured data quality (complete Offer attributes — price, availability, condition) directly affects eligibility for AI Overview inclusion on product queries. Flag incomplete or missing Offer attributes as an AIO risk.
  - *Traffic angle:* for high-volume product and category queries, check whether AI Overviews are present in SERPs. Where AIO is absorbing clicks, flag as an alternative explanation for traffic drops before attributing to technical issues.

## 2) Output

Ecommerce architecture findings + actionable fixes. Variant/canonical strategy recommendation per pattern.

| Pattern | URLs | Current Handling | Issue | Recommended Strategy | Fix |
|---|---|---|---|---|---|
