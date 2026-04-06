---
name: canonical-url-and-domain-validation
description: Pre-analysis validation of domain canonical status, HTTP resolution, variant consistency, and index status. Use at the start of any workflow that pulls data by domain or URL, checks indexation, or performs canonical analysis. Do not use as a standalone audit deliverable.
---

# URL and Domain Validation
**Pre-Analysis URL and Domain Canonical Target Validation**

Input: {Domain or URL} and consuming skill declaration (Validation level: Level 1 only / Level 1 + Level 2; Level 2 applies to: [which URLs and under what conditions]).

**Pre-execution check (satisfy from context before fetching):** confirm the canonical domain and indexation status have not already been confirmed from user context or earlier in the session; if both are already confirmed, validation is not required; if canonical domain is missing, proceed to Level 1; if index status is missing but canonical domain is confirmed, proceed to Check C only; if the consuming skill declares Level 2, run Level 2 after Level 1 passes regardless of cache state.

---

## Level 1 — Domain Validation (Always)

**A — HTTP Status:** fetch root domain, record HTTP status.
- 3xx → follow redirect chain up to 5 hops, use final destination as active domain, notify user.
- Chain > 5 hops → flag as excessive redirect chain, stop following, report chain to that point, ask user to confirm which destination to use — **blocking gap, full stop until user confirms.**
- 4xx/5xx → **hard stop**, domain not accessible, notify user.

Active domain after Check A: set from the final resolved URL, propagates forward.

**B — Canonical Domain:** identify the canonical domain by checking the following signals in order — stop at the first signal that produces a clear result.
1. Canonical tag in `<head>`
2. HTTP `Link` response header
3. Domain version that receives 301 redirects from other variants
4. Domain version registered as the primary property in GSC

Canonical tag handling:
- Absolute URL → extract the domain version from it.
- Relative URL → derive the host from the final resolved URL (established in Check A) and use that as the base domain for www/non-www/http/https comparison.
- Self-referential → confirms the current URL is the preferred version, proceed to conflict check.
- No canonical tag present → move to signal 2 without treating absence as a failure.

Conflict handling:
- Any signals conflict at any point → report the conflict clearly, list the conflicting signals and their values, ask user to confirm before proceeding — **blocking gap.**
- All available signals agree → that domain version is the canonical domain.

Circular conflict check: confirm the canonical domain does not 301 back to a variant, and no redirect destination has a canonical pointing back to the origin.
- Circular conflict detected → **hard stop**, show the full conflict clearly, do not proceed.

Variant stability check: once the canonical domain is confirmed, verify it is applied consistently across all common variants — www/non-www, http/https, trailing slash presence/absence, and common parameter-appended versions (e.g., `?ref=`, `?utm_`). Inconsistency across variants → flag, list the inconsistent variants, report to user.

Once the canonical domain is confirmed — if it differs from the domain provided in the input, apply the following:
- Same-domain mismatch (www/non-www, http/https, trailing slash) → switch to canonical domain, notify user, continue all analysis using the canonical domain; do not use the original input domain for any subsequent data pull.
- Cross-domain canonical → **hard stop**, state both domains, wait for confirmed user intent and verified GSC access — **blocking gap, do not proceed without confirmation.**

Canonical domain confirmed after Check B: used for all subsequent analysis.

**C — Homepage Index Status:** identify index status using the following fallback chain — stop at the first signal that produces a result.
1. GSC urlInspection → authoritative status with reason if not indexed.
2. `site:[homepage-url]` → a yes/no result only, not conclusive on its own.
3. Neither available → soft gap, note and proceed.

Result handling:
- Homepage confirmed not indexed via GSC → flag as critical, report the reason, ask user to confirm intent before proceeding — **blocking gap, full stop until user confirms.**
- Homepage not appearing in `site:` search → flag, not conclusive, confirm with user.

---

## Level 2 — URL Validation (When Consuming Skill Requires)

Level 2 runs only after Level 1 passes. If Level 1 produces a hard stop, do not proceed to Level 2. Consuming skill defines which URLs trigger Level 2 and under what conditions.

**D — URL Status:** fetch URL, record status.
- 3xx → follow up to 5 hops, record each hop; consuming skill defines whether to proceed with original or destination.
- Chain > 5 hops → flag as excessive redirect chain, stop following; consuming skill defines next step.
- 4xx → URL not serving content, not automatically invalid; consuming skill defines next step.
- 5xx → flag server-side issue.

**E — Indexability and Index Status:** a URL can be crawlable but excluded from the index — both must be confirmed independently.

Indexability: inspect meta robots tag in `<head>` and X-Robots-Tag in HTTP response headers for noindex directives.
- JS rendering may obscure noindex directives from a standard scraper. Proxy indicators of JS rendering: thin or empty `<head>` content, absence of expected meta tags, React/Next.js/Vue signatures in the HTML. If any proxy indicator is present → flag, note that indexability check may be incomplete.

Index status: confirm using the following fallback chain — stop at the first signal that produces a result.
1. GSC urlInspection → authoritative status with reason if not indexed.
2. `site:[url]` → a yes/no result only, lower confidence, note accordingly.
3. Neither available → soft gap, note and proceed.

**F — Canonical Target Status:** if the subject URL carries a canonical tag, fetch the canonical target URL and record its HTTP status.
- Non-200 status → **hard stop**, flag as critical: canonical points to a non-serving URL; report the target URL and its status, do not proceed without user confirmation — **blocking gap.**
- 3xx → flag: canonical target itself redirects; this creates a canonical-redirect chain; report the full chain, ask user to confirm intent — **blocking gap.**
- 4xx/5xx → **hard stop**, canonical target not accessible, report and halt.

**G — Canonical Target Indexability:** once canonical target is confirmed as 200 (Check F), inspect the canonical target URL for noindex directives using the same method as Check E.
- Canonical target carries noindex → **hard stop**, flag as critical: canonical points to a non-indexable URL; this defeats the purpose of the canonical; report and halt — **blocking gap.**
- JS rendering proxy indicators present on canonical target → flag, note check may be incomplete.

**H — Canonical-Redirect Conflict:** check whether the subject URL both carries a canonical pointing to URL-C and also issues a redirect to URL-R, where URL-C ≠ URL-R.
- Conflict present → **hard stop**, two competing destination signals exist; report both the canonical target and the redirect destination clearly, do not proceed without user confirmation — **blocking gap.**
- No conflict → proceed.
