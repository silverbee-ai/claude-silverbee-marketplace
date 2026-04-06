---
name: charts-output
description: >
  show_generative_ui Chart component reference and data formatting rules for
  Silverbee Cowork. Always consult this skill before producing any chart or
  data table (keyword tables, traffic tables, ranking tables, backlink tables,
  performance metrics, period comparisons). Ensures chart specs and data types
  are structured correctly for show_generative_ui rendering.
---

# Skill: Charts Output — show_generative_ui Reference

## Why this matters

The `show_generative_ui` Chart component renders directly in Cowork when the
data and spec follow the correct conventions. A wrong `variant`, mistyped
data key, or numeric cell with units breaks rendering. This skill encodes the
rules so every chart spec you produce renders correctly.

---

## Chart Component

The Chart component is a child of Stack. Use at most **1 Chart per dashboard**.

```json
{
  "type": "Chart",
  "variant": "line",
  "data": [
    { "period": "Jan", "value": 4200 },
    { "period": "Feb", "value": 5100 }
  ]
}
```

### Additional Chart props

| Prop | Purpose |
|------|---------|
| `variant` | Chart type: line, bar, area, pie, donut, scatter, radar, radialBar, treemap, funnel, sankey, composed |
| `data` | Array of data objects (use `series` and `xKey` props for multi-series) |
| `series` | Array of series definitions for multi-series charts |
| `xKey` | Key name for X-axis values |
| `height` | Chart height in pixels |
| `nameKey` | Key for label/name in pie/donut charts |
| `valueKey` | Key for value in pie/donut charts |
| `colors` | Array of hex color strings for series |
| `nodes` | Node definitions for sankey charts |
| `links` | Link definitions for sankey charts |

### variant options

| `variant` | Best for | Notes |
|---|---|---|
| `"line"` | Time-series trends: traffic, rankings, volume over time | Data must have a period/date key for X axis |
| `"area"` | Cumulative growth, filled trend emphasis | Same data shape as line |
| `"bar"` | Category comparisons: issue counts, intent distribution, gap volumes | Categorical X key, numeric Y |
| `"pie"` | Share breakdowns with ≤6 slices | Must have `label` and `value` keys |
| `"donut"` | Same as pie with center cutout | Same data shape as pie |
| `"scatter"` | Two-variable correlation | Requires x/y numeric pairs |
| `"radar"` | Multi-axis performance comparison | Categories as axes, values as radial distance |
| `"radialBar"` | Radial progress/score display | Circular progress indicators |
| `"treemap"` | Hierarchical breakdown | Nested category sizes |
| `"funnel"` | Conversion/funnel stages | Sequential stage values |
| `"sankey"` | Flow between stages | Requires `nodes` and `links` props |
| `"composed"` | Mixed chart types overlaid | Combine line + bar in one chart |

---

### Data format rules

1. **Numbers only in value fields.** No units, labels, or annotations inside data objects.
   - ✅ `{ "period": "Jan", "volume": 40500 }`
   - ❌ `{ "period": "Jan", "volume": "40,500 searches" }`

2. **Period/date keys come first** in each data object for time-series charts.
   - Use: `period`, `date`, `week`, `month`, `quarter`

3. **Key names become axis labels and legend entries** — keep them concise and human-readable.
   - ✅ `"clicks"`, `"impressions"`, `"volume"`, `"count"`
   - ❌ `"total_clicks_last_28d"`, `"avg_pos"`

4. **Missing/null values** — use `null` (not `0`, not `"N/A"`). The renderer will gap the line.

5. **Percentages** — express as decimal numbers.
   - Data: `{ "type": "CTR", "value": 3.4 }` (not `"3.4%"`)

6. **Pie charts** must use `label` and `value` keys:
   - `{ "label": "Informational", "value": 32 }`

---

### Data patterns by chart type

**Line / Area — traffic trend:**
```json
[
  { "period": "Week 1", "clicks": 1240, "impressions": 42000 },
  { "period": "Week 2", "clicks": 1380, "impressions": 48000 }
]
```

**Bar — issue counts by category:**
```json
[
  { "category": "Crawl", "count": 3 },
  { "category": "Index", "count": 2 },
  { "category": "Performance", "count": 4 }
]
```

**Line — multi-series (clicks + impressions):**
```json
[
  { "period": "Week 1", "clicks": 1240, "impressions": 42000 },
  { "period": "Week 2", "clicks": 1380, "impressions": 48000 }
]
```
Use `xKey: "period"` and `series: ["clicks", "impressions"]` with `colors: ["#2563EB", "#94a3b8"]` on the Chart component. Multi-series always uses a flat data array with multiple value keys — never `{ labels, datasets }`.

**Bar — gap opportunity by cluster:**
```json
[
  { "cluster": "Informational", "competitor": 1200, "you": 200 },
  { "cluster": "Commercial", "competitor": 800, "you": 450 }
]
```

**Pie — intent distribution:**
```json
[
  { "label": "Informational", "value": 32 },
  { "label": "Commercial", "value": 18 },
  { "label": "Transactional", "value": 9 }
]
```

---

## Table Component

```json
{
  "type": "Table",
  "striped": true,
  "compact": true,
  "columns": ["Keyword", "Vol", "KD", "Rank"],
  "rows": [
    ["running shoes", "40,500", "72", "#4"],
    ["trail running shoes", "12,100", "58", "-"]
  ]
}
```

### Table formatting rules

1. **Numeric columns contain numbers only.** No units inside cells.
   - ✅ `"40500"` or `"40,500"` — units belong in the column header
   - ❌ `"40,500 searches"` or `"~40k"`

2. **Column headers: ≤4 words, human-readable.** They become axis labels.
   - ✅ `"Vol"`, `"KD"`, `"CPC (USD)"`, `"Local Volume (US)"`
   - ❌ `"clicks_total_last_28d"`, `"avg_pos"`

3. **Missing values** — use `"—"` (em dash) in numeric columns, never `"no data"` or `"unavailable"`.

4. **Percentages** — cell value is the number, header indicates unit.
   - Header: `"CTR (%)"`, `"Change (%)"`
   - Cell: `"3.4"` not `"3.4%"`

5. **ISO/locale codes** — belong in the column header only, never in cells.
   - ✅ `"Local Volume (US)"` with cell `"2,400"`
   - ❌ `"2,400 US"`

6. **Size constraints:** 2 tables max per dashboard, 12 rows combined.

---

## Size constraints (hard limits)

| Element | Limit |
|---|---|
| Charts per dashboard | 1 |
| Tables per dashboard | 2 |
| Total table rows (combined) | 12 |
| Metric components | Exactly 4 |

---

## Color palette

Apply via data key naming or explicit color annotations in your spec description:

| Color | Hex | Use for |
|---|---|---|
| Blue | `#2563EB` | Volume, traffic, positive metrics |
| Red | `#DC2626` | Difficulty, issues, drops, critical findings |
| Green | `#16A34A` | Growth, gains, passing checks, opportunities |
| Amber | `#D97706` | Warnings, medium-priority items |

---

## Checklist before outputting any chart spec

- [ ] `variant` is a supported type: `line`, `area`, `bar`, `pie`, `donut`, `scatter`, `radar`, `radialBar`, `treemap`, `funnel`, `sankey`, `composed`
- [ ] Data objects contain numbers only (no units)
- [ ] Period/date key is first in each object (for time-series)
- [ ] Key names are ≤4 words, human-readable
- [ ] Pie charts use `label` and `value` keys
- [ ] Only 1 Chart in the full dashboard spec
- [ ] Table rows contain short cell values (no sentences)
- [ ] Combined table rows ≤ 12

---

## Executive Summary placement

Always precede the dashboard with a 3–5 bullet Executive Summary in the Text component or in plain chat. Bullets should highlight:
- Key trend or finding (with the number)
- Best and worst performer
- Anomaly or outlier
- Recommended action
