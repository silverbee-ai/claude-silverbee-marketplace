---
name: run-workflow
description: Execute a named Silverbee workflow step-by-step with live progress. Lists available workflows if no name is given.
---

Run Silverbee workflow: $ARGUMENTS

## Before running (if no workflow name provided)

Call `list_available_apps` to discover available integrations and actions, then use `AskUserQuestion` to ask the user which workflow to run:

```json
{
  "questions": [
    {
      "question": "Which workflow would you like to run?",
      "header": "Workflow",
      "options": [
        { "label": "I'll type the workflow name", "description": "Enter the name in chat" }
      ],
      "multiSelect": false
    }
  ]
}
```

Populate the `options` array dynamically from the `list_available_apps` results before calling `AskUserQuestion`. Present discovered integrations as selectable options.

After the user selects a workflow, confirm the choice and **wait for go-ahead** before executing.

---

## Execution

If a workflow name or task is provided:
1. Call `get_instructions` to understand the agent's capabilities
2. Break the task into discrete steps
3. Execute each step using the appropriate tool (`run_action`, `run_multi_actions`, or `run_action_batch`)
4. Report progress after each step
5. On any app-specific error, try the supervisor's fallback chain ("Step 3") before stopping. On connection/auth errors (all tools failing), follow the supervisor's "Tool call errors" section — show the login URL and stop.

---

## Tool execution pattern

1. `list_available_apps` — confirm which integrations are connected
2. `search_actions(query)` or `list_actions(app_name)` — find the right operation
3. `run_action(app_name, operation_id, input)` — execute

**MANDATORY — parallel execution:** Batch all independent queries into a single `run_multi_actions` call. Never call `run_action` in a sequential loop — that is a performance bug.

---

## Output Format

For workflows that produce structured data, use `show_generative_ui` to display
an interactive progress dashboard directly in chat. Use the `{ root, elements, state }`
spec format from `react-wow-output`. For advanced interactive patterns (forms,
progress trackers with state bindings), see the `interactive-ui` skill.

### Progress dashboard spec

```json
{
  "root": "root",
  "elements": {
    "root": {
      "type": "Stack",
      "children": ["title", "kpi-grid", "steps-accordion", "results-preview"]
    },
    "title": {
      "type": "Heading",
      "props": { "text": "Workflow: [Name]", "level": 1 }
    },
    "kpi-grid": {
      "type": "Grid",
      "props": { "columns": 4 },
      "children": ["metric-progress", "metric-status", "metric-source", "metric-records"]
    },
    "metric-progress": {
      "type": "Metric",
      "props": { "label": "Steps Completed", "value": "X of Y" }
    },
    "metric-status": {
      "type": "Metric",
      "props": { "label": "Status", "value": "Running", "trend": "up" }
    },
    "metric-source": {
      "type": "Metric",
      "props": { "label": "Data Source", "value": "app name" }
    },
    "metric-records": {
      "type": "Metric",
      "props": { "label": "Records", "value": "XX" }
    },
    "steps-accordion": {
      "type": "Accordion",
      "props": {
        "type": "multiple",
        "items": [
          { "title": "1. Scope Definition — Done", "description": "Locked scope for domain.com, IL market" },
          { "title": "2. Keyword Candidates — Done", "description": "84 keywords from Ahrefs" },
          { "title": "3. Volume Enrichment — Running...", "description": "Fetching KD/CPC for 84 keywords" },
          { "title": "4. Rankings — Pending", "description": "" }
        ]
      }
    },
    "results-preview": {
      "type": "Table",
      "props": {
        "columns": ["Step", "Status", "Key Output"],
        "rows": [
          ["Scope Lock", "Done", "domain.com — IL market"],
          ["Seed Keywords", "Done", "84 candidates"],
          ["Enrichment", "Running", "..."]
        ],
        "compact": true,
        "searchable": false
      }
    }
  }
}
```

### When to update the dashboard

Call `show_generative_ui` again with updated data after each major phase completes.
Each call replaces the previous dashboard, giving the user a live progress view.

### Final output

When the workflow completes, switch from the progress dashboard to the full
three-layer output per `seo-output-formatter`: Layer 1 (final dashboard),
Layer 2 (HTML report), Layer 3 (full markdown).

If `show_generative_ui` is unavailable, report progress as structured markdown after each step.
