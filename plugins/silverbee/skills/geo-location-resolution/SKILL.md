---
name: geo-location-resolution
description: >
  Determines the correct country/geo location parameter before any tool call that accepts
  a geo or country input (Ahrefs, DataForSEO, GSC, rank trackers, keyword tools).
  Use when planning any tool call that requires a country or geo parameter.
  Not needed when the user has explicitly specified a target country.
---

# Skill: Geo location Resolution

## Core Rule

Never derive the `geo` or `country` parameter from:
- User location
- Business registration country
- HTML signals (currency, hreflang, language tags)
- Assumed or inferred target market

These do not reliably reflect where a business targets organic traffic. A business 
registered in Austria may target the US. A site built on a US platform may serve 
only German users. Always verify from traffic data.

---

## Resolution Process

**Step 1 — Check GSC (primary source)**
Pull the GSC country breakdown from performance data. Identify the country with 
the highest organic traffic share.

**Step 2 — Check Ahrefs (secondary source)**
Pull organic traffic by country. Identify the top country by traffic share.

**Step 3 — Determine dominant traffic country**

| Situation | Action |
|-----------|--------|
| GSC and Ahrefs agree on top country | Use that country as dominant |
| GSC and Ahrefs conflict | Default to GSC as dominant, flag the discrepancy |
| Only one source available | Use available source, note the limitation |
| No country breakdown available | Ask the user to specify a target country |

**Step 4 — Apply final geo selection**

| Situation | Action |
|-----------|--------|
| User specified a geo + matches dominant country | Use it |
| User specified a geo + conflicts with dominant country | Use user geo, flag that it is not the dominant traffic country |
| No user geo specified | Use dominant traffic country |
| No dominant country and no user geo | Ask the user to specify a target country |

---

## Output Requirement

The selected geo and its data source must be explicitly stated in the plan before 
any tool call is constructed. Example:

> `geo: US` — sourced from GSC country breakdown (US: 74% of organic traffic)

> `geo: DE` — sourced from Ahrefs (GSC unavailable; DE: 61% of organic traffic)

> No geo set — no country breakdown available in GSC or Ahrefs. Awaiting user input.

---

## Scope

This rule applies to all tools that accept a geo or country parameter, including 
but not limited to: Ahrefs, DataForSEO, GSC filters, rank trackers, and keyword 
research tools. Geo resolution runs once per planning context and remains fixed for 
all subsequent tool calls unless:
- The user explicitly changes the target geo
- The task objective changes (e.g., multi-country comparison)
