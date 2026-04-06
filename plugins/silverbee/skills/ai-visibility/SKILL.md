---
name: ai-visibility
description: AI visibility audit and optimization. Domain-level LLM mention tracking (Ahrefs Brand Radar), prompt-level competitor gap analysis (DataForSEO AI Visibility), cross-validation, llms.txt validation (llmstxt.org spec), page-type-aware schema coverage, FAQ markup, AI crawlability, RSS/feed discovery, content citation signals, AI Overview presence. Use for GEO (Generative Engine Optimization), LLMO (Large Language Model Optimization), AEO (Answer Engine Optimization), AI Overview optimization, GEO competitor gap analysis, GEO competitor discovery, or any request about site visibility in AI/LLM engines (ChatGPT, Claude, Gemini, Perplexity, Google AI Overviews).
---

# Skill: AI Visibility Audit

## Title
AI Visibility & GEO/LLMO/AEO Audit

## Description
Audits and optimizes site visibility in AI-powered search and answer engines. Domain-level mention tracking via Ahrefs Brand Radar, prompt-level competitor gap analysis via DataForSEO AI Visibility (per-engine, with cited source extraction), llms.txt validation per llmstxt.org, page-type-aware schema coverage, AI crawlability and feed availability, content citation signals, and prioritized recommendations. Cross-validates findings when both domain-level and prompt-level analyses are available.

---

## Before running anything (mandatory)

Do not call any tools until you have collected required inputs.

Use `AskUserQuestion` to gather inputs in a **single call**:
```json
{
  "questions": [
    {
      "question": "What domain or brand should I audit for AI visibility?",
      "header": "Domain/Brand",
      "options": [],
      "multiSelect": false
    },
    {
      "question": "Which AI engines should I check visibility for?",
      "header": "AI Engines",
      "options": [
        { "label": "All available engines", "description": "ChatGPT, Google AIO, Gemini, Perplexity" },
        { "label": "Google AI Overviews only", "description": "Focus on Google search" },
        { "label": "ChatGPT only", "description": "OpenAI's ChatGPT mentions" },
        { "label": "Full GEO audit", "description": "Brand Radar + prompt-level gap analysis" }
      ],
      "multiSelect": false
    }
  ]
}
```

After collecting inputs, confirm them in a short text message and **wait for the user's go-ahead** before making any tool calls.

---

## Tool execution

Use this pattern for all data fetching:
1. `list_available_apps` — confirm which data sources are connected
2. `search_actions(query)` or `list_actions(app_name)` — find the right operation
3. `run_action(app_name, operation_id, input)` — execute

**MANDATORY — parallel execution:** Batch all independent queries into a single `run_multi_actions` call. Never call `run_action` in a sequential loop — that is a performance bug. On any app-specific error, try the fallback chain (see supervisor "Step 3") before stopping. On connection/auth errors (all tools failing), follow the supervisor's "Tool call errors" section.

---

## 1) Input

**Required:** target domain.
**Optional:** specific URLs to prioritize, competitor domains, topic/keyword focus areas.

---

## 2) Site Context

**Establish before all other checks.** Obtain the target domain's site context — from account data, site profile, or homepage extraction.

Required context:
- Core offering (products, services, content verticals).
- Primary entities (brand, people, locations) and how they are described.
- Target audience and market positioning signals.
- Key topic areas that would generate natural AI queries.

This context scopes every subsequent section — Brand Radar gaps, missing schema, content weaknesses, and AI Overview absence are only meaningful relative to what the site should be visible for.

---

## 3) Custom Query Set (user-requested only)

**Skip unless the user requests analysis of specific queries.** By default, Brand Radar (Section 4) returns all triggering queries per domain — a pre-built query set is unnecessary.

When requested: use Ahrefs Keywords Explorer to build 15–30 non-branded queries scoped to the site context from Section 2. This custom set then drives AI Overview presence checks (Section 9) and targeted content evaluation (Section 8).

---

## 4) LLM Mention Baseline

Two distinct analysis types. These are not interchangeable — each answers a different question.

### 4a) Domain-Level Mention Tracking (Ahrefs Brand Radar)

**What it answers:** "Where does my domain appear across LLM responses?"

**When using Ahrefs Brand Radar:** call `read_skill("ahrefs-brand-radar")` before executing any Brand Radar tool calls. That skill defines allowed data sources and execution constraints.

No queries needed as input — Brand Radar takes a domain and returns:
- Total LLM mention count.
- Mention count by URL — which pages LLMs cite.
- Triggering queries — what users ask when the site appears.
- Trend direction if historical data exists.
- Per-engine breakdown if the provider supports it.

**Competitor benchmarking:** if competitor domains are provided or identifiable from site context, pull the same metrics. Compare mention counts, overlapping queries, and pages competitors get cited for that the target does not.

If Brand Radar is unavailable, state the gap. The dataforseo-ai-visibility tool cannot substitute — it requires specific queries as input and cannot produce a domain-wide mention scan.

### 4b) Prompt-Level Competitor Gap Analysis (DataForSEO)

**What it answers:** "For the key questions users ask about my category, which domains appear in LLM answers — and am I among them?"

**Requires a query set as input.** This analysis cannot run without specific questions to test. Build the query set:

1. From the site context (Section 2), derive the domain's precise long-tail niche — the specific positioning within its industry, not a broad parent category. The niche must be narrow enough to return meaningful competitors.
2. Determine the primary competitive region from site context.
3. Construct questions that reflect how users prompt LLMs for recommendations in this space. Core question pattern: "What are the leading websites for [derived niche] in [region]?" — omit region only if the niche is globally narrow enough that adding one would over-restrict results.
4. Optionally expand with additional WH-type questions via Ahrefs Keywords Explorer (who, what, which, where, how, why) scoped to the niche.

**Execute per AI engine separately.** Submit each question using the dataforseo-ai-visibility tool for each available engine (ChatGPT, Google AI Overviews, and any other supported model). Do not merge results across engines — each may cite different domains and rely on different sources.

**Per question per engine, capture:**
- The full LLM answer text.
- Which domains/brands the LLM named in its answer and their positioning.
- Whether the target domain appears — if yes, where and how; if no, state explicitly.
- Cited source annotations — the full list of URLs the LLM relied on to produce the answer.

**Competitor emergence analysis (aggregate across all questions):**
- Which competitors appear most frequently across engines.
- Competitors that appear consistently across engines (high-confidence) vs. single-engine mentions.
- Cited sources that recur across questions and engines — these are the authoritative references driving AI citations in this category.
- Questions where the target domain is absent but competitors are present — priority gaps.

**Output (mandatory format for all prompt-level analysis):**

**Executive Summary:**

| Question Submitted | Total Competitors Found | {domain} Visible In | Top Competitor | Top Cited Source |

One short paragraph: where {domain} stands (present in N of M engines or absent entirely), the highest-confidence competitors (most engines), and the most recurring cited sources.

**Competitor Presence Matrix:**

Collect all unique domains mentioned across all engine responses into a single table. First column lists every domain. Remaining columns are the AI engines. Mark ✓ if mentioned, ✗ if not. **Target domain appears as the first row in bold.** Sort remaining rows by total ✓ count descending.

| Domain | ChatGPT | Google AIO | Gemini | Claude | Perplexity |
|---|---|---|---|---|---|
| **{domain}** | ✓/✗ | ✓/✗ | ✓/✗ | ✓/✗ | ✓/✗ |
| competitor-a.com | ✓/✗ | ✓/✗ | ✓/✗ | ✓/✗ | ✓/✗ |

**Cited Sources Matrix:**

Same structure. List all source URLs cited by any engine as references for their answers. Mark ✓/✗ per engine. Sort by total ✓ count descending.

| Source URL | ChatGPT | Google AIO | Gemini | Claude | Perplexity |
|---|---|---|---|---|---|
| source-url.com | ✓/✗ | ✓/✗ | ✓/✗ | ✓/✗ | ✓/✗ |

### When to run which

- **Brand Radar (4a):** always run when available. Provides the domain's baseline AI footprint without requiring query input.
- **Prompt-level (4b):** run when the user requests competitor gap analysis, GEO competitor discovery, or when Brand Radar shows low/no mentions and the user wants to understand who appears instead. Requires site context for niche derivation + dataforseo-ai-visibility tool for per-engine LLM answer retrieval.
- **Both:** run both when the user requests a full GEO audit. Brand Radar shows where the domain appears; prompt-level shows where it's missing relative to competitors. Cross-validation runs in Section 10.

---

## 5) llms.txt Validation

Fetch `{domain}/llms.txt`.

### If exists — validate against llmstxt.org:

The spec requires this structure in this order:
1. **H1** with site/project name (only mandatory element).
2. **Blockquote** with concise site summary.
3. **Zero or more body sections** (paragraphs, lists — no headings) with additional context.
4. **Zero or more H2 sections** containing file lists. Each item: `[name](url)` optionally followed by `: notes`.
5. **`## Optional`** section (if present) for secondary resources skippable in shorter contexts.

Validate:
- File at root path `/llms.txt`.
- Valid, parseable markdown.
- H1 present. Blockquote present and concise.
- Linked URLs return 200 and point to substantive content.
- Content is LLM-context-specific — not a copy of robots.txt, sitemap, or marketing boilerplate.

Output: Pass/Fail per check, specific issues, fixes.

### If missing — generate one:

Produce a spec-compliant llms.txt from scraped site structure. Include only pages that help an LLM accurately represent the site. Do not dump the sitemap.

---

## 6) AI Crawlability & Feed Discovery

Check robots.txt for directives affecting known AI crawlers: GPTBot, ClaudeBot, Google-Extended, PerplexityBot, Bytespider.

Report:
- Which AI crawlers are explicitly allowed, blocked, or unaddressed.
- Whether sitemap.xml exists, is accessible, and is referenced in robots.txt.
- Whether key content pages are crawlable and return 200.

**RSS / Atom feeds:** check for feed availability on sites with regularly published content (news, blog, articles, product updates, podcasts). Feeds provide AI systems with structured, timestamped content streams. If the site publishes content regularly and has no discoverable feed (check `<link rel="alternate" type="application/rss+xml">` in `<head>`, `/feed`, `/rss`, `/atom.xml`), flag as a gap. Do not recommend feeds for sites without recurring publishable content.

If AI crawlers are blocked, confirm with user before recommending changes — blocking may be intentional.

---

## 7) Structured Data for AI Readability

Structured data enables accurate extraction and citation by AI engines. Recommendations must be page-type-aware — recommend only schema types that match the page's actual content.

Check for presence, validity (JSON-LD syntax), and content match (schema reflects visible page content):

**Per page type:**
- **Homepage:** Organization or LocalBusiness — entity identity for brand attribution. SameAs links to official social profiles.
- **FAQ / Help pages:** FAQPage schema. If FAQ content exists without schema, flag. If schema exists, confirm it matches visible Q/As — no fabricated entries.
- **Articles / Blog posts / News:** Article, NewsArticle, or BlogPosting — author, datePublished, dateModified, headline. SpeakableSpecification where applicable for voice/AI answer eligibility.
- **Product pages:** Product + Offer — pricing, availability, reviews. AggregateRating if reviews exist.
- **How-to / Tutorial pages:** HowTo schema with step-by-step structure matching visible content.
- **Event pages:** Event schema with date, location, performer/organizer.
- **People / Author pages:** Person schema — name, jobTitle, affiliation, sameAs. Strengthens E-E-A-T signals for authored content.
- **Video content pages:** VideoObject — name, description, thumbnailUrl, uploadDate, duration.
- **Course / Educational content:** Course schema with provider, description, offers.
- **Review pages:** Review or CriticReview with itemReviewed.
- **All navigational hierarchies:** BreadcrumbList — site hierarchy for content relationship signals.

Recommend schema only when matching content exists on the page. Never recommend schema for content that isn't there.

*For full structured data audit and JSON-LD generation, call `read_skill("tech-seo-schema")`*

---

## 8) Content Structure & Citation Signals

AI engines cite content they can extract cleanly. Evaluate the site's top pages against Brand Radar triggering queries or the custom query set (Section 3) if provided.

**Answer readiness:** Key pages must open with direct, specific answers. Claims must be citable — numbers, dates, named entities — not vague assertions. Filler above the answer reduces citation probability.

**Extractable structure:** Clear H2/H3 hierarchy segmenting topics into discrete, self-contained blocks. Each block must be understandable without surrounding context.

**Entity clarity:** The primary entity (brand/business/person) must be consistently named and described across homepage, about page, and schema. Ambiguity reduces citation likelihood.

**Freshness:** Key pages must be dated in both visible content and schema (datePublished, dateModified). Evidence of regular content updates strengthens selection as a source.

**Authority:** Author attribution on editorial content. Outbound citations to authoritative sources. Unique data, original research, or expert perspective that differentiates from commodity content.

---

## 9) AI Overview Presence Check

For the top Brand Radar triggering queries — or the custom query set (Section 3) if provided — search Google and check:
- Whether an AI Overview triggers.
- Whether it cites the target domain.
- If not, which competitors are cited.

**Requires Google Search tool.** If unavailable, skip and note the gap.

Output:

| Query | AI Overview Triggered | Target Cited | Competitor Cited | Notes |

---

## 10) Cross-Validation (Brand Radar + Prompt-Level)

**Activate when both Section 4a and 4b were executed.** If only one ran, skip this section.

Cross-reference findings:

- **Confirmed visibility:** Brand Radar shows domain mentioned for a query AND prompt-level analysis confirms domain appears for related questions → high confidence.
- **Brand Radar only:** domain appears in Brand Radar data but prompt-level questions in the same topic area don't surface it → may reflect question phrasing differences, engine-specific behavior, or Brand Radar capturing edge mentions. Flag for investigation.
- **Prompt-level only:** domain appears in dataforseo-ai-visibility responses but not in Brand Radar → may reflect low mention volume below Brand Radar thresholds, or engine-specific coverage. Flag as emerging visibility.
- **Competitor consensus:** both Brand Radar competitor benchmarking and prompt-level gap analysis identify the same competitors dominating the same topic areas → high-confidence competitive gap, prioritize.
- **Cited source overlap:** sources cited in prompt-level LLM responses (4b) that also link to competitors in Brand Radar data → these are the authoritative references driving AI citations in this category. Potential link building or content partnership targets.

**Output:** consolidated findings table highlighting confirmed gaps, emerging signals, and priority competitors with evidence from both analysis types.

---

## 11) Output

**Executive Summary:** AI visibility status (strong / emerging / weak / invisible), Brand Radar mention baseline, prompt-level gap findings (if run), llms.txt status, top structural gaps, priority actions.

**Section-by-section findings** from Sections 2–10 with specific issues and fixes.

**Priority action list** ordered by impact:
1. **Access** — crawlability, llms.txt, sitemap, feeds (can AI engines reach the content).
2. **Extraction** — schema, content structure, entity clarity (can AI engines parse and cite it accurately).
3. **Authority** — freshness, author signals, unique value (will AI engines choose this source over alternatives).
4. **Monitoring** — Brand Radar tracking cadence, periodic prompt-level re-testing, query-level citation tracking over time.

---

## 12) Guardrails

- Never estimate LLM mention rates. Provider data or stated gap. No middle ground.
- Never fabricate llms.txt content. Generated files must reflect scraped site structure only.
- llms.txt must follow the llmstxt.org spec exactly. No format variations.
- Schema recommendations must match the page type and visible content. No markup for content that does not exist on the page. No HowTo on pages without steps, no FAQPage without Q/As, no Review without a review.
- The dataforseo-ai-visibility tool is not a fallback for Brand Radar. They answer different questions — Brand Radar scans domain-wide without queries, DFS requires specific questions per engine. Do not treat them as interchangeable.
- Competitor benchmarking within Brand Radar must compare domain-to-domain. Prompt-level gap analysis must use the same question set for all domains compared.
- Cross-validation (Section 10) compares findings across analysis types, not across equivalent data sources. Do not average or blend metrics.
- AI visibility and traditional organic rankings are independent metrics. Report each separately — do not conflate.
- RSS feed recommendations apply only to sites with recurring publishable content. Do not recommend feeds for static sites.
- Do not expand the custom query set beyond topics the site actually covers.
- Do not recommend unblocking AI crawlers without user confirmation.
- Every recommendation must tie to a specific finding. No generic best-practice padding.
- Report findings progressively. Do not hold all findings for a single batch output.

---

## Dashboard Template

Use `render_template("ai-visibility", data)` via the silverbee-ui MCP.

| Field | Type | Description |
|---|---|---|
| `title` | string | Dashboard heading |
| `metrics.llmMentions` | string | Total LLM mention count |
| `metrics.aiEngines` | string | Number of AI engines checked |
| `metrics.llmsTxtStatus` | string | llms.txt validation status |
| `metrics.topCitedUrl` | string | Most-cited URL |
| `chart.data[]` | `{engine: string, mentions: number}` | AI engine mention counts for bar chart |
| `competitorPresence.rows` | string[][] | Competitor presence matrix rows |
| `aioPresence.rows` | string[][] | AI Overview presence rows |

All metric values are **strings** (not numbers). Table `rows` are `string[][]` (arrays of string arrays, not objects).

For custom specs or troubleshooting, load the `show-generative-ui` skill.

---

## Output Format

When all data collection and analysis is complete, call `read_skill("seo-output-formatter")` and follow its instructions to format and present the full deliverable.
