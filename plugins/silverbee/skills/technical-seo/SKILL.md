---
name: technical-seo
description: Technical SEO audit. Runs preliminary (homepage-only) or full (site-wide) audits covering server health, crawl, indexation, redirects, rendering, performance, schema, and ecommerce. Use when user mentions "technical SEO", "site audit", "technical audit", "crawl issues", "indexing problems", or requests a technical health check. Not for content strategy, link building, or prospect outreach — if the request mentions "prospect", "outreach", "lead gen", or "cold audit", use prospect-snapshot instead.
---

# Skill: Technical SEO

## Title
Technical SEO Audit

## Description
Technical SEO audit with two modes containing all checks required for a preliminary (homepage-scoped) audit- Specialized micro-skills should only be loaded when the user specifically requests deeper analysis on that topic or when running a full site-wide audit on that layer, and are referenced under each section. 

---

## Before running anything (mandatory)

Do not call any tools until you have collected required inputs.

Use `AskUserQuestion` to gather inputs in a **single call**:
```json
{
  "questions": [
    {
      "question": "What domain or URL should I audit?",
      "header": "Domain/URL",
      "options": [],
      "multiSelect": false
    },
    {
      "question": "What audit depth do you want?",
      "header": "Audit Mode",
      "options": [
        { "label": "Preliminary", "description": "Homepage-only — fast, covers all critical checks" },
        { "label": "Full site-wide", "description": "Deep audit across all sections and pages" },
        { "label": "Specific topic", "description": "I'll tell you which area (crawl, redirects, schema, etc.)" }
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

**Required:** target domain or URL(s).
**Optional:** audit mode (preliminary or full), specific modules to focus on.

If mode is not specified, ask the user. Default to preliminary.

---

## 2) Execution Rules

**Prospect/outreach requests:** if the user asks for a "prospect audit", "prospect snapshot", "cold outreach audit", or any assessment framed as lead gen or prospecting, do not run this skill. Call `read_skill("prospect-snapshot")` instead.

**Preliminary audit:** this file is self-contained. Execute all checks below against the homepage only. Run CWV on homepage only (mobile mandatory). No multi-page crawling. No site-wide DOM analysis. **Do not load micro-skills** unless the user requests a deep dive on a specific topic.

**Full audit:** run each section at site-wide depth. Load the referenced micro-skill for each section to get the full methodology, checks, failure conditions, and output tables for that layer.

**Specific-topic request** (e.g., "check my redirects", "audit my structured data"): load only the relevant micro-skill for that topic. Do not load unrelated skills.

**Priority order is mandatory in all modes.** Fix discovery/crawl issues before optimizing on-page. Do not bury critical crawl/index issues below performance or schema findings. Sections are listed in priority order.

---

## 3) Checks

### 3.1 Server & Response

Confirm homepage returns 200, response headers are valid (text/html), no intermittent 4xx/5xx, protocol and host normalize to a single indexable variant (http→https, www or non-www), no mixed-content assets.

*Deep dive or full audit: call `read_skill("tech-seo-crawl")`.*

---

### 3.2 Crawl & Discovery

Confirm homepage is not blocked by robots.txt, important pages are internally linked from navigation, no obvious orphan important URLs, important pages reachable within three logical clicks, internal links do not point to 404s or redirected URLs.

*Deep dive or full audit: call `read_skill("tech-seo-crawl")`.*

---

### 3.3 Index Eligibility

Confirm homepage is indexable (not blocked by robots.txt, no meta or x-robots noindex), no index/noindex contradictions, internal links are not primarily pointing to noindex pages.

*Deep dive or full audit: call `read_skill("tech-seo-indexation")`.*

---

### 3.4 Canonical & Metadata

Confirm homepage canonical exists, is self-referencing, is indexable, matches preferred host/protocol, matches sitemap homepage URL. Confirm exactly one title tag, one meta description, no empty values. Confirm OG:title, OG:description, OG:image, OG:url exist and og:url matches canonical.

*Deep dive or full audit: call `read_skill("tech-seo-indexation")`.*

---

### 3.5 Duplication

Confirm homepage is accessible via only one indexable variant (http/https, www/non-www, trailing slash), no uncontrolled duplicate homepage URLs.

*Deep dive or full audit: call `read_skill("tech-seo-indexation")`.*

---

### 3.6 Redirect Integrity

Confirm homepage normalization redirects are single-hop, no redirect chains longer than two hops, redirects resolve to 200 pages, legacy homepage variants do not return 404.

*Deep dive or full audit: call `read_skill("tech-seo-redirects")`.*

---

### 3.7 Parameters & Pagination

Confirm homepage does not link to internal search URLs or uncontrolled filter/facet URLs, no parameterized homepage variants indexed.

*Deep dive or full audit: call `read_skill("tech-seo-redirects")`.*

---

### 3.8 Rendering

Confirm main content exists in raw HTML (not JS-only), navigation uses crawlable `<a href>` links, no hydration failures or placeholder-only content.

*Deep dive or full audit: call `read_skill("tech-seo-rendering")`.*

---

### 3.9 Performance / Core Web Vitals

Run PageSpeed Insights (mobile mandatory), flag failing LCP/CLS/INP, identify render-blocking CSS/JS, identify LCP element and blocking resource. Do not summarize scores — surface specific issues and affected resources.

*Deep dive or full audit: call `read_skill("tech-seo-performance")`.*

---

### 3.10 Images

Confirm meaningful images have non-empty alt attributes, hero image has alt, hero image is not oversized for LCP.

*Deep dive or full audit: call `read_skill("tech-seo-performance")`.*

---

### 3.11 Mobile Parity

Confirm mobile homepage contains same primary content as desktop, no hidden headings or content, no mobile usability blockers (viewport, tap targets).

*Deep dive or full audit: call `read_skill("tech-seo-performance")`.*

---

### 3.12 Sitemaps

Confirm sitemap exists and is accessible, homepage included, sitemap homepage URL returns 200, matches canonical, is indexable, no noindex or blocked URLs present.

*Deep dive or full audit: call `read_skill("tech-seo-indexation")`.*

---

### 3.13 Structured Data

Detect schema on homepage, confirm schema matches visible content, no conflicting schema types, no schema on noindex pages, no fatal syntax errors.

*Deep dive or full audit: call `read_skill("tech-seo-schema")`.*

---

### 3.14 International / Hreflang (If Applicable)

If hreflang exists, confirm reciprocal links, valid language-region codes, indexable hreflang URLs. If site is multilingual and hreflang is missing, flag.

---

### 3.15 Ecommerce (If Applicable)

Confirm homepage does not expose crawl traps via filters, internal search pages not indexable, out-of-stock products not blindly noindexed or removed.

*Deep dive or full audit: call `read_skill("tech-seo-ecommerce")`.*

---

### 3.16 Releases / Recovery (Conditional)

If traffic drop or deployment is mentioned, compare current vs historical robots.txt, canonical, meta robots, rendering, and CWV using Archive.org snapshots and PSI history. Flag regressions aligned with release timing.

*For full drop root-cause analysis: call `read_skill("drop-analysis")`.*

---

## 4) Evidence Requirements

Every issue must be tied to a specific URL, resource, or rule. No generic advice. Every recommendation must include:

- **What** is wrong
- **Where** it occurs (specific URL or resource)
- **Why** it matters (SEO impact)
- **Fix** (copy-paste code, exact configuration steps, or precise instructions)

---

## 5) Tool Usage

| Tool | Role | Required |
|---|---|---|
| **PageSpeed Insights** | CWV, performance diagnostics, rendering signals. Mobile + desktop. | **Mandatory** for performance checks. |
| **Scraper / Web Fetch** | HTML extraction: meta, headings, images, links, structured data, DOM analysis. | **Mandatory.** |
| **GSC** | Page-scoped and site-scoped data. Coverage, indexing, crawl stats. | Preferred. Fallback → Ahrefs → DataForSEO. |
| **Ahrefs** | Site structure data, backlink data for redirect reclaims. | Fallback for GSC. |
| **DataForSEO** | Site audit data fallback. | Fallback if GSC and Ahrefs unavailable. |
| **Google Search** | `site:` queries for index verification. | Optional but recommended. |

---

## 6) Reporting Standard

1. **Executive summary** — business impact + top 5 fixes.
2. **Issues by priority layer** — ordered by section number (3.1 through 3.16).
3. **Quick wins** — fixes implementable in <30 minutes.
4. **Implementation checklist** — step order by priority.

**Priority labels:**
- 🔴 Critical — blocks crawl, index, or renders site invisible
- 🟠 High — degrades ranking signals or wastes crawl budget materially
- 🟡 Medium — suboptimal but not actively harmful
- ⚪ Low — best practice improvement

---

## 7) Execution Guardrails

1. **Priority order is non-negotiable.** Do not surface schema recommendations above unresolved crawl or index issues.
2. **Every issue needs evidence.** No generic best practice lists.
3. **Fixes must be actionable.** Copy-paste code, exact config steps, or specific file/line references.
4. **Do not recommend architectural overhauls when narrow fixes solve the problem.**
5. **Preliminary mode stays homepage-scoped.** Do not expand unless explicitly switched to full mode.
6. **Do not load micro-skills unless needed.** Preliminary audit runs entirely from this file. Micro-skills are loaded only for deep dives, specific-topic requests, or full audit mode.
7. **Report after each section.** Do not batch all findings to the end.

---

## Step Count: 8

| # | Step | Duration Estimate |
|---|------|-------------------|
| 1 | Domain resolution | 2s |
| 2 | HTTP status / server check | 2–3s |
| 3 | Robots.txt / meta robots | 2s |
| 4 | Core Web Vitals | 5–8s |
| 5 | Schema validation | 3–5s |
| 6 | Redirect audit | 3–5s |
| 7 | Indexation check | 3–5s |
| 8 | Output generation | 3–5s |

## Step Criticality

| Step | Critical | Fallback |
|------|----------|----------|
| Domain resolution | Yes | Cannot proceed |
| HTTP status / server check | Yes | Cannot proceed |
| Robots.txt / meta robots | No | Note "robots data unavailable" |
| Core Web Vitals | No | Skip CWV section, note in output |
| Schema validation | No | Skip schema section, note in output |
| Redirect audit | No | Skip redirects section, note in output |
| Indexation check | No | Skip indexation section, note in output |

## Dashboard Template

Use `render_template("technical-seo", data)` via the silverbee-mcp MCP.

| Field | Type | Description |
|---|---|---|
| `title` | string | Dashboard heading |
| `metrics.issuesFound` | string | Total issues found |
| `metrics.criticalIssues` | string | Critical issue count |
| `metrics.pagesCrawled` | string | Pages crawled count |
| `metrics.cwvStatus` | string | Core Web Vitals status |
| `chart.data[]` | array of `{category, count}` | Issues by category (category: string, count: number) |
| `findings.rows` | string[][] | Findings table rows |
| `roadmap.rows` | string[][] | Fix roadmap table rows |

All metric values are **strings** (not numbers). Table `rows` are `string[][]` (arrays of string arrays, not objects).

For custom specs or troubleshooting, load the `show-generative-ui` skill.

---

## Output Format

When all data collection and analysis is complete, call `read_skill("seo-output-formatter")` and follow its instructions to format and present the full deliverable.
