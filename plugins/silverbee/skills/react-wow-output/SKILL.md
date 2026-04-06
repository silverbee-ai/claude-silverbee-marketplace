---
name: react-wow-output
description: >
  Documents the show_generative_ui component API and spec format for producing
  executive dashboards in Silverbee Cowork. Covers the full component catalog,
  spec format, per-workflow dashboard specs, and output constraints.
  For interactive patterns (forms, progress trackers, explorable results),
  see the interactive-ui skill. Replaces JSX file writing.
---

# Skill: show_generative_ui Component API

## Purpose

Use `show_generative_ui` to present SEO deliverables as compact, executive-quality
dashboards directly in the chat. Components render natively — not as file artifacts.
This replaces writing `.jsx` files.

Always use this skill when:
- Running keyword research, SEO audit, competitor analysis, or a performance report
- The user asks for something visual, impressive, polished, or "wow"
- There is structured data (tables, scores, rankings, metrics) to present

For **interactive patterns** (input forms, progress trackers, explorable results),
load the `interactive-ui` skill.

---

## Spec Format

Every `show_generative_ui` call takes a `spec` object with this structure:

```json
{
  "root": "root-element-id",
  "elements": {
    "root-element-id": {
      "type": "Stack",
      "props": { "direction": "vertical", "gap": 4 },
      "children": ["child-1", "child-2"]
    },
    "child-1": {
      "type": "Heading",
      "props": { "text": "Dashboard Title", "level": 1 }
    },
    "child-2": {
      "type": "Text",
      "props": { "text": "Some content here" }
    }
  },
  "state": {
    "optional": "data object for bindings"
  }
}
```

**Key rules:**
- `root` — string key that must exist in `elements`
- `elements` — flat map of `id → node`. Each node has `type` (required), `props`, `children` (array of element IDs), and optional `on`, `repeat`, `visible`
- `state` — optional object for data bindings and dynamic content
- Use an optional `title` parameter (outside `spec`) to show a title above the UI

---

## Component Reference

### Layout

#### Stack
Flex layout container. Every dashboard starts with a Stack as root.

| Prop | Type | Description |
|------|------|-------------|
| `direction` | string | `"vertical"` (default) or `"horizontal"` |
| `gap` | number | Spacing between children |
| `align` | string | Cross-axis alignment |
| `justify` | string | Main-axis alignment |
| `className` | string | Custom CSS class |

#### Grid
Multi-column grid layout. Use for KPI strips and side-by-side cards.

| Prop | Type | Description |
|------|------|-------------|
| `columns` | number | Number of columns (e.g., 4 for KPI strip) |
| `gap` | number | Spacing between grid items |
| `className` | string | Custom CSS class |

#### Card
Content container with optional title and description.

| Prop | Type | Description |
|------|------|-------------|
| `title` | string | Card header |
| `description` | string | Subtitle text |
| `maxWidth` | string | Maximum width (e.g., `"600px"`) |
| `centered` | boolean | Center the card |
| `className` | string | Custom CSS class |

---

### Content

#### Heading
Section titles.

| Prop | Type | Description |
|------|------|-------------|
| `text` | string | Heading text |
| `level` | number | `1` for main title, `2` for section headers |

#### Text
Prose content, bullet points, executive summary.

| Prop | Type | Description |
|------|------|-------------|
| `content` or `text` | string | Text content. Use `\n` for line breaks, `•` for bullets |
| `muted` | boolean | Dimmed/secondary styling |
| `variant` | string | Text style variant |

#### Markdown
GitHub-flavored markdown rendering for rich text content.

| Prop | Type | Description |
|------|------|-------------|
| `content` | string | Markdown string |

#### CodeBlock
Formatted code snippet block.

| Prop | Type | Description |
|------|------|-------------|
| `code` | string | Code content |
| `language` | string | Language for syntax highlighting |
| `wrap` | boolean | Wrap long lines |

---

### Data Display

#### Metric
KPI callout. Use exactly **4 Metrics** per output dashboard as the top-level KPI strip.

| Prop | Type | Description |
|------|------|-------------|
| `label` | string | Short label (≤4 words) |
| `value` | string | Display value — digits + brief qualifier, no sentences |
| `detail` | string | Additional detail text |
| `trend` | string | `"up"`, `"down"`, or `"neutral"` |

#### Table
Tabular data with optional search, sort, and filter.

| Prop | Type | Description |
|------|------|-------------|
| `columns` | array | Column header strings |
| `rows` | array | Array of arrays — each inner array is one row |
| `variant` | string | Table style variant |
| `compact` | boolean | Reduced row height |
| `searchable` | boolean | Enable search bar above table |
| `searchPlaceholder` | string | Placeholder text for search input |
| `sortable` | boolean | Enable column sorting |
| `defaultSort` | object | Default sort config |
| `filters` | array | Column filter definitions |
| `selectionStatePath` | string | State path for row selection |

**Output dashboard limits:** 2 tables max, 12 rows combined. These limits do NOT apply to interactive UIs.

#### Chart
Data visualization. Use at most **1 Chart** per output dashboard.

| Prop | Type | Description |
|------|------|-------------|
| `variant` | string | **Required.** `line`, `bar`, `area`, `pie`, `donut`, `scatter`, `radar`, `radialBar`, `treemap`, `funnel`, `sankey`, `composed` |
| `data` | array | Data points — array of objects with one key per series (e.g., `[{ period, clicks, impressions }]`) |
| `series` | array | Series definitions for multi-series charts |
| `xKey` | string | Key name for X-axis values |
| `height` | number | Chart height in pixels |
| `nameKey` | string | Key for label in pie/donut charts |
| `valueKey` | string | Key for value in pie/donut charts |
| `colors` | array | Array of hex color strings |
| `nodes` | array | Node definitions for sankey charts |
| `links` | array | Link definitions for sankey charts |

**variant selection guide:**

| Data shape | variant |
|-----------|---------|
| Time series (clicks, rankings over months) | `line` or `area` |
| Category comparison (keywords by volume) | `bar` |
| Part-of-whole (intent distribution, ≤6 slices) | `pie` or `donut` |
| Two-variable correlation | `scatter` |
| Multi-axis performance | `radar` |
| Radial progress/score | `radialBar` |
| Hierarchical breakdown | `treemap` |
| Conversion stages | `funnel` |
| Flow between stages | `sankey` |
| Mixed chart types overlaid | `composed` |

---

### Interactive

#### Button
Actionable button. Supports `on.press` for triggering actions.

| Prop | Type | Description |
|------|------|-------------|
| `label` | string | Button text |
| `variant` | string | Style variant (`"default"`, `"outline"`, `"destructive"`) |
| `size` | string | `"sm"`, `"default"`, `"lg"` |
| `disabled` | boolean | Disabled state |

**on.press** — see Interactive Features section below.

#### Input
Text input field with optional validation.

| Prop | Type | Description |
|------|------|-------------|
| `label` | string | Input label |
| `name` | string | Field name |
| `placeholder` | string | Placeholder text |
| `type` | string | `"text"` or `"email"` only |
| `value` | string or `$bindState` | Current value or state binding |
| `checks` | array | Validation rules |

Use `{ "$bindState": "/path" }` on `value` for two-way binding.

#### DateInput
Date picker.

| Prop | Type | Description |
|------|------|-------------|
| `label` | string | Input label |
| `name` | string | Field name |
| `value` | string or `$bindState` | Date value or state binding |
| `min` | string | Minimum date |
| `max` | string | Maximum date |
| `disabled` | boolean | Disabled state |

#### DateTimeInput
Date and time picker.

Same props as DateInput plus time selection.

#### Textarea
Multi-line text input.

| Prop | Type | Description |
|------|------|-------------|
| `label` | string | Input label |
| `name` | string | Field name |
| `placeholder` | string | Placeholder text |
| `rows` | number | Visible row count |
| `value` | string or `$bindState` | Current value or state binding |
| `checks` | array | Validation rules |

---

### Structure

#### Accordion
Collapsible sections. Use for grouped findings (issues by category, keywords by cluster).

| Prop | Type | Description |
|------|------|-------------|
| `items` | array | Array of `{ title, description, children? }` items |
| `type` | string | `"single"` or `"multiple"` (how many open at once) |
| `title` | string | Accordion group title |
| `description` | string | Accordion group description |
| `maxWidth` | string | Maximum width |
| `centered` | boolean | Center alignment |

#### Separator
Horizontal divider. No props.

#### Badge
Inline status/risk indicator label with color.

| Prop | Type | Description |
|---|---|---|
| `label` | string | Badge text |
| `color` | string | Hex color (e.g., `"#16A34A"`) |

---

## Output Dashboard Constraints

For **SEO output dashboards** (Layer 1 of the three-layer output), enforce these limits
to maintain readability:

| Constraint | Limit |
|---|---|
| Metric components | Exactly 4 |
| Charts | 1 maximum |
| Tables | 2 maximum |
| Total table rows (combined) | 12 hard cap |
| Cell values | Short — digits + brief qualifier, no sentences |

These limits apply to output dashboards only. For interactive UIs (input forms,
progress trackers, explorable results), see the `interactive-ui` skill — no caps apply.

---

## Color Palette

| Color | Hex | Use for |
|---|---|---|
| Blue | `#2563EB` | Volume, traffic, positive metrics |
| Red | `#DC2626` | Difficulty, issues, drops, critical findings |
| Green | `#16A34A` | Growth, gains, passing checks, opportunities |
| Amber | `#D97706` | Warnings, medium-priority items |
| Slate | `#64748B` | Neutral labels, secondary data |

---

## Per-Workflow Dashboard Specs

After the root Stack and Heading, use the matching spec below for output dashboards.

### keyword-research
- **Metrics:** Best Target (`"keyword / KD XX"`), Highest Volume, Fastest Growing, Total Keywords
- **Chart:** `variant: "bar"`, title: "Top 10 Keywords by Volume"
- **Table 1:** Top keywords — Keyword, Vol, KD, CPC, Rank, Intent (8 rows max)
- **Table 2:** SERP snapshot — Keyword, SERP Type, Top Competitor, Cannibal (4 rows max)

### competitor-analysis / seo-gap-analysis
- **Metrics:** Traffic Gap, Keyword Gap, DR Delta, Top Opportunity
- **Chart:** `variant: "bar"`, title: "Keyword Gap by Topic Cluster"
- **Table 1:** Gap keywords — Keyword, Vol, Their Rank, Your Rank, Intent (8 rows)
- **Table 2:** Competitor top pages — URL, Traffic, Keywords (4 rows)

### drop-analysis
- **Metrics:** Traffic Drop %, Affected Pages, Likely Cause, Recovery Actions
- **Chart:** `variant: "line"`, title: "Organic Traffic Over Time"
- **Table 1:** Most-affected pages — URL, Before, After, Drop % (8 rows)
- **Table 2:** Ranking drops — Query, Before, After, Delta (4 rows)

### technical-seo
- **Metrics:** Issues Found, Critical Issues, Pages Crawled, CWV Status
- **Chart:** `variant: "bar"`, title: "Issues by Category"
- **Table 1:** Critical findings — Issue, URL, Priority, Fix (8 rows)
- **Table 2:** Priority roadmap — Action, Impact, Effort, Owner (4 rows)

### periodic-seo-report
- **Metrics:** Clicks Change, Avg Position, Impressions, Top Gainer
- **Chart:** `variant: "line"`, title: "Clicks + Impressions Trend" (multi-series)
- **Table 1:** Ranking changes — Query, Before, After, Delta (8 rows)
- **Table 2:** Action outcomes — Action, Page, Effect, Confidence (4 rows)

### link-building
- **Metrics:** Target Domains, Opportunities, Authority Gain, Priority Wins
- **Chart:** `variant: "bar"`, title: "Opportunities by Category"
- **Table 1:** Top link prospects — Domain, DR, Traffic, Relevance, Type (8 rows)
- **Table 2:** Link building timeline — Target, Action, Timeline, Priority (4 rows)

### ai-visibility
- **Metrics:** LLM Mentions, AI Engines, llms.txt Status, Top Cited URL
- **Chart:** `variant: "bar"`, title: "Competitor Mentions per AI Engine"
- **Table 1:** Competitor AI presence — Domain, ChatGPT, AIO, Gemini, Perplexity (8 rows)
- **Table 2:** AI Overview presence — Query, AIO Triggered, Target Cited (4 rows)

### topical-authority-mapping
- **Metrics:** Pillars, Coverage Score, Missing Topics, Quick Wins
- **Chart:** `variant: "radialBar"`, title: "Coverage Score per Pillar"
- **Table 1:** Content gap — Subtopic, Demand, Status, Action (8 rows)
- **Table 2:** Priority matrix — Page, Type, Action, Demand (4 rows)

### content-optimization
- **Metrics:** Keywords Validated, Keywords Placed, GSC Queries Retained, Density Issues
- **Chart:** `variant: "bar"`, title: "Keyword Placement Distribution"
- **Table 1:** Keyword placement map — Keyword, Placement, Exact Match (8 rows)
- **Table 2:** Removed keywords — Keyword, Reason (4 rows)

---

## Full Example: Keyword Research Dashboard

```json
{
  "root": "root",
  "elements": {
    "root": {
      "type": "Stack",
      "props": { "gap": 4 },
      "children": ["title", "kpi-grid", "chart", "h2-keywords", "table-keywords", "h2-serp", "table-serp", "next-steps"]
    },
    "title": {
      "type": "Heading",
      "props": { "text": "Keyword Research — running shoes (US)", "level": 1 }
    },
    "kpi-grid": {
      "type": "Grid",
      "props": { "columns": 4 },
      "children": ["m-target", "m-volume", "m-growing", "m-total"]
    },
    "m-target": { "type": "Metric", "props": { "label": "Best Target", "value": "trail running shoes / KD 41" } },
    "m-volume": { "type": "Metric", "props": { "label": "Highest Volume", "value": "40,500 / mo" } },
    "m-growing": { "type": "Metric", "props": { "label": "Fastest Growing", "value": "minimalist running shoes" } },
    "m-total": { "type": "Metric", "props": { "label": "Total Keywords", "value": "63" } },
    "chart": {
      "type": "Chart",
      "props": {
        "variant": "bar",
        "data": [
          { "keyword": "running shoes", "volume": 40500 },
          { "keyword": "trail running", "volume": 12100 },
          { "keyword": "best running shoes", "volume": 9900 },
          { "keyword": "minimalist shoes", "volume": 4400 },
          { "keyword": "flat feet shoes", "volume": 3600 }
        ],
        "xKey": "keyword",
        "colors": ["#2563EB"]
      }
    },
    "h2-keywords": {
      "type": "Heading",
      "props": { "text": "Top Keywords by Volume", "level": 2 }
    },
    "table-keywords": {
      "type": "Table",
      "props": {
        "columns": ["Keyword", "Vol", "KD", "CPC", "Rank", "Intent"],
        "rows": [
          ["running shoes", "40,500", "72", "$1.20", "#14", "Commercial"],
          ["trail running shoes", "12,100", "58", "$0.95", "-", "Commercial"],
          ["best running shoes", "9,900", "65", "$1.45", "#31", "Commercial"],
          ["minimalist running shoes", "4,400", "42", "$0.80", "-", "Commercial"],
          ["running shoes for flat feet", "3,600", "38", "$1.10", "-", "Commercial"]
        ],
        "compact": true,
        "sortable": true
      }
    },
    "h2-serp": {
      "type": "Heading",
      "props": { "text": "SERP Snapshot", "level": 2 }
    },
    "table-serp": {
      "type": "Table",
      "props": {
        "columns": ["Keyword", "SERP Type", "Top Competitor", "AIO"],
        "rows": [
          ["running shoes", "Commercial", "runnersworld.com", "Yes"],
          ["trail running shoes", "Commercial", "rei.com", "No"],
          ["best running shoes", "Commercial", "runnersworld.com", "Yes"],
          ["minimalist running shoes", "Informational", "healthline.com", "No"]
        ],
        "compact": true
      }
    },
    "next-steps": {
      "type": "Text",
      "props": { "text": "• Prioritize trail running shoes (KD 41, no current ranking — fastest path to page 1)\n• Cannibalization check needed for best running shoes vs. running shoes\n• Full 63-keyword dataset available in the markdown deliverable below" }
    }
  }
}
```

---

## Fallback

If `show_generative_ui` is unavailable, present results as structured markdown tables
instead, following the `charts-output` skill formatting conventions.

After the dashboard (or fallback tables), always add 2–4 sentences in plain chat
covering anything that didn't fit within the size constraints.
