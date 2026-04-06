---
name: ahrefs-brand-radar
description: >
  Plans Ahrefs Brand Radar API usage for AI visibility data collection — covering
  brand mentions, cited pages, and cited domains across AI engines. Use when the user
  asks about brand presence in AI answers, share of voice across LLMs, queries that
  surfaced their brand, or sources cited alongside their brand. Do NOT use when the
  user supplies a specific prompt or question to test — route those to DataForSEO.
---

# Skill: Ahrefs Brand Radar Planning

Plan Ahrefs Brand Radar API calls to retrieve where a brand appears across AI-generated answers
and which sources LLMs cite alongside it.

---

## Step 1 — Confirm This Is the Right Tool

Brand Radar is a **single-engine, brand-driven API**: it takes a brand name as input, identifies
AI responses mentioning the brand, and surfaces the associated queries — one AI engine per call.
It does not accept queries as input.

If the user has provided a **specific prompt or question to test against an LLM**, route to
DataForSEO and stop.

---

## Step 2 — Confirm the Brand Name

- If business context already contains a confirmed brand name, use it.
- If it is unclear or missing, ask: *"Which brand should I analyze?"*

Do not proceed until the brand is confirmed. Do not infer the brand from a domain.

---

## Step 3 — Determine Scope

**Full audit** — user requests general AI visibility with no specific engine named:
- Plan all endpoints across all supported AI engines
- Generic audits must be executed as multiple calls — never one combined call

**Scoped audit** — user names a specific engine or subset:
- Plan only the calls required for that request
- Do not expand scope

---

## Step 4 — Plan Calls

### Rule: one data source per call

Brand Radar accepts exactly **one** `data_source` per call. Never combine values.

Allowed values: `google_ai_overviews` · `google_ai_mode` · `chatgpt` · `gemini` · `perplexity` · `copilot`

✓ Correct: `data_source = chatgpt` / `data_source = gemini` (separate calls)  
✗ Incorrect: `data_source = chatgpt, gemini` (invalid)

### Recommended analysis order (per engine)

1. `list-ai-responses` — queries where the brand appeared in an AI-generated answer
2. `list-cited-pages` — URLs cited by the LLM in those answers — **always set `limit=100`** (API default is 1000; leaving it unset on large brands will produce context-breaking output)
3. `list-cited-domains` — domains cited by the LLM in those answers

---

## Step 5 — Produce Output

Always deliver all four tables. Include only engines that were called.

### Table 1 — Mention Summary by Engine

| AI Engine | Total Mentions | Sample Queries |
|-----------|---------------|----------------|
| ChatGPT | N | query 1, query 2… |
| Gemini | N | … |
| Perplexity | N | … |
| Google AI Overviews | N | … |
| Google AI Mode | N | … |
| Copilot | N | … |
| **Total** | **N** | |

### Table 2 — Queries Where Brand Appears

Sort descending by Mention Count.

| Query | Engines Mentioning Brand (aggregated) | Mention Count |
|-------|---------------------------------------|---------------|
| [query text] | ChatGPT, Gemini | 2 |

### Table 3 — Cited Pages

URLs cited by LLMs in answers that mentioned the brand. Sort descending by Times Cited.

| Cited URL | Times Cited | AI Engine(s) |
|-----------|-------------|--------------|
| https://example.com/page | N | ChatGPT, Perplexity |

### Table 4 — Cited Domains

Domain-level aggregation of LLM sources. Sort descending by Times Cited.

| Cited Domain | Times Cited | AI Engine(s) |
|--------------|-------------|--------------|
| example.com | N | … |
