---
name: keyword-research
description: Keyword research for URL or topic inputs with scope locking. Ahrefs volume/KD/CPC, conditional GSC/Ahrefs ranking validation, SERP validation, mandatory cannibalization detection, intent classification, structured table output.
---

# Skill: Keyword Research

## Title
SEO Keyword Research

## Description
End-to-end keyword research for URL or topic inputs. Scope locking, Ahrefs volume/KD/CPC, ranking checks, SERP validation, cannibalization detection, intent classification. Structured table output.

---

## Before running anything (mandatory)

Do not call any tools until you have collected required inputs.

Use `AskUserQuestion` to gather inputs in a **single call**:
```json
{
  "questions": [
    {
      "question": "What keyword(s) or page URL should I research?",
      "header": "Keyword/URL",
      "options": [],
      "multiSelect": false
    },
    {
      "question": "What time range should I use for trend data?",
      "header": "Time Range",
      "options": [
        { "label": "Last 3 months", "description": "Recent demand signals" },
        { "label": "Last 12 months", "description": "Full seasonal cycle" },
        { "label": "Last 5 years", "description": "Long-term trend view" }
      ],
      "multiSelect": false
    },
    {
      "question": "What is the primary target country/market?",
      "header": "Country",
      "options": [
        { "label": "United States", "description": "en-US market" },
        { "label": "United Kingdom", "description": "en-GB market" },
        { "label": "Global", "description": "No country restriction" },
        { "label": "Other", "description": "I'll specify in chat" }
      ],
      "multiSelect": false
    }
  ]
}
```

After collecting inputs, confirm them in a short text message and **wait for the user's go-ahead** before making any tool calls.

---

## Tool execution

### Auth gate (mandatory — run before any data fetching)

Before starting data collection, verify that tool connections are live:

1. Call `list_available_apps`.
2. **If it returns ANY error** (511, "Tool execution failed", timeout, anything):
   Stop immediately. Follow the supervisor skill's **"Tool call errors"** section.
   In short: scan the error for a URL. If found, show it. If not, show the
   fallback URL `https://silverbee-us.apigene.ai/sign-in` and paste the raw error.
   **You MUST always show a clickable URL. No exceptions. Never respond to an
   error without a link.**
3. **If it returns an empty list:** Tell the user no data sources are connected and
   they need to link GSC/Ahrefs/etc. at https://silverbee-us.apigene.ai/sign-in.
4. **If it succeeds with apps listed:** Remember the list. Before every data step,
   check if the preferred app is available. If not, use the supervisor's fallback
   chain (GSC → Ahrefs → DataForSEO) silently — do NOT ask the user to connect
   an app when an alternative is available. Only ask if ALL fallbacks are exhausted.

Do **not** skip this step. Do **not** call `run_action` until the auth gate passes.

### Data fetching

**Before calling any tool**, output a plain-text kickoff message to the user:
> "🔍 Starting keyword research for **[target]**. Pulling data from Ahrefs, GSC, and DataForSEO — this takes 3–6 minutes. I'll update you after each step."

Use this pattern for all data fetching:
1. `search_actions(query)` or `list_actions(app_name)` — find the right operation
2. `run_action(app_name, operation_id, input)` — execute

**MANDATORY — parallel execution:** Use `run_multi_actions` to batch independent calls. Never call `run_action` in a loop one-by-one. When fetching volume/KD/CPC for multiple keyword groups, send them all in a single `run_multi_actions` call. Sequential `run_action` calls for independent queries are a performance bug. On any app-specific error, try the fallback chain (see supervisor "Step 3") before stopping. On connection/auth errors (all tools failing), follow the supervisor's "Tool call errors" section.

**After each major phase**, output a status line before the next tool call:

| After this phase | Output this line |
|---|---|
| Scope / scrape | `✓ Scope locked — [one-line summary]` |
| Ahrefs seed pull | `📊 Got [N] keyword candidates from Ahrefs. Enriching with volume/KD/CPC...` |
| Volume / KD / CPC enrichment | `✓ Metrics collected for [N] keywords. Pulling rankings...` |
| Rankings (GSC or Ahrefs) | `✓ Rankings pulled. Running SERP validation for top keywords...` |
| SERP validation | `✓ SERP data collected. Running cannibalization check...` |
| Cannibalization check | `✓ Cannibalization check done. Building dashboard...` |

Never skip these lines. They are the only feedback the user gets during a multi-minute operation.

---

## 1) Input

**Required:** {Page URL or Topic/Seed list}.

All operational parameters including domain, language, and market locale must be inferred during execution using tool-derived signals unless explicitly provided by the user or already available in the context.

---

## 2) Scope Definition

- **URL input** → use Scraper to extract page HTML + visible text, titles/meta, H1–H3, primary entities/products, implied intent, primary domain, primary language signals, and regional targeting indicators; Use Google Search Console (and fallback to Ahrefs if the user is not yet connected to GSC for the scoped URL domain) to determine the primary target country (where more organic traffic is coming from). Always normalize ISO country codes to full country names when listing countries in tables or summaries (e.g., "United States" not "US", "Georgia" not "GEO"). This does not apply to the Local Volume column header, which must retain the ISO code. Output a mandatory 3–7 bullet "scope lock". The Scope Lock becomes binding and cannot expand later (what the page is *and is not* targeting).

- **Topic input** → Use Ahrefs to identify dominant geographic market, and dominant language. use **Google Trends** for demand confirmation, and to identify keywords with stable or rising interest signals; keep only queries/entities that are directly about the topic and show rising/stable interest; drop generic/adjacent themes. when a seed keyword list is provided (instead of a single topic), treat it as the initial scope anchor; validate and retain all seed keywords that pass scope relevance, then proceed with Ahrefs and Google Trends as above.

---

## 3) Seed Set Creation (strict relevance)

Use **Ahrefs Keywords Explorer** to generate candidates, but **keep only keywords that clearly map to the locked scope and intent** (exclude "nearby/adjacent" suggestions even if volume is high). Exclude branded keywords (containing any brand name or trademarked term) unless the user explicitly requests them. When a user-provided seed list exists, include all scope-relevant seed keywords verbatim before Ahrefs expansion; they count toward minimum coverage.

---

## 4) Expansion to Minimum Coverage

Use **Ahrefs Search Suggestions** to add strictly relevant autocomplete + question variants.

Expansion must continue until the dataset contains at least 50 strictly relevant keywords or until all highly relevant keyword possibilities are exhausted. If 100 or more highly relevant keywords exist, include all of them without caps. Under no condition may the dataset contain fewer than 50 keywords unless documented exhaustion occurs. Iterate Ahrefs expansion (tighter scope-based modifiers, synonyms, singular/plural, question forms, use-case qualifiers) until either **≥ 50** or **all highly relevant possibilities are exhausted**.

If **100/200+** highly relevant terms exist, include all of them.

---

## 5) Volumes, KD, CPC

For **every keyword**, capture:

- Local Volume (ISO)
- Global Volume
- KD
- CPC

Record the **tool source and pull date** for each metric (store per-row, not as a general note).

Metric formatting rules are mandatory. Metric cells must contain numeric values only. Locale must appear only in the Local Volume column header and must never be repeated inside cells. Annotations or notes must never appear inside metric cells. If Global Volume is unavailable, record the value as "N/A".

Keyword strings must be recorded verbatim from the source tool. No case changes, rephrasing, merging, truncation, or reordering. Near-duplicates differing by plural, word order, or punctuation remain separate rows. Exclude any keyword with 0 Local Volume from the final output.

---

## 6) Current Rank (deterministic rule)

Determine Current Rank using Google Search Console when the tool is connected or ranking data already exists in the context. If GSC is unavailable, use Ahrefs ranking data. Apply URL-scoped rankings when input is a URL and domain-scoped rankings when input is a topic. Standardize output to #{RANK} when ranking exists or "-" when not ranking.

**URL input only.** When input is a topic or seed list with no associated domain, Current Rank cannot be determined — record "-" for all rows and skip rank lookups.

- If **GSC is available**, pull rankings from **Google Search Console**: **URL-scoped** when input is a URL, **domain-scoped** when input is a topic.
- If **GSC is not available**, pull "current rank" from **Ahrefs** using the same scoping rule (URL vs domain).
- Standardize output to **#{RANK} or -** ('-' for not ranking).

**URL mismatch flag (URL input only):** When the domain ranks for a keyword but on a different URL than the one being researched, flag as **"Ranks via {ranking URL}"** in the Current Rank cell alongside the position. This is not cannibalization — it signals the keyword has domain traction but not on the target page.

---

## 7) SERP Validation

Use **Ahrefs SERP Overview** to populate:

- **Top SERP URL** (the leading result you're benchmarking against)
- **SERP Type** must be classified as Informational, Commercial Investigation, Navigational, or Transactional; note presence of AI Overview / local pack / shopping if applicable, but keep SERP Type concise and record AI Overview, Local Pack, or Shopping features as contextual notes without altering SERP Type classification)

---

## 8) Cannibalization Check (mandatory per top keywords on URL input only)

**Applies to URL input only.** When input is a topic or seed list with no associated domain, skip this section entirely.

Before finalizing, for the top 20 keywords (priorotized by ranked terms at decending search volume order, and then non-ranked by volume), run:

1. 'site:{domain} "{keyword}"' (Google Search) to detect multiple relevant pages, and
2. Verify competing ranking pages using GSC when available, otherwise use Ahrefs ranking URLs to list ranking pages (or Ahrefs top ranking URLs if GSC unavailable).

**Output Pass/Fail:**

- **Pass** = zero or one dominant internal ranking page
- **Fail** = multiple competing pages → flag as **"Cannibalization risk – consolidate first."**

---

## 9) Keyword Grouping Rules (no flat dumps)

- Assign **Intent** (informational / commercial investigation / navigational / transactional).
- **Never** output an unstructured list of >20 keywords; group into clusters in the output (filters + grouping fields).

---

## 10) Category + Sub-Category Generation (density-based constraints)

Compute meaningful token/phrase frequency across the finalized keywords (exclude stopwords like "and/or/for," etc.).

Produce short labels based on core repeating value-terms.

Density constraints are mandatory and must **enforce:** ≤ 1 Category and ≤ 2 Sub-Categories per 10 keywords (so **50 keywords → max 5 Categories + 10 Sub-Categories**).

---

## 11) Output Tables

Primary output must be returned as structured tables inside the response.

Output must begin with an Executive Summary summarizing Scope Lock results, inferred market locale, demand validation outcomes, intent distribution patterns, SERP competitiveness trends, cannibalization risk findings, and keyword opportunity overview.

Table structure:

### Keywords Table

One keyword per row with these columns in this exact order:

| Keyword | Category | Sub-Category | Intent | Local Volume (ISO) | Global Volume | KD | CPC (USD – Commercial Intent) | Current Rank | Top SERP URL | SERP Type |

- ISO must appear only in the Local Volume column header. Numeric cells must contain numeric values only. One keyword per row is mandatory. All collected keywords must be included.
- Validation must exist for every keyword and cannot be skipped.

### Validation Table (URL input only)

(to satisfy missing mandatory checks without changing Keywords table columns; omit this table for topic/seed list input)

| Keyword | Cannibal Check (Pass/Fail) | Competing URLs | Source (Tool) | Data Pull Date | Notes/Action (e.g., consolidate first) |


## 12) Global Execution Guardrails

**Enforce:** Scope Lock relevance, ≥50 keyword minimum or documented exhaustion, verbatim keyword preservation, metric normalization, deterministic ranking logic (URL input only), mandatory cannibalization checks (URL input only), clustering, density-based category limits, exact column order, full dataset inclusion.

**Reject:** off-scope keywords regardless of volume, branded keywords (unless explicitly requested), zero-volume keywords, partial datasets, altered keyword strings, missing Global Volume when available, annotations inside metric cells, flat keyword dumps, skipped validation steps, SERP verification omissions, rank/cannibalization lookups without an associated domain.

- *For the full cannibalization check workflow, call `read_skill("seo-cannibalization-diagnosis")`*

---

## Output Format

When all data collection and analysis is complete, call `read_skill("seo-output-formatter")` and follow its instructions to format and present the full deliverable.
