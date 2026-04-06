---
name: tech-seo-schema
description: "Structured data audit and implementation skill. Use when: (1) auditing existing schema on a page for errors, conflicts, or guideline violations, (2) recommending or building new schema for a page, (3) investigating why rich results are not appearing, (4) checking AI Overview eligibility signals via structured data, (5) handling non-conventional page types that require schema.org lookup before implementation. Not for keyword research, content planning, or GSC performance analysis."
---
# Skill: Tech SEO — Schema & Structured Data

## Parallel Execution (MANDATORY)

Batch all independent tool calls into a single `run_multi_actions` call. When checking multiple URLs, fetching GSC + Ahrefs data, or querying multiple pages simultaneously, send all calls at once. Never call `run_action` sequentially for independent lookups — that is a performance bug.

---


## 1) Checks
- Detect existing schema on target pages.
- Confirm schema matches visible content (no fabricated reviews, ratings, or data).
- No conflicting schema types on the same page.
- No schema on noindex pages (wasted — search engines won't use it).
- No fatal syntax errors (validate before reporting).
- Appropriate schema type for the page content.
- Detect Rating, Review, or AggregateRating schema on the homepage — flag it as a guideline violation.

**Preferred stable patterns:** Product, Article, FAQ, LocalBusiness, BreadcrumbList, Organization, WebSite. Only recommend others when clearly justified by page content.

**Non-conventional page types:** If the target page does not map clearly to a preferred pattern (e.g. a stock quote page, vehicle listing, medical condition page, or financial instrument), do not guess. Fetch `https://schema.org/docs/documents.html` to identify the most semantically appropriate type before recommending or building any schema. State which type was selected and why.

---

## 2) Rules
- Recommend schema only if matching content exists on the page. Never recommend schema for content that isn't there.
- Provide complete JSON-LD ready to implement — not fragments.
- Include placement instruction (where in HTML).
- Flag contradictions: noindex + schema = wasted effort.
- Validate syntax before providing.
- Avoid conflicting schema types on the same page.

**Example data disclosure:** Never produce a schema block where fields are filled with placeholder or example values without explicitly flagging them. Every field containing example data must be marked with an inline comment (e.g. `// replace with actual value`) and a summary note must appear before the block stating which fields require real data before implementation.

**Homepage exception:** Never recommend Rating, Review, or AggregateRating schema for the homepage. Ratings require specific, reviewable entities (a product, a service, a business location). A homepage is a navigational entry point — applying rating schema to it is a misuse of the type and a Google guideline violation that can trigger a manual action.

---

## 3) Common Implementation Fails — Flag on Detection

These are patterns that are technically valid JSON-LD but violate Google's guidelines or produce misleading rich results. Flag any of the following when detected:

- **`InStock` on non-physical products** — `offers.availability: InStock` is only valid for physical or digital products with inventory. Never recommend it for apps, SaaS platforms, or web services. Use `OnlineOnly` or omit availability entirely for software products.
- **AggregateRating on pages without visible reviews** — Rating schema must reflect reviews that are actually visible to users on the page. Marking up ratings that exist only in a database or are hidden in the UI is a guideline violation.
- **AggregateRating on category or listing pages** — Ratings must be tied to a specific, reviewable entity. A category page listing multiple products cannot carry a single AggregateRating.
- **Product schema on category/listing pages** — Use `ItemList` with nested `ListItem` references instead.
- **Schema drift** — Schema that no longer matches on-page content (e.g. price changed, product discontinued, reviews removed). Flag any mismatch between schema field values and visible page content.
- **Identical schema copy-pasted across pages** — Each page must have unique schema reflecting its specific content. Boilerplate schema applied site-wide will be ignored or can trigger a manual action.
- **Mismatched rating scale** — `ratingValue` must be consistent with `bestRating`. A `ratingValue: 4.5` paired with `bestRating: 10` will display incorrectly in rich results.
- **Missing required fields for rich results** — Common omissions: `Article` missing `image`, `author`, or `datePublished`; `Product` missing `name`, `image`, or `offers`; `FAQPage` missing `acceptedAnswer`.

---

## 4) AI Overview Eligibility Signals
Schema types most correlated with AI Overview appearances: `FAQPage`, `HowTo`, `Article`.

- If a page contains Q&A content, step-by-step instructions, or an article body — and is missing the corresponding schema type — flag it as an AI Overview eligibility gap.
- Flag only when the content genuinely matches the type. Do not recommend FAQPage for pages without explicit Q&A pairs, or HowTo for pages without sequential steps.
- Note eligibility gaps in the output table under Recommended Schema.

---

## 5) Output
Per page:
| Page URL | Current Schema | Issues | Recommended Schema | AI Overview Gap | JSON-LD Block | Placement | Validation Notes |

JSON-LD blocks must be complete, syntactically valid, and ready to paste into the page. Any fields containing example or placeholder data must be explicitly flagged both inline and in a pre-block note.
