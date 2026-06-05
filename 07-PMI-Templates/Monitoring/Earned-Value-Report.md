# Earned Value Management (EVM) Report

> Quantitative performance measurement integrating scope, schedule, and cost data. Provides objective assessment of project health and forecasts for completion.

---

| Field | Value |
|-------|-------|
| **Project Name** | [Project Name] |
| **Project Manager** | [Name] |
| **Reporting Period** | [Period ending YYYY-MM-DD] |
| **Date** | [YYYY-MM-DD] |
| **Version** | [1.0] |
| **Data Date** | [YYYY-MM-DD] |

---

## 1. Core EVM Metrics

### Base Measurements

| Metric | Abbreviation | Value | Source |
|--------|-------------|-------|--------|
| **Budget at Completion** | BAC | $[Amount] | Approved cost baseline |
| **Planned Value** | PV | $[Amount] | Planned work value through data date |
| **Earned Value** | EV | $[Amount] | Value of work actually completed |
| **Actual Cost** | AC | $[Amount] | Actual cost incurred |

### Variance Analysis

| Metric | Formula | Value | Interpretation |
|--------|---------|-------|---------------|
| **Cost Variance (CV)** | EV – AC | $[Amount] | [+ = under budget / – = over budget] |
| **Schedule Variance (SV)** | EV – PV | $[Amount] | [+ = ahead / – = behind schedule] |
| **Cost Variance % (CV%)** | CV / EV × 100 | [X%] | [% over/under budget] |
| **Schedule Variance % (SV%)** | SV / PV × 100 | [X%] | [% ahead/behind schedule] |

### Performance Indices

| Metric | Formula | Value | Interpretation |
|--------|---------|-------|---------------|
| **Cost Performance Index (CPI)** | EV / AC | [X.XX] | [>1 = under budget / <1 = over budget] |
| **Schedule Performance Index (SPI)** | EV / PV | [X.XX] | [>1 = ahead / <1 = behind] |

### Forecasting

| Metric | Formula | Value | Interpretation |
|--------|---------|-------|---------------|
| **Estimate at Completion (EAC)** | BAC / CPI | $[Amount] | Projected total cost at current performance |
| **EAC (Typical)** | AC + (BAC – EV) / CPI | $[Amount] | Assumes CPI continues |
| **EAC (Atypical)** | AC + (BAC – EV) | $[Amount] | Assumes original budget for remaining |
| **EAC (CPI × SPI)** | AC + (BAC – EV) / (CPI × SPI) | $[Amount] | Considers both cost and schedule |
| **Estimate to Complete (ETC)** | EAC – AC | $[Amount] | Cost to finish remaining work |
| **Variance at Completion (VAC)** | BAC – EAC | $[Amount] | [+ = under budget / – = over budget] |
| **To-Complete Performance Index (TCPI)** | (BAC – EV) / (BAC – AC) | [X.XX] | Required efficiency to finish on budget |

---

## 2. Performance Summary

### Status Indicators

| Metric | Value | Status | Threshold |
|--------|-------|--------|-----------|
| CPI | [X.XX] | 🟢 / 🟡 / 🔴 | 🟢 ≥ 0.95 | 🟡 0.90–0.94 | 🔴 < 0.90 |
| SPI | [X.XX] | 🟢 / 🟡 / 🔴 | 🟢 ≥ 0.95 | 🟡 0.90–0.94 | 🔴 < 0.90 |
| CV% | [X%] | 🟢 / 🟡 / 🔴 | 🟢 ≥ -5% | 🟡 -5% to -10% | 🔴 < -10% |
| SV% | [X%] | 🟢 / 🟡 / 🔴 | 🟢 ≥ -5% | 🟡 -5% to -10% | 🔴 < -10% |
| VAC | $[Amount] | 🟢 / 🟡 / 🔴 | 🟢 ≥ 0 | 🟡 -5% of BAC | 🔴 < -10% of BAC |
| TCPI | [X.XX] | 🟢 / 🟡 / 🔴 | 🟢 ≤ 1.05 | 🟡 1.05–1.15 | 🔴 > 1.15 |

### Narrative Assessment
[Paragraph interpreting the numbers — what do CPI/SPI tell us about project health? Is recovery feasible? What actions are needed?]

---

## 3. Trend Analysis

### CPI/SPI Trend (Last 6 Periods)
| Period | CPI | SPI | CV ($) | SV ($) |
|--------|-----|-----|--------|--------|
| [Period 1] | [X.XX] | [X.XX] | $[Amount] | $[Amount] |
| [Period 2] | [X.XX] | [X.XX] | $[Amount] | $[Amount] |
| [Period 3] | [X.XX] | [X.XX] | $[Amount] | $[Amount] |
| [Period 4] | [X.XX] | [X.XX] | $[Amount] | $[Amount] |
| [Period 5] | [X.XX] | [X.XX] | $[Amount] | $[Amount] |
| [Current] | [X.XX] | [X.XX] | $[Amount] | $[Amount] |

---

## 4. EAC Comparison

| EAC Method | Formula | Value | Assumption |
|------------|---------|-------|-----------|
| EAC (CPI) | BAC / CPI | $[Amount] | Current CPI will continue |
| EAC (CPI × SPI) | AC + (BAC–EV)/(CPI×SPI) | $[Amount] | Both cost and schedule inefficiency continue |
| EAC (Atypical) | AC + (BAC – EV) | $[Amount] | Variance was one-time; remaining work at budget |
| EAC (Bottom-Up) | AC + Re-estimate remaining | $[Amount] | New estimate of remaining work |
| **Selected EAC** | [Method used] | **$[Amount]** | **[Justification for selected method]** |

---

## 5. Formula Reference

| Formula | Calculation | Interpretation |
|---------|-------------|---------------|
| CV = EV – AC | Positive = under budget | How efficiently are we using cost? |
| SV = EV – PV | Positive = ahead of schedule | How efficiently are we using time? |
| CPI = EV / AC | > 1.0 = under budget | Cost efficiency ratio |
| SPI = EV / PV | > 1.0 = ahead of schedule | Schedule efficiency ratio |
| EAC = BAC / CPI | Forecast total cost | What will the project actually cost? |
| ETC = EAC – AC | Cost to finish | How much more will we spend? |
| VAC = BAC – EAC | Positive = budget surplus | Will we be over or under? |
| TCPI = (BAC–EV) / (BAC–AC) | > 1.0 = harder to achieve | How efficient must we be to finish on budget? |

---

## 6. Corrective Actions

| Finding | Action | Owner | Target Date |
|---------|--------|-------|------------|
| [Performance finding] | [Corrective action] | [Name] | [Date] |
| [Performance finding] | [Corrective action] | [Name] | [Date] |

---

*Prepared by: [Name] | Distribution: [List] | Next report: [Date]*
