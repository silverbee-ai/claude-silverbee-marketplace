---
name: link-building-community
description: Community-based link building via blog comments, forums, Q&A sites, niche directories, and social bookmarks. Uses footprint queries to discover topically relevant placement opportunities across languages. Covers placement discovery, multilingual footprints, qualification, and contribution guidelines. Use for any request involving blog comment links, forum links, Q&A links, directory submissions, social bookmarks, or community link placements.
---

# Skill: Community Link Building

## Title
Community Link Building — Placement Discovery & Execution

## Description
Discovers and qualifies link placement opportunities on community platforms: blogs, forums, Q&A sites, niche directories, and social bookmarks. Uses footprint queries to find relevant sites that accept contributions, qualifies each for topical relevance and link viability, and provides placement-ready recommendations with contribution guidelines.

---

## 1) Input

**Required:** target domain, target topic/niche keywords.
**Optional:** target language/market, target landing pages, anchor text preferences (inherit from parent `link-building` skill Section 5 if called from there).

---

## 2) Footprint Query Methodology

Footprint queries combine a platform identifier, a posting/commenting indicator, and a topic term to find sites that accept community contributions. The agent constructs and runs these via Google Search.

**Pattern:** `[platform/software identifier] + [posting indicator in target language] + "[topic term]"`

**Rules:**
- Run queries on the Google domain matching the target language (google.com for English, google.fr for French, google.co.il for Hebrew, etc.).
- Replace `[topic]` with niche-specific terms derived from the target domain's content.
- Run multiple queries per link type — vary the topic term across the site's key themes.
- Footprints are discovery patterns, not a fixed list. Platform-specific patterns go stale as platforms rise and fall. Verify every discovered site before recommending.

---

## 3) Blog Comment Placements

**English footprints:**
- `site:blogspot.com "Post a Comment" +"[topic]"`
- `site:wordpress.com "Leave a Reply" +"[topic]"`
- `"post a comment" OR "leave a comment" +"[topic]"` (platform-agnostic, broader)

**Multilingual footprints (use on the corresponding regional Google domain):**
- **Hebrew:** `site:blogspot.com "הזן את התגובה שלך" +"[topic]"` / `site:wordpress.com "כתיבת תגובה" +"[topic]"`
- **French:** `site:blogspot.com "Enregistrer un commentaire" +"[topic]"`
- **Spanish:** `site:blogspot.com "Publicar un comentario en la entrada" +"[topic]"`
- **German:** `site:blogspot.com "Kommentar veröffentlichen" +"[topic]"`
- **Italian:** `site:blogspot.com "Posta un commento" +"[topic]"`
- **Dutch:** `site:blogspot.com "Een reactie plaatsen" +"[topic]"`
- **Russian:** `site:blogspot.com "Отправить комментарий" +"[topic]"`
- **Arabic:** `site:blogspot.com "إرسال تعليق" +"[topic]"`
- **Turkish:** `site:blogspot.com "Yorum Gönder" +"[topic]"`

For languages not listed, identify the localized "post a comment" string for the target blog platform and construct the query using the same pattern.

**Qualification before recommending:**
- Blog content is topically relevant to the target domain's niche.
- Blog has real readership (not abandoned — recent posts, active comment section).
- Comment section is moderated (unmoderated = likely spam-filled = low value).
- Comments are not restricted to members only (or registration is feasible).
- Commenting allows a URL field or in-comment link.

**Contribution rules:**
- The comment must add genuine value to the blog post — a substantive response, question, or insight related to the post's content.
- Never post generic praise ("Great article!") with a link. This is spam.
- The link should appear in the URL/website field of the comment form, not forced into the comment body unless contextually natural.
- One comment per blog post. Do not spam multiple posts on the same blog.

---

## 4) Forum Placements

**Footprints:**
- `"powered by vbulletin" +"[topic]"`
- `"powered by phpBB" +"[topic]"`
- `"proudly powered by bbPress" +"[topic]"`
- `"powered by XenForo" +"[topic]"`
- `"powered by Discourse" +"[topic]"`

**Qualification before recommending:**
- Forum is topically relevant and active (recent posts within the last month).
- Forum allows new member registration.
- Forum permits profile signatures with links, or allows contextual links within posts.
- Forum is not a link farm or spam dump (check post quality, moderation activity).

**Contribution rules:**
- Participate genuinely — answer questions, share expertise, contribute to discussions before placing any links.
- Links should be contextually relevant to the discussion thread, not forced.
- Profile signature links are acceptable where allowed — use natural anchor text, not exact-match keyword anchors.
- Do not create threads solely to drop a link. Contribute to existing relevant threads.
- Verify that the forum's rules permit outbound links. Some forums restrict links for new accounts.

---

## 5) Q&A Site Placements

**Footprints:**
- `site:quora.com +"[topic]"`
- `site:reddit.com +"[topic]"` (identify relevant subreddits and threads)

**Major Q&A platforms (no footprint needed — search directly):**
- Stack Exchange network: for technical/professional niches with matching Stack Exchange sites.
- Industry-specific Q&A platforms discovered via general search.

**Qualification before recommending:**
- The question must be genuinely relevant to the target domain's expertise.
- The Q&A site has real traffic and active community participation.
- Answers allow links (some platforms restrict links for new users or low-reputation accounts).

**Contribution rules:**
- The answer must be genuinely useful and substantive — not a thin response built around a link.
- The link must support the answer as a reference or resource, not replace the answer itself.
- Do not answer questions just to place a link. Answer because the expertise matches — the link is supplementary.
- On platforms with reputation systems (Stack Exchange, Quora), build reputation before placing links.

---

## 6) Niche Directory Placements

**Discovery (no footprint needed — direct search):**
- `"[industry] directory" submit`
- `"[industry] business listing"`
- `best [industry] directories [year]`

**Qualification before recommending:**
- Directory is industry-specific and editorially curated — not a general web directory accepting all submissions.
- Directory has real organic traffic (check via Ahrefs if available).
- Directory pages are indexed by search engines.
- Listing allows a website URL link.

**Avoid:** general-purpose directories with no editorial review, directories that charge excessive fees for basic listings, directories with pages full of unrelated outbound links.

**Contribution rules:**
- Submit accurate business information — name, description, category, URL.
- Use a natural business description, not a keyword-stuffed blurb.
- Select the most specific relevant category available.

---

## 7) Social Bookmark Placements

**Platforms (search for active platforms in the target market):**
- General: Reddit, Mix, Flipboard, Pocket.
- Niche-specific: industry communities, aggregators, and curation platforms relevant to the target domain's content.

**Contribution rules:**
- Submit content that is genuinely useful or interesting to the platform's community.
- Use descriptive, natural titles — not keyword-stuffed headlines.
- Do not submit the same URL repeatedly across platforms in a short window. Space submissions naturally.
- Engage with the community — upvote, comment, contribute — not just drop links.

---

## 8) Output

**Per link type — structured placement list:**

| Platform | URL | Type (Blog/Forum/Q&A/Directory/Bookmark) | Topic Relevance | Activity Level | Link Placement Method | Qualification Status |

**Contribution briefs per placement:** for each qualified opportunity, provide a brief describing what to post/comment, how the link fits naturally, and the recommended anchor approach.

**Summary:** total opportunities found, qualified count, breakdown by type, breakdown by language/market.

---

## 9) Guardrails

- Every placement must be qualified for topical relevance before recommending. High-traffic irrelevant platforms are rejected.
- Never recommend mass-posting, automated submission, or any form of link spam. Each placement requires a genuine, unique contribution.
- Footprint queries are discovery tools, not execution scripts. The agent discovers, qualifies, then recommends — does not auto-submit.
- Contribution quality is non-negotiable. A thin or generic contribution with a link is spam regardless of the platform's authority.
- Multilingual footprints must use the correct regional Google domain and localized strings. Do not run English footprints for non-English markets.
- Platform-specific footprints go stale. The agent must verify every discovered site is still active and accepting contributions.
- These are Tier 3 (supplementary) links. Do not over-invest in community links at the expense of Tier 1–2 strategies. Their value is in profile diversity, not as the primary link building method.
- All anchor text and landing page decisions inherit from the parent `link-building` skill's anchor text strategy (Section 5) and diversification rules (Section 6) when called from the parent.
