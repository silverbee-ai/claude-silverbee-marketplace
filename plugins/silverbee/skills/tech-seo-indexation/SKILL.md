---
name: tech-seo-indexation
description: Technical SEO indexation audit. Covers GSC index coverage status, index eligibility signals, canonical validation, soft 404 detection, index bloat, duplication, and sitemap quality. Use when investigating indexing issues, canonical conflicts, duplicate content, sitemap problems, or pages not appearing in search results.
---

# Skill: Tech SEO — Indexation

## Parallel Execution (MANDATORY)

When fetching data from multiple sources (GSC index coverage, Ahrefs backlinks, Ahrefs ranking URLs), batch all independent calls into a single `run_multi_actions` call. Never call `run_action` sequentially for independent lookups — that is a performance bug.

---

## 1) Index Coverage Status (GSC)

**Run first.** Before auditing signals (robots, meta, canonicals), check what Google has actually done.

Pull GSC Index Coverage for the target domain. Group URLs by status:
- **Valid:** indexed and serving.
- **Valid with warnings:** indexed but with issues.
- **Excluded — Crawled, currently not indexed:** Google saw the page but chose not to index it.
- **Excluded — Discovered, currently not indexed:** Google knows the URL exists but hasn't crawled or indexed it.
- **Excluded — Duplicate without user-selected canonical:** Google picked a different canonical than intended.
- **Excluded — Duplicate, Google chose different canonical than user:** signal conflict — Google overrode the declared canonical.
- **Excluded — Not found (404):** dead URLs still in Google's awareness.
- **Excluded — Soft 404:** page returns 200 but Google classifies content as empty, thin, or error-like.
- **Excluded — Blocked by robots.txt / noindex:** intentional or unintentional exclusion.

**Cross-reference with value signals:** for URLs in any "Excluded" status, check whether they have impressions, clicks, or backlinks (via GSC or Ahrefs). Excluded URLs with value signals are priority issues — they should be indexed but aren't.

**Output:**

| Status | URL Count | High-Value URLs Affected | Priority |

If GSC is unavailable, state the gap and proceed to signal-based analysis (Sections 2–6). Note reduced confidence — signal audits without outcome verification may recommend fixes for issues Google has already resolved correctly.

---

## 2) Index Eligibility Signals

Audit the directives that control whether pages can be indexed. Cross-reference every finding against GSC coverage status from Section 1 — fix signals only where the actual index outcome is wrong.

**Checks:**
- robots.txt allow/disallow vs intended indexation.
- meta robots tags (index/noindex, follow/nofollow).
- x-robots-tag headers (PDFs, media, non-HTML resources).
- Conflicts:
  - noindex + canonical pointing to itself.
  - Indexable page blocked by robots.txt (Google cannot see the noindex tag if crawling is blocked).
  - Canonical target is noindexed or blocked.
  - Internal links pointing heavily to noindex pages (wasted equity).
- Valuable pages incorrectly excluded (GSC impressions/clicks or Ahrefs backlinks on excluded URLs).

**Output:**

| URL | robots.txt | meta robots | x-robots | canonical | GSC Status | Intended? | Conflict | Fix |

**Fix patterns:**
- Remove unintended noindex; adjust robots rules.
- Ensure canonical targets are indexable and not blocked.
- Ensure internal links prioritize indexable canonical URLs.

**Guardrails:**
- Never recommend indexing thin, duplicate, or trap pages (filters, internal search, carts, login pages).
- Never change signals on a page whose GSC status is already correct. If Google resolved a conflict correctly, changing the signals may cause unintended deindexation.
- If a page is "Crawled, currently not indexed" with correct signals and no conflicts, the issue is content quality or authority — not an indexation signal problem. Flag for content review, do not recommend signal changes.

---

## 3) Soft 404 Detection

Pages returning HTTP 200 but containing thin, empty, or error-like content that Google classifies as soft 404.

**Checks:**
- Pull soft 404 URLs from GSC coverage report.
- For each, scrape the page and assess: is the content genuinely thin/empty/error, or is Google misclassifying a valid page?
- Common causes: empty search result pages, out-of-stock products with no content, template pages with placeholder text, error messages served with 200 status.

**Classification:**
- **Legitimate soft 404:** page is genuinely empty or low-value. Fix: either add substantive content or return proper 404/410 status.
- **Misclassified valid page:** page has real content but Google treats it as soft 404. Fix: strengthen content signals (add unique text, remove boilerplate dominance), or investigate rendering issues. *If the page relies on JS to render content, call `read_skill("tech-seo-rendering")` — content may not be visible to Googlebot.*

---

## 4) Index Bloat

The reverse of missing indexation — pages that *are* indexed but shouldn't be, inflating the index with low-value content and diluting quality signals.

**Checks:**
- Compare total indexed pages (GSC or `site:` count) against the number of pages that should be indexed (meaningful content pages).
- Identify indexed pages that are low-value: parameter variants, internal search results, filter/facet combinations, paginated pages with no unique content, thin tag/archive pages, utility pages (login, cart, thank-you).
- Identify indexed pages with zero impressions over 90 days — these occupy index space but generate no search visibility.

**Output:**

| URL Pattern | Count Indexed | Should Be Indexed? | Impressions (90d) | Recommended Action |

**Fix patterns:**
- noindex for low-value pages that must exist for users.
- 404/410 for pages that should not exist at all.
- Canonical consolidation for parameter variants. *For parameter handling methodology, call `read_skill("tech-seo-redirects")` Section 2.*

**Guardrail:** Do not mass-noindex without checking for backlinks or residual traffic. Some low-value-looking pages may carry link equity.

---

## 5) Canonical Validation

**Checks:**
- Canonical points to 200 status URL.
- Canonical target is indexable (not noindex/blocked).
- Canonical is stable and consistent across variants (http/https, slash, params).
- Canonical loops and chains.
- Canonical vs redirects mismatch (canonical points elsewhere but URL also redirects).
- Canonical across pagination and faceted URLs (must be intentional, not blanket).
- GSC "Duplicate, Google chose different canonical than user" — where Google overrode the declared canonical, identify why and whether the declared canonical or Google's choice is correct.

**Output:**

| URL | Canonical | Canonical Status | Indexable? | GSC Override? | Issue | Fix |

**Fix patterns:**
- Self-referencing canonicals on canonical URLs.
- Canonical parameterized variants to clean primary URL when correct.
- Use redirects for truly deprecated/merged URLs. *For redirect methodology, call `read_skill("tech-seo-redirects")`.*

**Guardrails:**
- Do not canonicalize paginated pages to page 1 unless proven best for that content type.
- Do not use canonical as a substitute for fixing internal linking and URL normalization.
- When Google overrides the declared canonical, investigate Google's choice before insisting on the declared one. Google may be correct.

---

## 6) Duplication

**Checks:**
- URL variants generating duplicate content: http/https, www/non-www, trailing slash, parameters (sort, filter, tracking), printer-friendly, UTM, session IDs.
- Template duplication: repeated titles/descriptions across many pages, heading reuse patterns that collapse uniqueness.
- Content duplication: same body content across multiple URLs (product variants, location pages).

**Output:**

| Cluster ID | URLs | Preferred URL | Reason | Fix Type (301/canonical/noindex) | Priority |

**Fix patterns:**
- Choose one primary URL; 301 deprecated variants.
- Canonical for benign variants that must exist.
- Noindex for low-value duplicates that must exist for users but not search.

**Guardrail:** Always preserve the URL with strongest signals (links/traffic) as preferred unless business requires otherwise.

**Cannibalization:** if GSC data shows the same query ranking with multiple URLs from the domain, do not diagnose here — flag the affected queries and URLs and dispatch to `read_skill("seo-cannibalization-diagnosis")` for full assessment. Duplication (same content, multiple URLs) and cannibalization (different pages, same intent) are different problems requiring different solutions.

---

## 7) Sitemaps

**Checks:**
- Sitemap exists and is referenced in robots.txt.
- All sitemap URLs: return 200, are canonical (self-canonical or canonical targets), are indexable (not noindex/blocked).
- Alignment: sitemap URLs should reflect the intended index set. Identify bloat (URLs that shouldn't be indexed are in the sitemap) and gaps (key URLs missing from the sitemap).
- Cross-reference against GSC coverage: are "Discovered, currently not indexed" pages missing from the sitemap? Adding them may accelerate crawl priority.

**Output:**

| Sitemap URL | URL Count | Non-200 | Non-Canonical | Non-Indexable | Missing Key URLs | Fix |

---

## 8) Guardrails

- Always check GSC index coverage status before recommending signal changes. The actual index outcome takes precedence over signal analysis.
- Never recommend indexing thin, duplicate, parameter, or utility pages regardless of signal configuration.
- Never change signals on pages whose GSC status is already correct — fixing a "conflict" that Google resolved correctly can cause deindexation.
- "Crawled, currently not indexed" with correct signals is a content quality issue, not an indexation signal problem. Flag for content review.
- Duplication and cannibalization are different problems. Duplication = same content, multiple URLs (fix here). Cannibalization = different pages, same intent (dispatch to `seo-cannibalization-diagnosis`).
- If JS rendering is suspected as the cause of indexation failure, dispatch to `read_skill("tech-seo-rendering")` — do not diagnose rendering issues in this skill.
- Every fix must reference the specific URL, the current GSC status, the signal conflict, and the expected outcome after the fix.
