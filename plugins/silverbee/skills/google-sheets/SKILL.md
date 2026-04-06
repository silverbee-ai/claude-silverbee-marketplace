---
name: google-sheets
description: Plan and orchestrate Google Sheets workflows — creating spreadsheets, writing data, formatting, and structuring output for SEO reports and analysis.
---

# Google Sheets tool - overview

## What This Is For
This guide helps you plan workflows to create a plan with a Google Sheets tool. Think of yourself as the architect — you decide WHAT needs to happen and in what order. The executor agent will handle the actual tool calls.

---

## When to Use Sheets

**Use Sheets when the user wants:**
- A spreadsheet (they'll say "create a sheet", "export to sheets", "track in Google Sheets", "read my data and analyze it")
- Something they can share with their team
- Data that lives beyond this conversation

**Don't use Sheets when:**
- User just wants to see results in chat → show a markdown table instead
- It's a one-time thing they don't need to keep
- They didn't ask for a spreadsheet

---

## The 3 Golden Rules

### Rule 1: Create First, Write Second
**Never** try to write data and create a spreadsheet at the same time.

✅ **Do this:**
```
Stage 1: Create the spreadsheet
Stage 2: Write data to it (depends on Stage 1)
```

❌ **Not this:**
```
Stage 1: Create spreadsheet AND write data (both together)
```

**Why?** Writing needs the spreadsheet ID from the create step. They can't happen in parallel.

---

### Rule 2: Find Out Sheet Names Before Writing
If the user gives you an existing spreadsheet ID but you don't know the sheet names, **always** discover them first.

✅ **Do this:**
```
Stage 1: Get spreadsheet info (discover sheet names)
Stage 2: Write/append data (depends on Stage 1)
```

❌ **Not this:**
```
Stage 1: Write to "Sheet1" (guessing the name)
```

**Why?** The sheet might be called "Data", "Sheet 4" (with space), or something custom. Agents guess wrong.

---

### Rule 3: Different Data = Different Sheets
When you have different types of data, put them on separate sheets.

✅ **Do this:**
```
Create with multiple sheets:
- "SEO Metadata" sheet
- "Performance Data" sheet
- "Issues Found" sheet
```

❌ **Not this:**
```
Put metadata in columns A-C, performance in E-G, issues in I-K (all same sheet)
```

**Exception:** If it's a visual comparison table (like competitor A vs B vs C side-by-side), same sheet is OK.

---

## How to Pick the Right Tool

**For writing data:**
- Writing to ONE area? → Use **values.update**
- Writing to MULTIPLE areas at once? → Use **values.batchUpdate**
- Adding rows to existing data? → Use **values.append**

**For structure/formatting:**
- Need to add charts, formatting, or modify structure? → Use **spreadsheets.batchUpdate**

**For discovery:**
- Don't know what sheets exist? → Use **spreadsheets.get** first

---

## Common SEO Workflows

### Workflow 1: Technical SEO Audit → Report
**User says:** "Run a technical audit on my site and create a Google Sheet with findings"

**How to plan:**
```
Stage 1: Collect Data
  - Scrape homepage metadata
  - Scrape page content
  - Check robots.txt
  - Get Core Web Vitals
  (All can run in parallel)

Stage 2: Create Report
  - Create spreadsheet with 3 sheets: Metadata, Performance, Issues
  - Must wait for ALL Stage 1 tasks to finish

Stage 3: Write Findings
  - Write to all 3 sheets at once using batchUpdate
  - Depends on Stage 2 (needs the spreadsheet ID)
```

**Key point:** Sheets comes LAST. Collect all data first, then export to sheets.

---

### Workflow 2: Search Console → Dashboard
**User says:** "Get my top 20 pages from Search Console and put them in a spreadsheet"

**How to plan:**
```
Stage 1: Get Data
  - Query Search Console for top 20 pages

Stage 2: Export
  - Create spreadsheet (depends on Stage 1 - needs data first)
  - Write the GSC data (depends on create - needs spreadsheet ID)
```

**Key point:** Single table = use values.update, not batchUpdate.

---

### Workflow 3: Multi-Source Report
**User says:** "Create a weekly report with Analytics, Search Console, and PageSpeed data in one spreadsheet"

**How to plan:**
```
Stage 1: Collect Everything (Parallel)
  - Get Analytics data
  - Get Search Console data
  - Get PageSpeed data
  (All independent, can run together)

Stage 2: Create Spreadsheet
  - Create with 3 separate sheets (one per data source)
  - Must wait for ALL Stage 1 tasks

Stage 3: Write All Data
  - Write to all 3 sheets using batchUpdate
  - Depends on Stage 2
```

**Key point:** Multiple data sources = separate sheets, not same sheet.

---

### Workflow 4: Competitor Analysis
**User says:** "Scrape 5 competitor sites, analyze them, and create a comparison sheet"

**How to plan:**
```
Stage 1: Scrape All Sites (Parallel)
  - Scrape competitor 1
  - Scrape competitor 2
  - Scrape competitor 3
  - Scrape competitor 4
  - Scrape competitor 5

Stage 2: Analyze
  - Process and compare data
  - Depends on ALL scraping tasks

Stage 3: Export
  - Create spreadsheet
  - Write comparison data
  - Both depend on Stage 2
```

**Key point:** If data needs processing, add a processing stage between collection and export.

---

## When Sheets Works with Other Tools

**The Pattern:**
1. Collect data (scraping, APIs, etc.)
2. Process it if needed
3. Export to Sheets

**Sheets is almost always the LAST thing.**

**Example - SEO Audit:**
```
Stage 1: Data Collection
  - Scrape homepage
  - Check robots.txt
  - Get Core Web Vitals

Stage 2: Export
  - Create spreadsheet (depends on ALL of Stage 1)
  - Write findings (depends on create)
```

**Critical:** The create task must wait for ALL data to be ready. Don't create the sheet before you have the data.

---

## Common Mistakes & How to Fix Them

### Mistake: Creating sheet too early
❌ **Wrong:**
```
Stage 1: Create spreadsheet, scrape website (together)
Stage 2: Write data
```

✅ **Right:**
```
Stage 1: Scrape website
Stage 2: Create spreadsheet, then write data
```

---

### Mistake: Forgetting dependencies
❌ **Wrong:**
```
Stage 2:
  - write_data (depends only on create_sheet)
```

✅ **Right:**
```
Stage 2:
  - write_data (depends on create_sheet AND scrape_data)
```

**Why?** The write task needs both the spreadsheet ID AND the data from scraping.

---

### Mistake: Mixing data types in one sheet
❌ **Wrong:**
```
Create one sheet, write:
  - Summary in columns A-C
  - Raw data in columns E-Z
```

✅ **Right:**
```
Create with 2 sheets:
  - "Summary" sheet
  - "Raw Data" sheet
```

---

## Quick Decision Guide

**"Should I create a new spreadsheet or use an existing one?"**
- User says "create a spreadsheet" → New one
- User gives you a spreadsheet ID → Existing one

**"Do I need to discover sheet names?"**
- If it's a NEW spreadsheet you're creating → No, you control the names
- If it's an EXISTING spreadsheet and user didn't tell you the sheet names → Yes, use spreadsheets.get first

**"Which write tool should I use?"**
- Writing to one area → values.update
- Writing to multiple areas → values.batchUpdate
- Adding rows to a table → values.append

**"When do I create the spreadsheet?"**
- AFTER all data is collected
- BEFORE writing data to it

**"Do I need separate sheets?"**
- Different data types (metadata vs performance vs issues) → Yes
- Same type of data, just more rows → No
- Visual comparison table → Maybe not (use judgment)

---

## Remember

1. **Create before write** — Always. (if the user didnt give you a specific sheet to write to)
2. **Discover before write** — When structure is unknown
3. **Different data, different sheets** — Usually
4. **Collect before export** — When working with other tools
5. **State your dependencies** — So executor knows the order

---

**Last Updated:** 2025-02-18
**For:** Planner Agent (SEO Agent context)
