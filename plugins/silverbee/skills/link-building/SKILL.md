---
name: link-building
description: Link building strategy and evaluation. Covers link profile assessment, link quality framework, link type taxonomy, anchor text strategy, velocity/diversification, risk signals, and dispatches to outreach and community skills for execution. Use for any link building strategy, backlink analysis, anchor text planning, link quality evaluation, link profile review, or general "build links" request.
---

# Skill: Link Building

## Title
Link Building Strategy & Evaluation

## Description
Governs link building strategy, link quality evaluation, anchor text planning, risk assessment, and profile monitoring. Dispatches to two execution skills: outreach (Tier 2 — prospecting, contact extraction, pitch drafting) and community (Tier 3 — blog comments, forums, Q&A, directories via footprint queries). This skill defines the strategic framework both operate within.

---

## Before running anything (mandatory)

Do not call any tools until you have collected required inputs.

Use `AskUserQuestion` to gather inputs in a **single call**:
```json
{
  "questions": [
    {
      "question": "What domain should I build links for?",
      "header": "Domain",
      "options": [],
      "multiSelect": false
    },
    {
      "question": "What niche or topic should the links be relevant to?",
      "header": "Niche/Topic",
      "options": [],
      "multiSelect": false
    },
    {
      "question": "What is your primary link building goal?",
      "header": "Goal",
      "options": [
        { "label": "Authority building", "description": "Increase domain rating / DR" },
        { "label": "Topical relevance", "description": "Links from topic-relevant sites" },
        { "label": "Digital PR", "description": "Earn editorial mentions and citations" },
        { "label": "Local visibility", "description": "Local directories and regional sites" }
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

**Required:** target domain.
**Optional:** target pages/linkable assets, competitor domains, specific link building goals (authority, topical relevance, digital PR, local visibility), current link profile concerns.

---

## 2) Link Profile Assessment (Current State)

Before building new links, evaluate what exists. Use Ahrefs (fallback: DataForSEO).

Pull for the target domain:
- Total referring domains and trend (growing / flat / declining).
- DR distribution of referring domains (concentration in low/mid/high authority).
- Anchor text distribution — ratio of branded, exact-match, partial-match, generic, URL, and miscellaneous anchors.
- Link type distribution — editorial, blog comments, directories, forums, social profiles, resource pages, guest posts, other.
- Follow vs. nofollow ratio.
- Top linked pages — which pages attract the most backlinks and whether those are the pages that need authority.
- Toxic/spam signals — referring domains with spam indicators, link farms, PBN patterns, reciprocal link clusters.

**Profile health classification:**
- **Healthy:** diverse anchor distribution, editorial links dominate, no significant toxic clusters, links flow to priority pages.
- **Imbalanced:** over-concentration in one anchor type, link type, or landing page. Not toxic but needs diversification.
- **At risk:** significant toxic backlinks, unnatural anchor patterns, link farm exposure. Disavow review may be needed before building new links.

Report profile assessment to user before recommending strategy.

---

## 3) Link Quality Evaluation Framework

Not all links are equal. Evaluate every link opportunity — existing or prospective — against these factors in priority order:

1. **Topical relevance:** the linking page's content must relate to the target page's topic. A high-authority irrelevant link is worth less than a moderate-authority relevant one. This is the primary quality signal.
2. **Placement context:** a link embedded naturally within body content carries more weight than a sidebar, footer, or author bio link. Links surrounded by relevant context pass stronger topical signals.
3. **Source authority:** referring domain's authority (DR/DA), organic traffic, and trust signals. Authority without relevance is weak; relevance without authority is still valuable.
4. **Link source type:** organic editorial links (earned through content merit) are highest value. Manually placed links (comments, directories, forums) are supplementary. Paid or exchanged links carry risk.
5. **Follow vs. nofollow:** dofollow links pass direct ranking signals. Nofollow links still carry value — they contribute to profile diversity, referral traffic, and brand signals. A profile with only dofollow links looks unnatural.
6. **Linking page quality:** thin content, excessive outbound links, or spam indicators on the linking page devalue the link regardless of domain authority.

---

## 4) Link Type Taxonomy

Ranked by general value. Actual value depends on execution quality and relevance — a well-placed directory link can outperform a poorly executed guest post.

### Tier 1 — Earned editorial links (highest value)
- **Organic editorial mentions:** other sites reference the target's content because it's useful, original, or authoritative. Cannot be manufactured — requires linkable assets worth citing.
- **Digital PR / linkable assets:** original research, data studies, tools, calculators, infographics, or expert commentary that earn coverage and links from publishers. The link is a byproduct of newsworthy or useful content.
- **Link bait:** content designed to attract natural links — can be informational, visual, interactive, or provocative. Must be genuinely valuable, not gimmick-driven.

### Tier 2 — Proactive outreach links (high value when executed well)
- **Resource page placements:** links from curated resource lists on relevant sites.
- **Guest posts:** authored content on relevant third-party sites with editorial standards. The host site must have real audience and editorial review — guest post farms are Tier 4.
- **Broken link replacements:** replacing dead links on relevant pages with the target's equivalent content.
- **Expert roundups / interviews:** contributing expertise to multi-source content.
- **Unlinked brand mentions:** converting existing mentions of the brand into linked references.

*For the full prospecting and outreach workflow, call `read_skill("link-building-outreach")`*

### Tier 3 — Supplementary / community links (supporting value)

Blog comments, forum participation, Q&A contributions, niche directory listings, social bookmarks, and social media profile links. Lower individual value but essential for profile diversity. The agent discovers placement opportunities using footprint queries — Google search patterns combining platform identifiers, posting indicators (multilingual), and topic terms.

*For the full community link building methodology — footprint queries, multilingual discovery, qualification criteria, and contribution guidelines — call `read_skill("link-building-community")`*

### Tier 4 — Avoid (risk outweighs value)
- Link farms, PBNs, link exchanges/reciprocal schemes.
- Paid links without nofollow/sponsored attributes.
- Guest post farms (sites that exist solely to sell guest posts with no editorial standards or real audience).
- Automated link placement (mass blog commenting, forum spam, bookmark spam).
- Irrelevant directory submissions with no editorial review.

---

## 5) Anchor Text Strategy

Anchor text distribution must appear natural. Over-optimization of any single type triggers algorithmic penalties.

**Target distribution ranges** (approximate — vary by niche competitiveness and existing profile):
- **Branded anchors** (brand name, brand + keyword): 30–50% of total.
- **URL/naked URL anchors:** 10–20%.
- **Generic anchors** ("click here", "learn more", "this article"): 10–15%.
- **Partial-match** (keyword variation within a natural phrase): 10–20%.
- **Exact-match** (target keyword as the full anchor): 3–10%. The most dangerous to over-optimize.
- **Miscellaneous / long-tail / contextual phrases:** remainder.

**Rules:**
- Assess the current anchor distribution (Section 2) before planning new anchors. If exact-match is already over-represented, shift new links toward branded and generic.
- Distribute anchor types across link types. Do not concentrate exact-match anchors in one link type.
- Distribute across landing pages. Do not point all new links to the same URL. Spread across priority pages based on where authority is most needed.
- Anchor text must read naturally in context. Forced keyword insertion into anchor text is detectable and counterproductive.

---

## 6) Velocity & Diversification

**Velocity:** link acquisition must be steady, not spiky. A sudden burst of links followed by silence is an unnatural pattern. Plan link building as ongoing activity — consistency over volume.

**Diversification rules:**
- Mix link types — do not rely on a single acquisition method. A profile built entirely on guest posts or entirely on directories looks manufactured.
- Mix authority levels — a natural profile includes links from high, mid, and lower authority sites. All-high-DR profiles are uncommon for most domains.
- Mix follow and nofollow — a natural profile contains both. Do not pursue only dofollow links.
- Mix landing pages — distribute links across pages that need authority, not just the homepage.
- Adjust strategy based on competitor link profiles. If competitors have heavy editorial link profiles, blog comments and directories alone will not close the gap.

---

## 7) Risk Signals & Avoidance

Flag and avoid:
- **Anchor over-optimization:** exact-match anchor ratio significantly above niche norms.
- **Link farms / PBNs:** networks of low-quality sites interlinking and selling placements. Indicators: no organic traffic, thin/template content, excessive outbound links, unrelated topic coverage.
- **Reciprocal link schemes:** systematic "I link to you, you link to me" patterns.
- **Paid links without proper attributes:** links acquired through payment must carry rel="nofollow" or rel="sponsored".
- **Sudden velocity spikes:** acquiring a large volume of links in a short window without a corresponding content or PR event to justify it.
- **Toxic backlink accumulation:** if the profile assessment (Section 2) identifies significant toxic exposure, recommend a disavow review before investing in new link building.

---

## 8) Execution Dispatch

This skill defines strategy. Execution lives in two separate skills. Route based on what the user needs — default to both unless the user scopes to one.

**Route to outreach** when the goal is earning editorial links from third-party sites — backlink gap prospecting, resource page placements, guest posts, broken link replacements, unlinked brand mentions. These require identifying prospects, qualifying them, extracting contacts, and drafting pitches.
→ Call `read_skill("link-building-outreach")`

**Route to community** when the goal is building profile diversity through direct placements — blog comments, forum participation, Q&A contributions, niche directories, social bookmarks. These use footprint queries to discover relevant platforms where the user can place links by contributing content.
→ Call `read_skill("link-building-community")`

**Route to both** when the user asks to "build links" or "start link building" without specifying a method. A complete link building campaign needs Tier 2 (outreach) and Tier 3 (community) working together — outreach for high-value editorial links, community for diversity and supporting signals. Present both as part of the strategy.

Both execution skills inherit:
- The link quality framework from Section 3 (qualification criteria).
- The anchor text strategy from Section 5 (anchor recommendations).
- The risk signals from Section 7 (rejection criteria).
- The diversification rules from Section 6 (mix of link types).

---

## 9) Link Profile Monitoring

Ongoing — not one-time.

- Track referring domain count and trend (monthly cadence minimum).
- Monitor for new toxic backlinks (quarterly review or when rankings drop unexpectedly).
- Track anchor text ratio drift — if distribution shifts toward over-optimization, adjust strategy.
- Monitor competitor link acquisition to identify new opportunities and benchmark velocity.
- Check for link losses — high-value referring domains that stop linking. Reclaim or replace.

Use Ahrefs (fallback: DataForSEO) for monitoring. GSC backlink data is supplementary but incomplete.

---

## 10) Guardrails

- Never recommend link building without first assessing the current profile (Section 2). Building on a toxic foundation makes things worse.
- Never recommend a link type or anchor pattern that conflicts with the current profile's needs. If exact-match is already over-optimized, do not add more.
- Topical relevance is a hard requirement. High authority with no relevance is not a quality link.
- Never recommend link schemes, paid links without proper disclosure, or any tactic in Tier 4.
- Anchor text distribution targets are guidelines, not rigid rules. Adjust based on niche norms and existing profile.
- Every link building recommendation must connect to a specific page that needs authority. Do not recommend link building without identifying target landing pages.
- Link building without linkable assets is ineffective. If the target domain lacks content worth linking to, recommend content development before outreach.
- Do not conflate link quantity with link quality. 5 relevant editorial links outweigh 50 irrelevant directory submissions.
- Report profile assessment before strategy recommendations. The user needs to understand the current state before planning next steps.

---

## Dashboard Template

Use `render_template("link-building", data)` via the silverbee-mcp MCP.

| Field | Type | Description |
|---|---|---|
| `title` | string | Dashboard heading |
| `metrics.targetDomains` | string | Number of target domains |
| `metrics.opportunities` | string | Total link opportunities |
| `metrics.authorityGain` | string | Projected authority gain |
| `metrics.priorityWins` | string | Priority quick wins count |
| `chart.data[]` | array of `{category, count}` | Opportunities by category (category: string, count: number) |
| `prospects.rows` | string[][] | Link prospects table rows |
| `timeline.rows` | string[][] | Implementation timeline rows |

All metric values are **strings** (not numbers). Table `rows` are `string[][]` (arrays of string arrays, not objects).

For custom specs or troubleshooting, load the `show-generative-ui` skill.

---

## Output Format

When all data collection and analysis is complete, call `read_skill("seo-output-formatter")` and follow its instructions to format and present the full deliverable.
