---
name: content-optimization
description: SEO content optimization with mandatory keyword validation. Exact-term embedding, density/repetition limits, metadata rules, GSC query retention. Supports pages, paragraphs, headings, title/description, FAQs, social, documentation.
---
# Skill: Content Optimization

## Title
Content Optimization (for SEO)

## Description
Governs all content optimization requiring validated keywords before any rewrite, with exact-term preservation and density controls.

---

## Before running anything (mandatory)

Do not call any tools until you have collected required inputs.

Use `AskUserQuestion` to gather inputs in a **single call**:
```json
{
  "questions": [
    {
      "question": "What page URL or content piece should I optimize?",
      "header": "URL / Content",
      "options": [],
      "multiSelect": false
    },
    {
      "question": "Do you have target keywords, or should I research them?",
      "header": "Keywords",
      "options": [
        { "label": "I'll provide keywords", "description": "Paste them in chat after this" },
        { "label": "Research them for me", "description": "I'll run keyword research on the URL or topic" }
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

## Core Rule

Never optimize content without validated keywords from approved sources (user-provided list or Keyword Research output). Use exact terms as researched without modifications. Optimize in the content's original language — never translate content to another language during optimization. Maintain non-branded focus unless explicitly requested; however, retain branded terms already present in the original content where semantically necessary. Apply strict density and repetition limits.

---

## 1) Gate: Keywords Are Mandatory

**Rule:** Do not optimize any content (rewrite, expand, compress, restructure, or create metadata) unless a **keywords source** exists and is **validated** as relevant.

A "keyword source" means: a list of exact terms that will be intentionally embedded in the optimized output.

### 1.1 Allowed keyword sources (only these)

- **User-provided keyword list** (directly supplied by the user in the request), and/or
- **Keyword Research workflow output** (Page URL–based research or Topic-based research)
  - *For the full keyword research workflow, call `read_skill("keyword-research")`*

### 1.2 Forbidden behavior

- Do not "invent" keywords.
- Do not generate synonyms unless they were explicitly provided by a keyword research output or a user provided list.
- Do not introduce new terms by changing spelling, adding prefixes/suffixes, pluralizing, or merging terms (exact-term rule applies later).

### 1.3 Keyword validation (must happen before any optimization)

Validate each keyword against the optimization input, using these checks:

1. **Scope match:** The keyword must describe the same core topic/value as the content being optimized (no "nearby" topics).
2. **Intent match:** The keyword's implied intent must fit the content unit's intent (informational vs commercial vs transactional vs navigational).
3. **Language match:** The keyword must be in the same language as the content. If the keyword is in a different language, it is invalid unless the content is explicitly bilingual.
4. **Branding rule:** The keyword must be non-branded unless a matching branded term already appears in the original content (title/description/headings/body), or unless the user explicitly stated branded keywords should be included.
5. **Noise removal:** Drop generic fillers and vague terms that do not add semantic value (e.g., "best", "top", "guide") unless they were explicitly returned by research AND clearly match intent.
6. **Scope hierarchy (and cannibalization check):** Keywords must match the page's architectural role. A parent page (homepage, hub, category index) must retain broad scope that reflects all its child sections — do not narrow it to terms that belong to a specific child/section page. If child pages already target more specific terms, the parent must use broader terms that sit above them in the hierarchy. *For more information on cannibalization checks, call `read_skill("seo-cannibalization-diagnosis")`*

**Output of this stage:**

- A "Validated Keywords" list (only the keywords that passed)
- A "Removed Keywords" list with a one-line reason per removal (off-topic / wrong language / branded not present / too generic / intent mismatch)

If the validated list is empty, request/re-run keyword sourcing.

---

## 2) Keyword Sourcing

### 2.1 If the user provided keywords

1. Treat the user list as the initial candidate set.
2. Run the validation checks from Section 1.3.
3. If after validation fewer than ~10 keywords remain **and** the user expects a full-page optimization (or new page creation), trigger the Keyword Research skill as a supplement (do not replace the user's list; merge and re-validate).  For the full workflow, call `read_skill("keyword-research")`.

### 2.2 If the user did not provide keywords (Keyword Research is mandatory)

Choose the correct research path based on the user input type:

#### Case A — User input is a Page URL

1. Trigger the **Keyword Research skill (URL-based research)** for the provided URL. For the full workflow, call `read_skill("keyword-research")`.
2. Ensure research is **page-scoped**, not generic domain topic research.
3. Once research returns, validate the resulting keyword list using Section 1.3.

#### Case B — User input is a content piece (text that is or will become a page)

1. **Summarize the content first** into a precise long-tail topic statement, before research. This summary must be:
   - one or two sentences at most
   - tight scope (what it is + what it is not)
   - includes the core value and target intent
   - avoids generic words ("solutions", "things", "best practices") unless the content truly is generic
2. Trigger the **Keyword Research skill (Topic-based research)** using that topic statement as the topic input. For the full workflow, call `read_skill("keyword-research")`.
3. Once research returns, validate the resulting keyword list using Section 1.3.

#### Case C — User input is a smaller unit (paragraph, social post, FAQ answer, metadata-only)

1. Extract a short "micro-topic statement" from the unit (what is this block specifically about).
2. If the user did not provide keywords, you may:
   - either request keywords, or
   - run Topic-based keyword research on the micro-topic if the user's request implies SEO optimization is required.
3. Validate results using Section 1.3.

---

## 3) Input Normalization (What is being optimized + what outputs are required)

Before optimizing, declare both:

### 3.1 Optimization Target (object type)

Exactly one:

- **Existing Page URL** (live page optimization)
- **New Page (from content piece)** (content becomes a page)
- **Paragraph/Snippet**
- **Metadata only** (Title and/or Meta description and/or headings)
- **FAQ unit** (one or more question+answer pairs)
- **Social / engagement post**
- **Academic / research text**
- **Documentation / help article**
- **Other** (must be named)

### 3.2 Deliverable scope (what you must produce)

- If **metadata-only** → output only the requested fields, nothing else.
- If **paragraph/snippet** → rewrite only that block.
- If **new page** → must produce Title tag + Meta description + H1 + H2 set + body content.
- If **existing page URL** → must optimize existing metadata + headings + body (unless user restricted scope).
- If **FAQ** → each Q/A is optimized as a stand-alone unit (see Section 9).
- If **social** → engagement-first copy, SEO-aware term embedding (see Section 10).

---

## 4) Non-Branded Optimization Rule (Always On)

**Default:** Use non-branded keywords only, unless the user explicitly stated branded keywords should be included.

**Exception:** If branded terms already appear in the original content (title/description/headings/body), retain them where they are semantically necessary.

**Never:** Introduce new branded terms that were not present.

---

## 5) URL-Based GSC Preservation Logic (Only for Existing Page URLs)

This is mandatory when optimizing a live page URL.

### 5.1 Pull GSC data (last 30 days)

For the **specific page URL**, pull:

- Top non-branded queries by **clicks**
- Top non-branded queries by **impressions**

Exclude:

- branded queries (explicitly filtered out)
- wrong-language queries
- irrelevant queries (accidental rankings)

### 5.2 Select "must-retain" queries

Pick the **top 3 non-branded queries** that are:

- high relevance to the page scope
- correct language
- correct intent

These three must be supported in the optimized output (title/H1/H2/body as appropriate) to avoid losing existing traction.

### 5.3 Secondary opportunity logic (site-wide)

Still in last 30 days:

- Rank pages by **non-branded impressions**
- Select the **highest-impression page not yet optimized**
- Use its top relevant non-branded queries as **secondary reinforcement ideas only** if they fit the current page scope without broadening it.

---

## 6) Term Placement Priority (When metadata/headings exist)

When producing or optimizing metadata/headings, embed terms with this priority order:

1. **Title tag** (highest priority placement)
2. **H1**
3. **Meta description**
4. **H2s**
5. **Body**

Placement rule:

- If the best term is used in Title, use the next best for H1, then next for description, etc.
- Do not "double spend" the same short-tail term across multiple high-priority placements unless it already exists.

---

## 7) Exact-Term Usage

All keywords taken from the keyword list must be used:

- **Exactly as provided** in the research output
- **Without adding or removing** letters, prefixes, or suffixes
- **Without merging** with other terms
- **Without grammatical "improvements"** that change the term's surface form

The goal is to preserve the **exact surface string** that was measured for search volume and rankings.

### Special rule for prefix-attached languages (e.g., Hebrew)

In languages where function words (e.g., "and", "from", "to", "in", "the", "of") are commonly attached as **prefixes** to words, attaching such prefixes creates a **different surface term** that may have different search volume and ranking behavior.

Therefore:

- **Do not attach prefixes** (e.g., ו/מ/ל/ב/ה) to researched keywords if doing so changes the exact surface form.
- **Prefer sentence restructuring** to keep the keyword in its exact researched form.
- A prefix may be attached **only if** the sentence cannot be written clearly without it **and** the keyword appears elsewhere **at least once** in its exact researched form.

Exact-match preservation takes precedence over stylistic flow unless meaning would otherwise break.

---

## 8) Keyword Density / Repetition Rules (All previous constraints, consolidated)

### 8.1 Global embedding limits (across the whole piece)

- Each **short-tail term**: include **once** total.
- A short-tail term may appear **up to twice only if it occurs inside long-tail terms** used elsewhere.
- Each **long-tail term**: include **up to twice** total.
- If a term already appears **3+ times** in the original content: do **not reduce** it; also do **not add new repeats** beyond what already exists.

### 8.2 Per-block repetition limits (Title / Meta description / each heading / each paragraph / each FAQ answer)

- No single word repeated more than **3** times in a block (including "and/or").
- No two-word pair repeated more than **2** times in a block.
- No 3+ word phrase repeated more than **1** time in a block.

### 8.3 Embedded redundancy rule

If a short-tail term is contained inside a longer term, prefer the longer term to avoid redundancy (e.g., use "cat hair shampoo" instead of repeating "cat hair" separately).

### 8.4 Comma stuffing guardrail

Never use more than **three commas in a row** anywhere.

In meta descriptions, avoid comma-separated keyword strings; if unavoidable, allow it **once**, max **two terms**.

---

## 9) Meta Description Rules (When meta description is produced/optimized)

- Must be **≤ 156 characters**.
- Must be readable, coherent, and not keyword-stuffed.
- Must remain true to the content's promise (no misleading claims).
- Keyword blending must be natural; do not list keywords back-to-back as a "bag of terms."
- Comma-based listing allowed at most once and for at most two terms, only if needed.

---

## 10) Content-Type Adaptation Rules (So it works beyond "pages")

### 10.1 FAQ Optimization (stand-alone requirement)

For each Q/A pair:

- Optimize in the original language of the Q/A content. Never translate Q/A content to another language.
- Treat each question+answer as its own mini-page:
  - validate keywords against that Q/A scope
  - embed terms within that Q/A only
  - do not rely on other FAQs to "carry" the keyword
- Avoid repeating the same long-tail term across multiple answers unless the original already did.

### 10.2 Social / engagement content

- Primary goal is engagement and readability; SEO keyword embedding is secondary and must not harm tone.
- Still obey:
  - non-branded rule
  - exact term rule
  - repetition limits
- Prefer placing one high-value term naturally in the hook or first sentence rather than forcing multiple terms.

### 10.3 Academic / research content

- Prioritize accuracy and clarity over keyword inclusion.
- If terms do not fit naturally, do not force them; instead, embed where they align with the academic phrasing.
- If adding claims, do not invent data.

### 10.4 Documentation / help content

- Optimize for task intent and clarity.
- Keywords should align with "how-to / troubleshooting" phrasing without stuffing.

---

## 11) Trend & Fact Enrichment (Conditional, not universal)

Only apply when the output is:

- a new page
- a blog/editorial post
- a long content piece intended for publication

If applied:

- Use Google Trends to identify only highly relevant trending angles tied to the topic.
- Do not inject trends that broaden scope.
- Any data points must be real and cite trustworthy sources (no invented stats).

---

## 12) Internal Linking Recommendation

Only produce internal linking advice if:

- optimizing an existing Page URL, OR
- optimizing a full content piece that is intended to become a page.

Do not produce internal linking recommendations for:

- metadata-only edits
- paragraph-only edits
- social posts
- isolated snippets

When applicable:

- recommend exactly **one** internal page to link to
- explain why (topical cluster support + funnel logic)
- ensure it does not create cannibalization

*For the full internal linking methodology, call `read_skill("tech-seo-crawl")`*

---

## 13) Optional URL Structure Suggestions (Lowest priority)

Only suggest URL folder structure changes if:

- there is a clear, concrete reason tied to clarity or SEO architecture
- and it does not distract from the primary content + metadata optimization

Never let URL structure discussion replace content work.

*For URL management and normalization, call `read_skill("tech-seo-redirects")`*

---

## 14) Output

Every run must output three sections:

1. **Optimized Output**
   Only what the target type requires (no extras).

2. **Keyword Placement Map**
   List each embedded keyword and where it was placed:
   - Title / H1 / Description / H2 / Body / Q/A / Hook, etc.

3. **Compliance Confirmation**
   A short checklist confirming:
   - non-branded rule followed
   - exact-term rule followed
   - repetition limits followed
   - meta description length followed (if applicable)
   - GSC top-3 retention applied (if URL-based)

---

## Step Count: 6

| # | Step | Duration Estimate |
|---|------|-------------------|
| 1 | Target keyword validation | 2–3s |
| 2 | Current page content fetch | 3–5s |
| 3 | GSC query retention check | 3–5s |
| 4 | Competitor content analysis | 5–8s |
| 5 | SERP feature analysis | 3–5s |
| 6 | Output generation | 3–5s |

## Step Criticality

| Step | Critical | Fallback |
|------|----------|----------|
| Target keyword validation | Yes | Cannot proceed |
| Current page content fetch | Yes | Cannot proceed |
| GSC query retention check | No | Skip retention, note in output |
| Competitor content analysis | No | Optimize without competitor context |
| SERP feature analysis | No | Skip SERP features, note in output |

## Dashboard Template

Use `render_template("content-optimization", data)` via the silverbee-ui MCP.

| Field | Type | Description |
|---|---|---|
| `title` | string | Dashboard heading |
| `metrics.keywordsValidated` | string | Count of validated keywords |
| `metrics.keywordsPlaced` | string | Count of keywords placed |
| `metrics.gscQueriesRetained` | string | GSC queries retained |
| `metrics.densityIssues` | string | Density/repetition issues found |
| `chart.data[]` | `{placement: string, count: number}` | Keyword placements by location |
| `placements.rows` | string[][] | Keyword placement detail rows |
| `removed.rows` | string[][] | Removed keywords with reasons |

All metric values are **strings** (not numbers). Table `rows` are `string[][]` (arrays of string arrays, not objects).

For custom specs or troubleshooting, load the `show-generative-ui` skill.

---

## Output Format

When all data collection and analysis is complete, call `read_skill("seo-output-formatter")` and follow its instructions to format and present the full deliverable.
