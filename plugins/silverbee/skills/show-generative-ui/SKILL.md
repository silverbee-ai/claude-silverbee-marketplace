---
name: show-generative-ui
description: >
  Guide for using the silverbee-mcp MCP to render dashboards, charts, tables,
  and interactive UI in Cowork. Covers render_template, show_generative_ui,
  show_html, troubleshooting, and the template catalog.
---

# Generative UI — Quick Reference

The `silverbee-mcp` MCP server renders interactive UI inline in chat.
Three tools available, in order of preference:

| Tool | When to use | Token cost |
|---|---|---|
| `render_template` | A matching template exists (see catalog below) | Low — just pass data |
| `show_generative_ui` | Custom layout not covered by any template | Medium — full spec |
| `show_html` | Raw HTML/CSS/JS needed (escape hatch) | High — full markup |

**Always check `list_templates` first.** If a template fits, use `render_template`.

---

## Template Catalog

| Template | Components | Use with skill |
|---|---|---|
| `keyword-research` | 4 metrics + bar chart + keywords table + SERP table | keyword-research |
| `competitor-analysis` | 4 metrics + cluster chart + gap keywords + top pages | competitor-analysis, seo-gap-analysis |
| `technical-seo` | 4 metrics + category chart + findings + roadmap | technical-seo, preliminary-technical-seo-audit |
| `performance-report` | 4 metrics + trend chart + rankings + actions | periodic-seo-report, search-performance-monitoring |
| `drop-analysis` | 4 metrics + line chart + affected pages + ranking drops | drop-analysis |
| `link-building` | 4 metrics + category chart + prospects + timeline | link-building, link-building-outreach |
| `ai-visibility` | 4 metrics + engine chart + competitor presence + AIO | ai-visibility, prospect-snapshot |
| `content-optimization` | 4 metrics + placement chart + placements + removed | content-optimization |
| `topical-authority` | 4 metrics + coverage chart + content gap + priority | topical-authority-mapping |
| `input-form` | Dynamic form from field definitions | interactive-ui (input collection) |
| `progress-tracker` | 4 metrics + accordion steps | interactive-ui (workflow progress) |
| `save-workflow` | Callout + 3 metrics + summary + CTA button | seo-output-formatter (save workflow) |

---

## Using render_template

```json
render_template({
  "template": "keyword-research",
  "data": {
    "title": "Keyword Research — example.com",
    "metrics": {
      "bestTarget": "seo tools",
      "highestVolume": "12,400",
      "fastestGrowing": "ai seo",
      "totalKeywords": "847"
    },
    "chart": {
      "data": [
        {"keyword": "seo tools", "volume": 12400},
        {"keyword": "ai seo", "volume": 8100}
      ]
    },
    "keywords": {
      "columns": ["Keyword", "Volume", "KD", "CPC", "Intent"],
      "rows": [["seo tools", "12,400", "67", "$4.20", "Commercial"]]
    },
    "serp": {
      "columns": ["Feature", "Present"],
      "rows": [["Featured Snippet", "Yes"]]
    }
  }
})
```

**All templates follow the same pattern:**
- `metrics` — object with 4 named string fields (see each skill's reference card)
- `chart` — `{ data: [...] }` where data is an array of objects with numeric values
- Two tables — `{ columns: string[], rows: string[][] }`

---

## Using show_generative_ui (custom specs)

Use when no template matches. Build a flat element tree:

```json
show_generative_ui({
  "spec": {
    "root": "root",
    "elements": {
      "root": {
        "type": "Stack",
        "props": { "gap": 3 },
        "children": ["heading", "metric-grid", "table"]
      },
      "heading": {
        "type": "Heading",
        "props": { "text": "Custom Report", "level": 2 }
      },
      "metric-grid": {
        "type": "Grid",
        "props": { "columns": 3 },
        "children": ["m1", "m2", "m3"]
      },
      "m1": { "type": "Metric", "props": { "label": "Score", "value": "92" } },
      "m2": { "type": "Metric", "props": { "label": "Issues", "value": "3" } },
      "m3": { "type": "Metric", "props": { "label": "Pages", "value": "142" } },
      "table": {
        "type": "Table",
        "props": {
          "columns": ["URL", "Status", "Issue"],
          "rows": [["/about", "Warning", "Missing H1"]]
        }
      }
    }
  }
})
```

### Component quick reference

**Leaf** (no children, content in props):
Heading, Text, Markdown, CodeBlock, Metric, Badge, Callout, Link, Image,
Progress, Table, Chart, Accordion, Button, Input, Textarea, Select,
Checkbox, Switch, DateInput, DateTimeInput, Separator

**Container** (layout via children):
Stack, Grid, Card, Tabs, TabContent, Dialog

---

## Troubleshooting

### "Unknown template"
Template name must match exactly. Use `list_templates` to see valid names.
Common mistakes: underscores instead of hyphens (`keyword_research` → `keyword-research`),
plurals, abbreviations, or extra spaces.

### "Leaf types must NOT have children"
You added `children` to a leaf component. Move content to `props` instead.
```
BAD:  { "type": "Table", "children": ["row1"] }
GOOD: { "type": "Table", "props": { "columns": [...], "rows": [...] } }
```

### "root must exist in elements"
Your `root` field references an ID that doesn't exist in `elements`.
```
BAD:  { "root": "main", "elements": { "dashboard": { ... } } }
GOOD: { "root": "dashboard", "elements": { "dashboard": { ... } } }
```

### "child ID not found in elements"
A `children` array references an element ID that doesn't exist.
Check for typos in IDs. Every ID in `children` must have a matching key in `elements`.

### Chart shows nothing / wrong values
Chart data values must be **raw numbers**, not strings with units.
```
BAD:  { "keyword": "seo", "volume": "12,400" }
GOOD: { "keyword": "seo", "volume": 12400 }
```
Also check: `xKey` must match a key in your data objects, and `colors` must be an array.

### Table shows empty or wrong columns
Table `columns` must be `string[]` and `rows` must be `string[][]` (array of arrays).
```
BAD:  "rows": [{"url": "/about", "status": "ok"}]
GOOD: "rows": [["/about", "ok"]]
```

### Link doesn't navigate in Cowork iframe
Use a Button with `openLink` action instead of a Link component:
```json
{
  "type": "Button",
  "props": { "label": "Open Report" },
  "on": {
    "press": {
      "action": "openLink",
      "params": { "url": "https://example.com" }
    }
  }
}
```

### Metric trend shows raw text instead of arrow
`trend` must be exactly `"up"`, `"down"`, or `"neutral"` — not percentages or numbers.
```
BAD:  { "trend": "+12%" }
GOOD: { "trend": "up", "detail": "+12%" }
```

### Badge doesn't render correctly
Badge uses `label` + `color` (hex), not `text` + `variant`.
```
BAD:  { "type": "Badge", "props": { "text": "New", "variant": "success" } }
GOOD: { "type": "Badge", "props": { "label": "New", "color": "#16A34A" } }
```

### Too many elements / slow render
Keep specs under ~40 elements. If you need more data, put it in Table rows
(which render as one element regardless of row count) rather than individual elements.

### render_template validation error
The data you passed doesn't match the template's schema. Call `list_templates`
to see the exact required fields and types. Common issues:
- Missing a required field (check `required` array in schema)
- Passing a number where a string is expected (metric values are strings)
- `chart.data` is missing or has wrong field names
- Table `rows` is objects instead of arrays of strings

### State / interactivity not working
- State paths must start with `/` (e.g., `/userName`, not `userName`)
- Use `$bindState` for two-way binding on inputs, `$state` for read-only
- Dialog open/close requires `setState` on the path in `props.openPath`
