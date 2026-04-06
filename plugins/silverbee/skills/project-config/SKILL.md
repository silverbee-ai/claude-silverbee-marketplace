---
name: project-config
description: >
  Reads .silverbee.json from the working directory to load project defaults.
  Skills check this config before asking the user for domain, competitors, etc.
  All fields are optional — skills work without this file (current behavior).
---

# Skill: Project Config

## Config file: `.silverbee.json`

Located in the project root (working directory). All fields optional:

```json
{
  "domain": "example.com",
  "competitors": ["competitor1.com", "competitor2.com"],
  "geo": "us",
  "language": "en",
  "brand_terms": ["Example", "Example Inc"],
  "target_keywords": ["primary keyword", "secondary keyword"],
  "gsc_property": "sc-domain:example.com",
  "excluded_paths": ["/staging/", "/dev/", "/test/"],
  "output": {
    "html_dir": "./seo-reports",
    "default_format": "all"
  }
}
```

## How skills use project config

### At workflow start

Before asking the user for a domain or competitors, check if `.silverbee.json`
exists in the working directory. If it does, read it and use its values as
defaults.

### Priority order

1. **User's explicit input** in the current message — always wins
2. **`$ARGUMENTS`** passed to the command — second priority
3. **`.silverbee.json`** values — used when the user doesn't specify

### Field usage by skills

| Field | Used by |
|-------|---------|
| `domain` | All skills that need a target domain |
| `competitors` | competitor-analysis, seo-gap-analysis |
| `geo` | geo-location-resolution (skips GSC lookup if set) |
| `language` | keyword-research, content-optimization |
| `brand_terms` | keyword-research (brand vs non-brand filtering) |
| `target_keywords` | content-optimization, search-performance-monitoring |
| `gsc_property` | gsc-query-planning (exact property ID) |
| `excluded_paths` | tech-seo-crawl, tech-seo-indexation (ignore paths) |
| `output.html_dir` | seo-output-formatter (where to write HTML reports) |
| `output.default_format` | seo-output-formatter (output layers to produce) |

### Behavior when config is missing

If `.silverbee.json` doesn't exist, skills behave exactly as they do today —
ask the user for required inputs. Never error on a missing config file.

### Behavior when a field is missing

Use the field if present; ignore if absent. Never require any field.
For example, if `domain` is set but `competitors` is not, use the domain
but still ask the user for competitors when needed.
