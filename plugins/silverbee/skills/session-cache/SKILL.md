---
name: session-cache
description: >
  Conversation-scoped data reuse. If you already fetched data for a domain
  in this conversation, reuse the result instead of re-fetching.
---

# Skill: Session Cache

## Rule

Before making **any** MCP call, check if you already made the same call
earlier in this conversation. If you did, reuse that result — do not call
the API again. This applies to **all** call types:

### Discovery calls (highest savings)

These calls return the same result for the entire conversation. **Never**
call them more than once per session:

- `get_instructions` — returns the tool catalog. Call once, reuse forever.
- `list_available_apps` — returns connected apps. Call once, reuse forever.
- `search_actions(query)` — returns operation IDs. Call once per unique
  query, reuse for any subsequent need for the same operations.
- `list_actions(app_name)` — returns app operations. Call once per app.

### Data calls

Same **domain** + same **data type** + same **source app** + same
**parameters** = reuse.

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
