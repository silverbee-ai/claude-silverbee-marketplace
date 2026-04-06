# Silverbee — SEO AI Assistant for Claude

AI-powered SEO assistant plugin for Claude Code and Cowork. Gives Claude live access to Google Search Console, Ahrefs, DataForSEO, Google Analytics, Web Vitals, and 10+ other data sources — plus 15 specialized skills for keyword research, technical audits, content optimization, competitor analysis, and more.

## Install

```bash
claude plugin install silverbee@claude-plugins-official
```

Then authenticate with the Silverbee MCP server:

1. In Claude Code, type `/mcp`
2. Follow the authentication prompt

That's it — all SEO tools are now available.

**Local development:**

```bash
claude --plugin-dir ./sources/claude-plugin
```

## Commands

| Command | What it does |
|---------|-------------|
| `/silverbee:keyword-research <url or topic>` | End-to-end keyword research with Ahrefs data, SERP validation, cannibalization check |
| `/silverbee:seo-audit <domain>` | Technical SEO audit — crawlability, indexation, Core Web Vitals, schema, redirects |
| `/silverbee:content-optimize <url> [keywords]` | Content optimization with keyword embedding, density control, metadata rules |
| `/silverbee:competitor-analysis <domain> vs <competitor>` | Keyword, content, and backlink gap analysis |
| `/silverbee:seo-report <domain> [period]` | Periodic SEO performance report with GSC/GA data |
| `/silverbee:drop-analysis <domain>` | Traffic or ranking drop diagnosis with root cause analysis |
| `/silverbee:run-workflow [name]` | Execute a Silverbee workflow; lists available workflows if no name given |

You can also just describe what you need in plain language — the plugin's skills activate automatically based on context.

## Connected Tools

When the Silverbee MCP server is running, Claude has access to:

| Tool | Data |
|------|------|
| Google Search Console | Organic performance, query rankings, index coverage |
| Google Analytics | Traffic, sessions, conversions |
| Ahrefs | Keywords, backlinks, SERP data, site explorer |
| DataForSEO | Search volume, keyword difficulty, SERP features |
| Web Vitals | Core Web Vitals (LCP, INP, CLS) |
| Tavily Search | Real-time web search |
| Scrapfly | Full-page scraping with JS rendering |
| Google Trends | Demand signals, seasonal trends |
| Slack | Post reports to Slack channels |
| Archive.org | Historical page snapshots |
| + more | Metadata, inner text, and structured data scrapers |

## Interactive Output

In Cowork, deliverables are rendered as **interactive React dashboards** with:
- Sortable, filterable data tables
- Charts (bar, line, pie) via Recharts
- KPI cards with color-coded severity
- Keyword difficulty and intent badges
- Expandable issue cards for audit findings

In Claude Code CLI, the same data is presented as clean markdown tables.

## Skills

Skills load automatically when relevant. The full set:

| Skill | Purpose |
|-------|---------|
| keyword-research | Full keyword research protocol with scope locking |
| content-optimization | SEO content rewrite with keyword validation |
| technical-seo | Technical audit across 7 dimensions |
| competitor-analysis | Feature and content gap analysis |
| drop-analysis | Traffic/ranking drop diagnosis |
| link-building | Link prospecting and outreach |
| gsc-query-planning | GSC data extraction strategy |
| ai-visibility | AI Overview and generative search optimization |
| seo-gap-analysis | Opportunity gap identification |
| topical-authority-mapping | Topic cluster and pillar strategy |
| periodic-seo-report | Structured reporting protocol |
| charts-output | Table formatting for chart rendering |
| react-wow-output | Interactive JSX component templates |
| platform-awareness | Plugin capability reference |

## Requirements

- **Node.js** (v18+) — required for the MCP proxy
- **Claude Code** or **Cowork** — the plugin works in both environments

## Troubleshooting

**MCP tools not loading:**
- Check that Node.js is installed: `node --version`
- The plugin verifies Node.js availability on session start

**Tools return auth errors:**
- Some tools (GSC, Google Analytics, Slack) require OAuth setup
- The plugin will tell you which tool needs connecting and how

**No data returned:**
- Verify the target domain has data in the connected tools
- Check API quotas for external services (Ahrefs, DataForSEO)

## License

Proprietary — Copyright (c) 2024-2026 Silverbee AI. All rights reserved. See [LICENSE](LICENSE) for details.
