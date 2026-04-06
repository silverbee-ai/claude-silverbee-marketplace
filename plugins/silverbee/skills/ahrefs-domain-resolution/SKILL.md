---
name: ahrefs-domain-resolution
description: >
  Governs how the planner constructs Ahrefs tool calls to avoid false-zero
  data results caused by incorrect domain mode selection. Trigger whenever planning
  any Ahrefs organic data retrieval (keywords, traffic, backlinks). Not for GSC queries
  or non-Ahrefs tools.
---

# Skill: Ahrefs Domain Resolution

## Default Behavior

When planning an Ahrefs call, default to `mode: subdomains` unless the user explicitly 
specifies a root domain only. This mode captures data across all subdomains (including 
`www`) and is the safer default for most real-world websites.

## Zero-Data Fallback Rule

If an Ahrefs call returns 0 organic keywords **and** 0 traffic:

**Do not report zero as final.** Plan a second call using the alternative mode before 
concluding the site has no organic presence.

Fallback sequence:
1. First call used `mode: domain` → retry with `mode: subdomains`  
2. First call used `mode: subdomains` → retry with `mode: domain`

If both calls return 0, only then report zero data as confirmed, and flag it explicitly:
> "Both `domain` and `subdomains` modes returned 0 data for [target]. The site may 
> have no indexed organic presence, or the domain input may be incorrect."

## Mode Reference (for planning)

| Mode | What it covers |
|------|----------------|
| `domain` | Root domain only — excludes `www` and other subdomains |
| `subdomains` | Root + all subdomains (`www`, `blog`, `shop`, etc.) |
| `prefix` | URLs matching a specific path prefix |
| `exact` | Single exact URL |

## Common Root Cause

Websites indexed under `www` will return 0 data when queried with `mode: domain`. 
This is technically correct but misleading — the data exists under `www.domain.com`, 
not `domain.com`. The fallback rule above prevents this from surfacing as a false zero.
