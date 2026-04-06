---
name: tech-seo-redirects
description: Technical SEO audit for redirect health and URL normalization. Focuses on server-side HTTP signals and HTML Meta Refresh. Use when investigating redirect issues, URL normalization problems, redirect chains, trailing slash conflicts, parameter handling, or open redirect risks. Triggers on phrases like "redirect audit", "301 vs 308", "redirect chain", "trailing slash", "meta refresh", "lost link equity", "HSTS redirect", or "open redirect".
---

# Skill: Tech SEO — Redirects & URL Management

## Scope

In scope: HTTP redirects (301, 302, 307, 308), redirect chains and loops, host + protocol normalization, trailing slash conflicts, meta refresh redirects, parameter indexing behavior, pagination crawl structure, open redirect vulnerabilities.

Out of scope: JavaScript redirects, client-side routing, rendering-based redirects.

If HTTP status = 200 but page redirects in-browser → flag as possible JavaScript redirect → read_skill("tech-seo-rendering") for diagnosis.

---

# Core Definitions

| Mechanism | Passes Link Equity | Method Behavior | Recommended Use |
|---|---|---|---|
| HTTP 301 | Yes (~full) | Converts POST → GET | Standard permanent redirect |
| HTTP 308 | Yes (~full) | Does NOT convert POST → GET | Use for APIs, carts, auth paths |
| HTTP 302 | Conditional — consolidates only if Google determines redirect is effectively permanent over time | Converts POST → GET | Temporary moves only |
| HTTP 307 | Conditional — same as 302 | Does NOT convert POST → GET | Temporary redirect; HSTS 307s are browser-internal, invisible to Googlebot |
| `<meta refresh>` instant (0s delay) | Yes — strong canonicalization signal | N/A — browser navigation only | Last resort when server redirect unavailable; poor accessibility practice (W3C) |
| `<meta refresh>` delayed (>0s delay) | Weak — temporary signal only | N/A — browser navigation only | Avoid on indexable pages |
| CDN / edge rule | Depends on status code used | Depends on code used | Hidden chain source; audit separately from CMS |

**Redirect signal rules:**
- 301, 308, `<meta refresh>` 0s → strong permanent canonicalization signal → destination becomes canonical
- 302, 307, `<meta refresh>` >0s → weak temporary signal → source remains canonical
- All 30x redirects pass PageRank per Google; the distinction is canonicalization signal strength, not equity transfer
- Server-side redirects have the highest chance of correct interpretation; use them over meta refresh whenever possible

---

# Tool Stack

| Tool | Purpose |
|---|---|
| httpstatus.io API | Resolve redirect chains, status codes, response headers per URL |
| DataForSEO OnPage API | Site-wide crawl — redirect chains, internal links, canonical tags, parameter URLs |
| DataForSEO Backlinks API | Prioritize redirects with referring domain data |
| Scraper | Detect `<meta refresh>` and canonical tags in `<head>` |
| GSC | Detect indexed parameter URLs, impressions data |
| Ahrefs | Alternative source for backlink and referring domain data |

If a tool is unavailable → skip that check → continue with available signals → state limitation in output.

**DataForSEO OnPage API** crawls the target domain on demand and returns redirect chains, page status codes, internal links, canonical tags, and duplicate tag data. Submit a crawl task and retrieve results once complete.

---

# Tool: httpstatus.io

```
GET https://api.httpstatus.io/v1/status?url=<encoded_url>
```

Returns: `chain[]` (URL + status per hop), `finalUrl`, `totalHops`, response headers.
Use for: per-URL spot checks, HSTS header verification, cross-layer chain confirmation.

---

# Output Format

**Severity levels:**
- 🚨 Critical — site access or transaction flow broken
- 🔴 High — indexing or canonicalization risk
- 🟡 Medium — crawl inefficiency or structural risk
- 🔵 Low — technical debt

**Individual finding format:**
```
[SEVERITY] Issue Found: [Issue Type]

URL: <url>
Current Status: <HTTP code + label>
Pattern Match: <matched rule or pattern>

The Problem: <one sentence>
The Fix: <one sentence>
```

**Example:**
```
🚨 Critical Issue Found: Functional Breakage Risk

URL: `https://site.com/api/v1/checkout`
Current Status: `301 Moved Permanently`
Pattern Match: E-commerce checkout flow (.*\/checkout\/.*)

The Problem: A 301 on this path discards POST data and breaks OPTIONS
pre-flight handshakes in API/headless environments.
The Fix: Change the redirect code from 301 to 308.
```

Summary tables follow individual findings, grouped by section.

---

# 1) Server-Side Redirect Audit

**Detection:**
- DataForSEO OnPage API — site-wide redirect chain data
- DataForSEO OnPage API — all redirecting URLs filtered by status code
- httpstatus.io → spot-check individual URLs; verify chain details and response headers

**Checks:**

| Check | Condition | Flag as |
|---|---|---|
| Redirect chain | `totalHops >= 3` | 🟡 Medium |
| Redirect loop | Any URL repeats in `chain[]` | 🚨 Critical |
| Dead destination | Final URL returns 404, 410, or 500 | 🚨 Critical |
| Wrong redirect type | Permanent content move uses 302 or 307 | 🔴 High |
| Protocol/host inconsistency | Chain includes HTTP→HTTPS→HTTP or www↔non-www mix | 🔴 High |
| Open redirect | 3xx to external domain via `?url=`, `?dest=`, `?redirect=`, `?destination=`, `?next=`, `?return=` | 🟡 Medium |
| Cross-layer chain | Server redirect chain terminates in `<meta refresh>` at final URL (confirm via Scraper) | 🟡 Medium |

**HSTS / 307 logic:**
```
307 detected?
└── Yes → Check for Strict-Transport-Security header in response
          ├── Present → browser-level HSTS; not a server redirect; Googlebot may not see it
          │             → verify server issues explicit 301 HTTP→HTTPS
          │             → verify Strict-Transport-Security header is present on the HTTPS hop
          │               specifically — per RFC 6797, browsers ignore this header on HTTP
          │               responses; it is only valid and cached when received over HTTPS
          └── Absent  → server-issued 307; flag as wrong redirect type if move is permanent
```

**Equity attenuation:** `equity ≈ (0.90)^n` where `n` = hops. Use as relative severity signal only — not a confirmed Google metric.

**Output — Chain map:**

| Source URL | Hop 1 | Hop 2 | Final URL | Final Status | Hops | Layer Types | Issue | Fix |
|---|---|---|---|---|---|---|---|---|

**Output — Equity reclaim list:**

| Legacy URL | Status | Referring Domains (Ahrefs/DFS) | Best Target | Priority |
|---|---|---|---|---|

**Fixes:**
- Chain → collapse to single direct 301
- Host/protocol → enforce at server level, not CMS
- Dead destination (404/410) → identify as broken; recommend restoring content, updating redirect target to a relevant live URL, or using 410 if no suitable match exists
- Redirect target selection (where to point the 301) → determine correct target by checking canonical URLs, GSC performance data, and topical relevance to the source URL
- Open redirect → validate or remove destination parameter

**Guardrails:**
- No redirect to irrelevant page → use 410 if no matching live page exists; use 301 only when a genuinely relevant target can be identified
- Never use 302 for permanent moves

---

# 2) 301 vs 308 — Interaction Integrity

**Rule:** 301 converts POST → GET, discarding request body. In API-first/headless environments, also breaks `OPTIONS` pre-flight handshake. Use 308 for permanent redirects on any interaction path.

**Detection:** DataForSEO OnPage API — retrieve all URLs returning 301; cross-reference against interaction path patterns below.

**Decision logic:**
```
Permanent redirect?
├── No  → 302 or 307
└── Yes → Path matches interaction pattern?
          ├── Yes → 308
          └── No  → 301
```

**Interaction path patterns — flag any 301 matching these:**

| Regex | Risk Category | Severity |
|---|---|---|
| `.*\/api\/.*` | API endpoint | 🚨 Critical |
| `.*\/v[0-9]+\/.*` | Versioned API | 🚨 Critical |
| `.*\/webhook[s]?\/.*` | Webhook receiver | 🚨 Critical |
| `.*\/cart\/.*` | E-commerce cart | 🚨 Critical |
| `.*\/checkout\/.*` | Checkout flow | 🚨 Critical |
| `.*\/add-to-basket.*` | E-commerce (alt) | 🚨 Critical |
| `.*\/order[s]?\/.*` | Order endpoint | 🚨 Critical |
| `.*\/login.*` | Auth | 🔴 High |
| `.*\/signin.*` | Auth (alt) | 🔴 High |
| `.*\/register.*` | Registration | 🔴 High |
| `.*\/signup.*` | Registration (alt) | 🔴 High |
| `.*\/auth\/.*` | Auth flows | 🔴 High |
| `.*\/submit.*` | Generic form | 🟡 Medium |
| `.*\/search.*` | Search (POST variant) | 🟡 Medium |
| `.*\/filter.*` | Filter (POST variant) | 🟡 Medium |
| `.*\/comment[s]?.*` | Comments | 🟡 Medium |
| `.*\/contact.*` | Contact form | 🟡 Medium |

**Output:**

| Source URL | Pattern Match | Current Code | Fix | Severity |
|---|---|---|---|---|

**Guardrails:**
- Path name alone is not proof of POST usage — confirm with dev team before changing
- Do not apply 308 to static content URLs (pages, images, assets)
- Uncertain → default to 308
- Redirect consolidation involves competing URLs for same keyword → read_skill("seo-cannibalization-diagnosis") before deciding target

---

# 3) Meta Refresh Detection

**Detection:** Scraper checks `<head>` for `<meta http-equiv="refresh">` on individual URLs. For site-wide detection, use DataForSEO OnPage API to retrieve all pages with meta refresh signals.

**Checks:**

| Condition | Flag as |
|---|---|
| `<meta refresh>` present on indexable page | 🔴 High |
| Delay > 0 seconds | 🚨 Critical (doorway-page risk) |
| `<meta refresh>` + server-side redirect on same URL | 🔴 High (conflicting signals) |
| `<meta refresh>` as final step in redirect chain | 🟡 Medium (forces renderer; delays indexing) |

**Output:**

| URL | Delay (s) | Destination | Server HTTP Status | Chain Tail? | Fix |
|---|---|---|---|---|---|

**Fix:** Replace with server-side 301 or 308.

**Guardrail:** `<meta refresh>` with delay > 0 on indexable pages → always flag Critical.

---

# 4) Trailing Slash & Host Normalization

**Detection:**
- httpstatus.io → test both `/page` and `/page/` variants for key URLs
- DataForSEO OnPage API — internal links report to detect mixed slash variants
- DataForSEO OnPage API — pages report to verify canonical tags match the 200-OK variant

**Checks:**

| Test | Expected | Failure → Flag as |
|---|---|---|
| `/page` and `/page/` via httpstatus.io | One returns 200; other 301 to canonical | Both 200 → 🔴 High (duplicate); loop → 🚨 Critical |
| `rel="canonical"` on 200-OK variant | Matches 200-OK URL | Mismatch → 🔴 High |
| Internal links (DataForSEO OnPage) | All use canonical variant | Mixed variants → 🟡 Medium |
| Sitemap URLs | All use canonical variant | Mixed variants → 🟡 Medium |
| CDN slash handling | Matches origin behavior | CDN adds/strips differently → 🔴 High |

**Output:**

| URL Base | With-Slash | Without-Slash | Canonical Tag | Internal Links Variant | Conflict? | Fix |
|---|---|---|---|---|---|---|

**Fix:** Pick one variant → enforce via server-level 301 → update sitemap and internal links.

**Guardrail:** Canonical tag alone is insufficient — enforce with a server-level redirect.

---

# 5) Parameters & Pagination

**Detection:**
- GSC Search Analytics — identify which parameter URLs are indexed
- DataForSEO OnPage API — pages with parameter URLs; verify canonical tags
- DataForSEO OnPage API — internal links report to detect links generating parameter URLs

**Parameter checks:**

| Parameter type | Examples | Fix |
|---|---|---|
| Tracking | `utm_*`, `fbclid`, `gclid` | Canonical to clean URL |
| Sorting | `sort=` | Canonical to default sort |
| Facets | `color=`, `size=` | Allow strategic combinations; noindex + canonical on others |
| Internal search | `q=` | noindex; if infinite combinations → also disallow in robots.txt (see note) |
| Pagination | `page=` | Self-referencing canonical per page |

Additional checks:
- Infinite combination risk → DataForSEO OnPage API — count unique parameter combinations from crawl
- Canonical targets correctly set → DataForSEO OnPage API pages report

**Note on infinite parameter combinations:** For parameter sets that generate millions of URLs (multi-facet explosion, unbounded search queries), noindex alone is insufficient — Google will still crawl every URL to discover the noindex tag, consuming crawl budget. In this case, combine noindex with robots.txt Disallow. Exception: do not block via robots.txt if canonical or noindex tags on those URLs need to be read by the crawler to resolve a specific indexing issue.

**Pagination checks:**

| Requirement | Detection | Failure → Flag as |
|---|---|---|
| Links are HTML `<a>` tags | DataForSEO OnPage API | JS-only links → 🔴 High |
| Each page has self-referencing canonical | DataForSEO OnPage API | Missing → 🔴 High |
| Infinite scroll has crawlable fallback URLs | DataForSEO OnPage API | Missing → 🔴 High |
| No duplicate `<title>` or `<meta description>` across series | DataForSEO OnPage API | Duplicates → 🟡 Medium |

**Output — Parameters:**

| Param | Type | Unique Content? | Index Allowed? | Canonical Target | Recommendation |
|---|---|---|---|---|---|

**Output — Pagination:**

| Series Root | Page Count | Link Type | Canonical Pattern | Issues | Fix |
|---|---|---|---|---|---|

**Guardrails:**
- Do not block parameter URLs via robots.txt if noindex/canonical needs to be crawled to resolve an indexing issue
- For infinite parameter combinations → robots.txt Disallow is correct; noindex alone is insufficient at scale
- Do not canonical paginated pages to page 1 — de-indexes deep content

---

# Audit Priority Order

1. 🚨 Critical — redirect loops and dead targets
2. 🚨 Critical — transactional paths using 301 instead of 308
3. 🔴 High — host / protocol normalization issues
4. 🟡 Medium — redirect chains > 2 hops
5. 🟡 Medium — open redirects
6. 🟡 Medium — meta refresh as chain tail
7. 🟡 Medium — HSTS / 307 misconfiguration
8. 🔵 Low — legacy meta refresh cleanup
9. 🔵 Low — parameter indexing issues
