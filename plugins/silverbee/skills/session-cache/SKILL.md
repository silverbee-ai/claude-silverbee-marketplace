---
name: session-cache
description: >
  Conversation-scoped data reuse. If you already fetched data for a domain
  in this conversation, reuse the result instead of re-fetching.
---

# Skill: Session Cache

## Rule

Before making an MCP data fetch, check if you already fetched the same
data type for the same domain earlier in this conversation. If you did,
reuse that result — do not call the API again.

## What counts as "same data"

Same **domain** + same **data type** + same **source app**.

Example: If you fetched GSC keywords for example.com in step 2, and step 6
needs GSC keywords for example.com again, reuse step 2's result.

If the data came from a fallback app (e.g., Ahrefs instead of GSC), it is
not the same as the primary source. Do not substitute one for the other.

## When to re-fetch

- User explicitly asks to "refresh", "re-fetch", or "get fresh data"
- The new query needs different parameters (different date range, filters, etc.)
- The earlier fetch returned an error (never reuse errors)

## Status updates

When reusing data, say so:
`✓ Reusing GSC keyword data from earlier (847 keywords)`

## Scope

- Conversation only — no persistence across sessions
- No token overhead — this is a behavioral rule, not a data structure
