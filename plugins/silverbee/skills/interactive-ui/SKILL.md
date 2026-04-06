---
name: interactive-ui
description: >
  Interactive UI patterns for show_generative_ui in Cowork: input collection
  forms, workflow progress trackers, and explorable result views. Covers state
  bindings ($bindState), button actions (on.press), repeat rendering, and
  conditional visibility. Load this skill when building interactive UIs beyond
  output dashboards. For the component API reference, see react-wow-output.
---

# Skill: Interactive UI Patterns

## Purpose

Use this skill when you need interactive UI beyond a standard output dashboard —
input collection forms, workflow progress trackers, or explorable result views.

For the **component API reference** (all component types, props, spec format),
see the `react-wow-output` skill. This skill covers **how to combine components
into interactive experiences**.

---

## Interactive Features

### State and $bindState

The `state` object holds data referenced by components. Use `$bindState` on input
values for two-way binding — user changes update state automatically.

```json
{
  "root": "root",
  "elements": {
    "root": { "type": "Stack", "children": ["input-keyword"] },
    "input-keyword": {
      "type": "Input",
      "props": {
        "label": "Target keyword or URL",
        "placeholder": "e.g., running shoes",
        "value": { "$bindState": "/form/keyword" }
      }
    }
  },
  "state": {
    "form": { "keyword": "" }
  }
}
```

### on.press Actions

Button elements support `on.press` to trigger actions when clicked.

```json
{
  "submit-btn": {
    "type": "Button",
    "props": { "label": "Start Research", "variant": "default" },
    "on": {
      "press": {
        "action": "submitForm",
        "params": { "workflow": "keyword-research" },
        "confirm": "Start keyword research?",
        "onSuccess": { "action": "showResults" },
        "onError": { "action": "showError" }
      }
    }
  }
}
```

### repeat — List Rendering

Render an element for each item in a state array.

```json
{
  "step-item": {
    "type": "Card",
    "props": { "title": "Step name" },
    "repeat": { "statePath": "/workflow/steps", "key": "id" }
  }
}
```

### visible — Conditional Rendering

Show or hide elements based on conditions.

```json
{
  "error-alert": {
    "type": "Text",
    "props": { "text": "Authentication required", "variant": "error" },
    "visible": "/state/hasError"
  }
}
```

---

## Pattern 1: Input Collection Form

Use instead of `AskUserQuestion` when you need multi-field input with free text,
dates, and visual grouping. Falls back to `AskUserQuestion` for simple option selection.

```json
{
  "root": "form-card",
  "elements": {
    "form-card": {
      "type": "Card",
      "props": { "title": "Keyword Research Setup", "maxWidth": "500px", "centered": true },
      "children": ["input-target", "input-country", "input-range", "submit-btn"]
    },
    "input-target": {
      "type": "Input",
      "props": {
        "label": "Target keyword or page URL",
        "placeholder": "e.g., running shoes or https://example.com/page",
        "value": { "$bindState": "/form/target" }
      }
    },
    "input-country": {
      "type": "Input",
      "props": {
        "label": "Target country",
        "placeholder": "e.g., United States",
        "value": { "$bindState": "/form/country" }
      }
    },
    "input-range": {
      "type": "DateInput",
      "props": {
        "label": "Trend data start date",
        "value": { "$bindState": "/form/startDate" }
      }
    },
    "submit-btn": {
      "type": "Button",
      "props": { "label": "Start Research", "variant": "default" },
      "on": { "press": { "action": "startWorkflow", "params": { "type": "keyword-research" } } }
    }
  },
  "state": {
    "form": { "target": "", "country": "United States", "startDate": "" }
  }
}
```

---

## Pattern 2: Workflow Progress Tracker

Show live progress during multi-step workflows with Accordion steps and KPI metrics.

```json
{
  "root": "progress",
  "elements": {
    "progress": {
      "type": "Stack",
      "children": ["progress-title", "kpi-grid", "steps"]
    },
    "progress-title": {
      "type": "Heading",
      "props": { "text": "Keyword Research — running shoes (US)", "level": 1 }
    },
    "kpi-grid": {
      "type": "Grid",
      "props": { "columns": 4 },
      "children": ["m1", "m2", "m3", "m4"]
    },
    "m1": { "type": "Metric", "props": { "label": "Steps", "value": "3 of 6" } },
    "m2": { "type": "Metric", "props": { "label": "Status", "value": "Running", "trend": "up" } },
    "m3": { "type": "Metric", "props": { "label": "Keywords", "value": "84" } },
    "m4": { "type": "Metric", "props": { "label": "Source", "value": "Ahrefs" } },
    "steps": {
      "type": "Accordion",
      "props": {
        "type": "multiple",
        "items": [
          { "title": "1. Scope Lock — Done", "description": "ynet.co.il, Hebrew, IL market" },
          { "title": "2. Seed Keywords — Done", "description": "84 candidates from Ahrefs" },
          { "title": "3. Volume Enrichment — Running...", "description": "Fetching KD/CPC" },
          { "title": "4. Rankings — Pending", "description": "" }
        ]
      }
    }
  }
}
```

Call `show_generative_ui` again with updated data after each major phase completes.
Each call replaces the previous dashboard, giving the user a live progress view.

---

## Pattern 3: Explorable Results

Use Accordion for grouped findings and searchable/sortable Tables for large datasets.

```json
{
  "root": "results",
  "elements": {
    "results": {
      "type": "Stack",
      "children": ["title", "findings", "full-table"]
    },
    "title": {
      "type": "Heading",
      "props": { "text": "Technical Audit — example.com", "level": 1 }
    },
    "findings": {
      "type": "Accordion",
      "props": {
        "type": "multiple",
        "items": [
          { "title": "Crawl Issues (3)", "description": "Blocked resources, redirect chains, broken links" },
          { "title": "Indexation Issues (2)", "description": "Noindex on key pages, thin content" },
          { "title": "Performance Issues (4)", "description": "LCP failures, render-blocking resources" },
          { "title": "Schema Issues (1)", "description": "Missing breadcrumb markup" }
        ]
      }
    },
    "full-table": {
      "type": "Table",
      "props": {
        "columns": ["Issue", "URL", "Priority", "Fix"],
        "rows": [
          ["Blocked CSS", "/assets/style.css", "High", "Update robots.txt"],
          ["Redirect chain", "/old-page", "High", "Direct to final URL"],
          ["LCP > 4s", "/homepage", "Critical", "Optimize hero image"]
        ],
        "compact": true,
        "searchable": true,
        "searchPlaceholder": "Search issues...",
        "sortable": true
      }
    }
  }
}
```

---

## When to Use Each Approach

| Need | Tool |
|------|------|
| Simple option selection (1–3 questions) | `AskUserQuestion` |
| Multi-field input with free text, dates, visual grouping | `show_generative_ui` form (Pattern 1) |
| Live workflow progress with step tracking | `show_generative_ui` progress tracker (Pattern 2) |
| Grouped findings with drill-down | `show_generative_ui` explorable results (Pattern 3) |
| Standard SEO output dashboard | `show_generative_ui` per `react-wow-output` specs |
