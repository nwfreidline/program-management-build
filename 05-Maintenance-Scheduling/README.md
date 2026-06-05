# Layer 5: Maintenance Scheduling

> Tools and templates for managing recurring preventative maintenance programs, vendor coordination, and compliance-window scheduling.

---

## Who Needs This

Anyone managing:
- Recurring vendor maintenance (HVAC, electrical, fire systems, etc.)
- Compliance-driven inspection schedules
- Multiple vendors across multiple locations
- Seasonal or frequency-based work programs

---

## What's Included

### Schedule Templates

Pre-built Excel templates for common scheduling patterns:

| Template | Purpose |
|----------|---------|
| `Schedule-Templates/Master-Schedule-Template.xlsx` | Full-year schedule with all programs, sites, and vendors |
| `Schedule-Templates/90-Day-Outlook-Template.xlsx` | Rolling 90-day view for vendor coordination |
| `Schedule-Templates/Vendor-Maintenance-Outlook.xlsx` | Per-vendor view for sharing externally |

### Pipeline Pattern Documentation

| Document | Purpose |
|----------|---------|
| `Pipeline-Pattern.md` | How to build an automated schedule generation pipeline |
| `Compliance-Windows.md` | How to calculate compliance windows from frequency codes |

---

## Quick Start

### 1. Choose Your Scheduling Approach

| Approach | Complexity | Best For |
|----------|-----------|----------|
| **Excel Templates** | Low | < 50 recurring tasks, 1-3 vendors |
| **MS Project** | Medium | 50-500 tasks, multiple programs |
| **Automated Pipeline** | High | 500+ tasks, data-driven generation |

### 2. Set Up the Master Schedule

1. Open `Schedule-Templates/Master-Schedule-Template.xlsx`
2. Fill in your programs, sites, and vendors on the Config tab
3. Enter your work orders on the Schedule tab
4. The 90-Day Outlook tab auto-filters to upcoming work

### 3. Generate Vendor Views

Use the "Per-Vendor" tab to filter the master schedule by vendor, then export/share with each vendor for coordination.

---

## Compliance Window Calculation

For inspection programs driven by frequency (monthly, quarterly, annual), each work order has a **compliance window** — the acceptable date range for completion.

### Formula

```
Compliance Start = Due Date - Buffer Days
Compliance End   = Due Date + Buffer Days
```

### Standard Buffer Table

| Frequency | Buffer (±Days) | Total Window |
|-----------|---------------|--------------|
| Monthly (1M) | ±3 | 6 days |
| Bi-Monthly (2M) | ±6 | 12 days |
| Quarterly (3M) | ±10 | 20 days |
| Semi-Annual (6M) | ±18 | 36 days |
| Annual (12M) | ±37 | 74 days |
| Biennial (24M) | ±37 | 74 days |
| Triennial (36M) | ±55 | 110 days |

**General pattern:** ~10% of cycle length each side, with floor of ±1 day and cap of ±55 days.

---

## Scheduling Rules (Best Practices)

1. **No work on weekends** unless explicitly authorized
2. **Avoid critical operations days** — identify blackout periods upfront
3. **Lead time for vendor coordination** — submit work requests ≥14 days ahead
4. **Monthly review cadence** — review the schedule 6 weeks in advance
5. **Level load** — distribute work evenly across the month; avoid overloading any single week
6. **Compliance alignment** — schedule start dates within the compliance window
7. **Vendor capacity** — coordinate with vendors to avoid scheduling conflicts

---

## Templates Included

The Excel files in `Schedule-Templates/` are stripped reference versions showing structure and formulas. Customize them for your specific programs:

### Master Schedule Columns
| Column | Purpose |
|--------|---------|
| Program | Which maintenance program (e.g., Fire System, HVAC) |
| Site/Location | Where the work happens |
| Vendor | Who performs the work |
| Frequency | How often (1M, 3M, 6M, 12M, etc.) |
| Due Date | Next scheduled due date |
| Compliance Start | Earliest acceptable completion date |
| Compliance End | Latest acceptable completion date |
| Scheduled Date | Actual scheduled date (within compliance window) |
| Status | Scheduled / Complete / Overdue / Pending |
| Notes | Special instructions, access requirements, etc. |

### 90-Day Outlook Columns
| Column | Purpose |
|--------|---------|
| Week Of | Week bucket for the upcoming work |
| Program | Maintenance program |
| Site | Location |
| Vendor | Vendor name |
| Scope Summary | Brief description of work |
| Status | Confirmed / Pending / Needs MCM |

---

## Advanced: Building an Automated Pipeline

For organizations with 500+ recurring work orders, manual scheduling becomes unsustainable. See `Pipeline-Pattern.md` for how to build a Python pipeline that:

1. Pulls work order data from your maintenance management system
2. Applies compliance window formulas automatically
3. Generates scheduling outputs (Excel, MS Project XML, or both)
4. Produces per-vendor views for coordination
5. Supports year-over-year rollforward with date shifting

The pipeline pattern is documented at a conceptual level — you'll need to adapt the data source connection to whatever system you use (SAP, Maximo, ServiceNow, spreadsheets, etc.).
