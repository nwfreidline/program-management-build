# Automated Schedule Generation Pipeline

> How to build a Python pipeline that converts raw work order data into a fully-scheduled maintenance calendar.

---

## Architecture

```
Data Source (EAM/CMMS/Excel)
        │
        ▼
┌──────────────────┐
│  data_pull.py    │  ← Extract work orders for target year
└──────────────────┘
        │
        ▼
┌──────────────────┐
│  compliance.py   │  ← Calculate compliance windows from frequencies
└──────────────────┘
        │
        ▼
┌──────────────────┐
│  scheduler.py    │  ← Apply scheduling rules (level-load, blackouts, weekdays)
└──────────────────┘
        │
        ▼
┌──────────────────────────────────┐
│  output_generator.py             │  ← Generate outputs
│  ├── Excel (master + per-vendor) │
│  ├── MS Project XML              │
│  └── 90-Day Outlook              │
└──────────────────────────────────┘
```

---

## Pipeline Components

### 1. Data Pull (`data_pull.py`)

**Input:** Connection to your maintenance management system (EAM, SAP PM, Maximo, ServiceNow, or just an Excel export)

**Output:** Standardized DataFrame with columns:
- `work_order_id` — Unique identifier
- `site` — Location code
- `program` — Maintenance program category
- `vendor` — Vendor name
- `frequency` — Frequency code (1M, 3M, 6M, 12M, etc.)
- `last_completed` — Date of last completion
- `due_date` — Next due date
- `description` — Work scope description
- `estimated_hours` — Labor estimate

**Adaptation points:**
- Replace the data source query with your system's API/export
- Map your system's field names to the standard columns above

### 2. Compliance Calculator (`compliance.py`)

**Input:** DataFrame with `due_date` and `frequency` columns

**Output:** Same DataFrame with added `compliance_start` and `compliance_end` columns

**Logic:**
```python
BUFFER_DAYS = {
    "1M": 3, "2M": 6, "3M": 10, "4M": 12,
    "6M": 18, "12M": 37, "24M": 37, "36M": 55,
}

def calculate_compliance_window(due_date, frequency):
    buffer = BUFFER_DAYS.get(frequency, 10)
    return (due_date - timedelta(days=buffer),
            due_date + timedelta(days=buffer))
```

### 3. Scheduler (`scheduler.py`)

**Input:** DataFrame with compliance windows

**Output:** DataFrame with `scheduled_date` assigned within each compliance window

**Rules applied:**
1. No weekends (shift to nearest weekday)
2. No blackout dates (holidays, standfast periods)
3. Level-loading: distribute evenly across available days
4. Vendor capacity: max N jobs per vendor per day
5. Site conflicts: max N jobs per site per day

### 4. Output Generator (`output_generator.py`)

Produces final deliverables:

| Output | Library | Purpose |
|--------|---------|---------|
| Master Excel | `openpyxl` | Full schedule with all programs |
| Per-Vendor Excel | `openpyxl` | Filtered view for vendor coordination |
| 90-Day Outlook | `openpyxl` | Rolling view for planning meetings |
| MS Project XML | `xml.etree` | Gantt chart with dependencies (optional) |

---

## Folder Structure

```
schedule-pipeline/
├── pipeline.py          # Main orchestrator (runs all steps)
├── data_pull.py         # Data extraction
├── compliance.py        # Window calculation
├── scheduler.py         # Scheduling algorithm
├── output_generator.py  # File generation
├── config.json          # Site mappings, vendor lists, blackout dates
├── requirements.txt     # pandas, openpyxl
└── output/
    ├── Master_Schedule_YYYY.xlsx
    ├── 90_Day_Outlook.xlsx
    └── Vendor_Views/
        ├── Vendor_A.xlsx
        └── Vendor_B.xlsx
```

---

## Year-Over-Year Rollforward

To generate next year's schedule from this year's:

1. Pull the current year's completion data
2. Shift all due dates forward by their frequency period
3. Recalculate compliance windows
4. Apply scheduling rules for the new calendar year
5. Flag any work orders that changed frequency or vendor

This eliminates rebuilding the schedule from scratch annually.

---

## Getting Started

1. Export your current maintenance data to Excel (one row per work order)
2. Map columns to the standard format above
3. Start with just the compliance calculator — that alone provides value
4. Add the scheduling algorithm when you're managing 100+ items
5. Add automated output generation when you're managing 500+ items

The key insight: **you don't need to automate everything at once.** Start with what saves you the most manual work and build from there.
