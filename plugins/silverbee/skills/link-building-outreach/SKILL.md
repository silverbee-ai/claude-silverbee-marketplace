---
name: link-building-outreach
description: Systematic link building prospecting and outreach preparation. Identifies qualified link opportunities via backlink gap analysis, resource page discovery, and broken link detection. Qualifies prospects, extracts contacts, drafts personalized outreach. Not for backlink audits or disavow work.
---

# Skill: Link Building Outreach Prospecting

## Title
Link Building Prospecting & Outreach

## Description
Identifies, qualifies, and prepares outreach for link building opportunities. Runs backlink gap analysis, discovers resource pages and guest post targets, detects broken link opportunities, qualifies prospects by authority and topical relevance, extracts contacts, and drafts personalized outreach. Minimum viable analysis requires Ahrefs or a comparable backlink data source + Google Search.

---

## 1) Input

**Required:** target domain or URL(s).
**Optional:** competitor domains (if not provided, the agent identifies them), target pages/linkable assets on the target domain, DR/authority thresholds, topical focus areas.

Determine which tools are available. Fallback chain for backlink data: Ahrefs → DataForSEO. If neither is available, the skill can still run resource page and guest post discovery via Google Search, but backlink gap analysis and DR qualification are skipped — note reduced prospect quality to the user.

---

## 2) Competitor Identification & Backlink Gap

**If competitors not provided:** use the active backlink data source to identify the top 3–5 organic competitors for the target domain (domains ranking for similar keyword sets with stronger backlink profiles).

**Backlink gap analysis:** identify referring domains that link to one or more competitors but not to the target domain. This is the primary prospect pool — these domains are already proven linkers in the niche.

**Filter the gap results:**
- Remove irrelevant domains (directories, forums, social profiles, press release wires, PBNs, link farms).
- Remove domains below DR threshold (default: DR 20 unless user specifies otherwise).
- Remove domains with no organic traffic (likely dead or penalized).

**Report to user before proceeding:** number of gap domains found, number after filtering, top 20 prospects ranked by DR with linking page URLs, which competitors they link to and with what context (anchor text, linking page topic).

---

## 3) Opportunity Discovery

Run in parallel with or after section 2. These methods find prospects outside the backlink gap.

**Resource page discovery:** use Google Search to find resource pages, link roundups, and curated lists in the target's niche. Search for queries combining the target's topic with resource page indicators ("resources", "useful links", "recommended tools", "best [topic] resources", "[topic] roundup").

**Guest post discovery:** use Google Search to find sites in the target's niche that accept guest contributions. Search for queries combining the target's topic with guest post indicators ("write for us", "contribute", "guest post guidelines", "submit an article"). Validate that the site is editorially legitimate (not a guest post farm).

**Broken link discovery:** for high-value prospects identified in section 2 or above, use the Scraper to check the linking pages for broken outbound links. A broken link pointing to content the target domain can replace is a high-conversion outreach angle.

**Deduplication:** merge all prospects from sections 2 and 3. Remove duplicates. Tag each prospect with its source (backlink gap, resource page, guest post, broken link, roundup).

---

## 4) Prospect Qualification

Every prospect must pass qualification before entering the final list. No unqualified prospects in the output.

**Mandatory checks per prospect:**

- **Topical relevance:** does the prospect's content align with the target domain's niche? Scrape the prospect page (or a sample of recent content) and verify topical alignment. Irrelevant domains are rejected regardless of DR.
- **Authority (when backlink data available):** DR, organic traffic estimate, referring domain count. Flag but don't auto-reject low-DR sites if topical relevance is strong (niche-specific sites often have lower DR but high link value).
- **Link viability:** is the linking page a live, indexable page? Does it accept outbound links? Is there a clear placement opportunity (resource list, editorial mention, broken link replacement, guest post)?
- **Spam signals:** check for excessive outbound links on the prospect page, sitewide link selling indicators, thin/scraped content. Reject if present.

**Qualification result per prospect — binary:**
- **Qualified:** passes relevance, viability, and spam checks.
- **Rejected:** fails one or more checks. Record the reason.

**Report to user before proceeding:** total prospects evaluated, number qualified, number rejected (with rejection reason distribution), qualified prospect list with DR, traffic estimate, source type, and link opportunity type.

---

## 5) Contact Extraction

For qualified prospects only.

Use Scraper to extract contact information from each prospect's site:
- Author/editor name and email from the relevant page, about page, or contact page.
- Social profiles if email is not available.
- Contact form URL as last resort.

**Contact quality hierarchy:** named person email > generic team email (editor@, content@) > contact form > social DM. Prioritize the highest quality contact available.

If no contact information is extractable, flag the prospect as "no contact found" — still include in the list but mark as requiring manual research.

**Report to user before proceeding:** number of prospects with direct email, number with generic email, number with contact form only, number with no contact found.

---

## 6) Outreach Preparation

Draft personalized outreach for each qualified prospect. The outreach angle must match the prospect type and opportunity.

**Angle matching:**
- **Backlink gap prospect:** reference the competitor content they already link to, position the target's content as a stronger/complementary resource.
- **Resource page prospect:** reference their resource page specifically, explain what the target's content adds to their list.
- **Guest post prospect:** propose a specific topic relevant to their audience, reference their editorial guidelines if found.
- **Broken link prospect:** identify the specific broken link on their page, offer the target's content as a replacement.
- **Roundup prospect:** reference the specific roundup, position the target's content as a fit for their next edition.

**Per outreach draft:**
- Subject line.
- Personalized opening (reference something specific about the prospect's site or content — not generic flattery).
- Value proposition (what the target's content offers their audience).
- Specific ask (link placement, guest post, broken link swap).
- Keep under 150 words. No fluff.

Output as structured text.

---

## 7) Output

**Final deliverable — structured prospect list:**

| Prospect Domain | DR | Traffic Est. | Source Type | Opportunity Type | Linking Page URL | Contact | Contact Type | Outreach Angle | Qualification Status |

Return two structured tables in the output:

Table 1 — Qualified Prospects  
Table 2 — Rejected Prospects (include rejection reason)

Outreach drafts delivered separately per prospect.

Include a summary section with: total prospects found, qualified count, rejection rate, breakdown by source type, breakdown by opportunity type, contact coverage rate.

---

## 8) Tool Usage

| Tool | Role | Required |
|---|---|---|
| **Ahrefs** | Backlink gap analysis, competitor identification, DR/traffic data, referring domain prospecting. | Preferred. Fallback → DataForSEO. |
| **DataForSEO** | Backlink gap fallback, DR/traffic data. | Fallback if Ahrefs unavailable. |
| **Google Search** | Resource page discovery, guest post target discovery, niche-specific prospect finding. | **Mandatory.** |
| **Scraper / Web Fetch** | Prospect page content analysis, contact extraction, broken link detection, topical relevance validation. | **Mandatory.** |

Minimum viable execution: Google Search + Scraper. Backlink gap analysis and DR qualification require Ahrefs or DataForSEO.

---

## 9) Execution Guardrails

1. **Never output unqualified prospects.** Every prospect in the final list must pass section 4 checks.
2. **Topical relevance is a hard filter.** High DR with no relevance = rejected.
3. **Never fabricate contact information.** If contact is not found, say so.
4. **Never use generic outreach.** Every draft must reference something specific to the prospect. If there's nothing specific to reference, flag the prospect for manual outreach.
5. **Deduplicate across all sources.** No prospect appears twice in the output.
6. **Report after each section.** Do not batch findings.
7. **Do not inflate prospect counts.** Quality over volume. 20 qualified prospects beats 200 unqualified ones.
8. **Tag every prospect with its source.** The user needs to know how each prospect was found.

---

## 10) Edge Cases

- **No backlink data tools available (Ahrefs + DataForSEO):** Run sections 3–6 only (resource pages, guest posts, broken links via Google Search + Scraper). Note that backlink gap analysis and DR qualification are unavailable.
- **Target domain has no linkable content:** Flag this before proceeding. Link building without something worth linking to is ineffective. Suggest the user develop linkable assets first.
- **Niche is too narrow for resource page/guest post discovery:** Note low prospect volume. Focus on backlink gap analysis as primary source.
- **User provides competitors that aren't actual organic competitors:** Validate competitor overlap before running backlink gap. If overlap is minimal, flag it and suggest alternatives.
