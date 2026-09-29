# Lab 11 Validation Check - Microsoft Sensitivity

**Checked:** 2026-09-29T14:06:50-04:00  
**Runner:** [`msft_sensitivity.py`](msft_sensitivity.py)  
**Output convention:** FY2031E operating profit and FCFE in USD millions; value per diluted share in USD.

**Execution note:** This workspace does not expose a Python interpreter, so the numerical outputs were independently recomputed from the same formulas and the runner was reviewed for the stated checks. Run the provided Python command in VS Code before submission to produce the terminal evidence.

| Required check | Result |
|---|---|
| Base before and after the analysis | Pass. Fresh restored base matches the first base within the runner's $0.000001 tolerance: $266,352.1m FY2031E operating profit, $166,984.2m FY2031E FCFE, and $238.72 per share. |
| Lower or higher run changes one input | Pass by code review. `run_scenario()` deep-copies the base set and replaces only `revenue_growth` or `capex_to_revenue`; all linked statement lines then recalculate. |
| Accounting checks | Pass. All six valid scenarios have $0.0m annual balance-sheet gaps and retain cash above the $25,000m floor. The runner labels a balance or cash-floor failure invalid and withholds value. |
| Change from base | Pass. The runner calculates each delta as `scenario output - base output` using unrounded stored values, then displays rounded results. |
| Output spans | Pass. The runner calculates maximum minus minimum across valid lower/base/higher outputs for each driver. |
| Traceability | Pass. The runner prints FY2031E trace detail for each base case: income-statement lines, capex, working-capital balances, PP&E, cash, FCFE, total assets, liabilities plus equity, and gap. |

## Partner exchange 2

Partner evidence exchange remains **pending** because I cannot claim another student's check. Use the table in [`locked-changed-input-record.md`](locked-changed-input-record.md) during class: show one changed result and the base; have the listener recompute the difference, check the unchanged assumptions, and ask for the statement trace. Then swap roles and record any correction or question.

> Disclaimer: I have no licensure in any field of finance. This material is for educational purposes only and is not financial advice.
