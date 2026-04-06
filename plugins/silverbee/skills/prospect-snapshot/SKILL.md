---
name: prospect-snapshot
description: Single-page evidence brief for prospect outreach using only public data. Surfaces high-impact AI visibility gaps, organic keyword gaps vs competitors, and traffic trajectory signals. Framed as business impact, not an audit. Use for prospect audit, prospect teaser, cold outreach prep, lead gen audit, or any quick assessment of a domain the user doesn't own or have access to.
---

# Skill: Prospect Snapshot

Selective single-page brief that surfaces findings most likely to make a prospect feel a gap immediately. Not an audit — a provocation designed to open a conversation.

**This skill runs exactly three analyses** (Sections 4a–4c) and produces a brief from their findings. It does not run a technical SEO audit, crawl check, CWV test, redirect analysis, robots.txt review, schema validation, or any other site health assessment. Those belong in `technical-seo` and its micro-skills — not here. If an analysis is unavailable (tool not connected, data not returned), silently skip it and produce findings from the remaining analyses. Never substitute with a technical audit. Never mention in the output what couldn't be checked.

---

## 1) Input

**Required:** prospect domain.
**Optional:** known competitors, industry/niche context, target length, finding count.

---

## 2) Site Context

All data from public sources — no access required.

Scrape the homepage **to understand the business only** — not to audit the site. Derive:
- Precise long-tail niche (specific positioning, not broad category).
- Primary competitive region.
- Core offering in plain language.

Do not assess, report, or store any technical signals from the scrape (load time, meta tags, schema, redirects). The scrape exists solely to determine what the prospect does and who they compete with.

If unclear from homepage, check about page and meta descriptions. State assumptions if needed.

---

## 3) Competitor Identification

Pull Ahrefs organic competitors. Take the top 2–3 by keyword overlap in the same vertical. Competitors must be names the prospect would recognize as direct competition — discard aggregators, directories, platforms. If the user provides competitors, use those.

---

## 4) Finding Selection

Run exactly these three analyses — no others. Include only findings that meet threshold. Never pad. If an analysis is unavailable, silently skip it and work with the remaining analyses.

### 4a) AI Visibility Gap

Call `read_skill("ai-visibility")` — prompt-level competitor gap analysis only.

Derive one niche question from site context. Submit to each AI engine via dataforseo-ai-visibility. Retrieve Competitor Presence Matrix.

**Threshold:** prospect absent from 3+ of 5 engines while a competitor appears in 3+. Otherwise skip.

### 4b) Organic Visibility Gap

Call `read_skill("seo-gap-analysis")` — keyword/topic coverage gap only.

Identify the highest-impact organic gaps where competitors outperform the prospect. Two variants — use whichever produces the stronger finding:
- **Zero presence:** keyword clusters where 2+ competitors rank top 5 and the prospect doesn't rank at all.
- **Wasted effort:** keywords where the prospect ranks poorly (positions 15+) while a competitor holds top 3. This can be a stronger provocation — the prospect is already investing effort and losing.

Then call `read_skill("keyword-research")` to surface the specific highest-traffic keywords within those gaps — the brief needs named keywords with search volume, not abstract cluster descriptions.

The finding must be concrete: "[Competitor] ranks #N for '[specific keyword]' ([X] monthly searches) — [prospect domain] doesn't rank at all." Or: "[Prospect domain] ranks #22 for '[specific keyword]' ([X] monthly searches) — [Competitor] holds #2." Not: "Competitors capture a keyword cluster you're missing."

**Threshold:** 500+ estimated monthly visits for the cluster. Below that, use the strongest available gap but flag the lower volume.

### 4c) Trajectory Signal (conditional)

Call `read_skill("drop-analysis")` — public signals only: Ahrefs historical traffic trend and ranking volatility.

**Threshold:** 20%+ traffic drop over 6 months, or sustained downward trend over 3+ months. If stable or growing, skip entirely. Absence of decline is not a finding.

### Ranking

Prioritize findings where: (1) the gap is quantifiable, (2) a named competitor captures what the prospect doesn't, (3) the prospect can understand the impact without SEO knowledge. Tiebreaker: prefer the finding the prospect is least likely to have seen before.

---

## 5) Output

### Defaults

User instructions override all defaults below.

- **Length:** ~400 words. Never pad to reach any target — but extend naturally if findings warrant it.
- **Findings:** default 2–3, but driven by what the data surfaces. If only one finding meets threshold, deliver one. If four or five strong findings emerge, include them all — more genuine provocation points strengthen the brief. If the user requests a specific count, expand or narrow the analysis scope accordingly: pull additional keyword clusters from the gap analysis, test additional questions through AI engines, or adjust selection thresholds.

### Format

- No audit-category headers. Frame every finding as what the prospect is losing or missing, not what's technically wrong.
- No status tables. Never produce rows of checks with "Healthy" / "Needs improvement" / "Gap" statuses. This is a narrative brief, not an audit grid.
- No implementation steps, fix instructions, or "next steps" checklists. One sentence of recommendation max per finding. The "how" is the paid engagement.
- No raw data: no keyword lists, crawl stats, backlink counts, CWV scores, redirect chains, competitor tables.
- No methodology disclosure. Findings are observations, not process outputs.
- No positive findings. If something is working fine, do not mention it. The brief contains only gaps the prospect didn't know they had.

### Structure

**Opening** (1 sentence) — "[Domain] competes in [niche] against [Competitor A] and [Competitor B]."

**Findings** — strongest first. Each: one data point, one competitor name, one business implication. Each finding must present a different angle — never two findings that say the same thing differently.

**Trajectory** (only if threshold met) — framed as urgency connecting to findings above, compounding their impact.

**Closing** (1 sentence) — a statement of fact about what's winnable. Not a recommendation, not a pitch. Leave the prospect wanting the how.

### Tone

- Peer-to-peer — sharp colleague, not vendor report.
- No hedging. State findings as facts with numbers.
- No flattery. The brief is about gaps, not strengths.
- No manufactured urgency ("you need to act now", "this is critical"). The data creates its own urgency — manufactured urgency undermines credibility.
- No jargon. Every finding must work as: "[Competitor] gets [thing you want] from [place you're absent]." If it can't be framed that way, drop it.

### Quality Check

Apply before finalizing output: does every finding name a specific competitor, cite a specific number, and describe a business impact a non-SEO reader would understand? If any finding is generic ("you're missing opportunities"), technical ("CLS exceeds threshold"), or padded (restates another finding differently) — cut or rewrite it.

---

## 6) Guardrails

- **Only the three prescribed analyses (4a–4c) produce findings for this brief.** Do not run technical audits, CWV checks, redirect tests, robots.txt reviews, schema validation, crawl assessments, or any site health checks. If an analysis is unavailable, silently skip it — never substitute with a technical audit, never mention in the output what couldn't be checked.
- User instructions override defaults on length, finding count, and format.
- Never pad. Every sentence earns its place.
- Never fabricate or inflate findings to fill a count.
- Include all findings that meet threshold — do not cap artificially if the data surfaces more strong findings than the default range.
- Never include findings that require SEO vocabulary. Reframe or drop.
- Never report healthy signals or passing checks. The brief contains gaps only — no "Healthy" statuses, no "what's working well." Strengths belong in the paid engagement.
- Never produce tables of check results with status columns. This is a narrative brief, not an audit report.
- Trajectory signal is conditional. Do not force it to reach a finding count.
- Competitor names must be recognizable to the prospect.
- Every number must come from tool output. Never estimate or inflate.
