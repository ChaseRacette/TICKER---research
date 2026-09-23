# Lab 09 - ABG Three-Statement Pro-Forma

## Purpose and model file

This is the five-year, three-statement training model for Asbury Automotive Group (ABG). The editable, standard-library Python model is [`proforma.py`](../../proforma.py). It projects FY2026E through FY2030E, computes cash last, checks that every projected balance sheet balances, and only then calculates equity value per share.

Run it from the repository root:

```powershell
python proforma.py
```

All dollar values in the model are USD millions except per-share value and shares outstanding.

## Three judgments that carry the ABG valuation

1. **Organic revenue growth (1.8% each year):** revenue is the starting point for profit and for inventory needed to support sales.
2. **SG&A as a percent of gross profit (66.5% to 64.5%):** this is the largest operating-profitability judgment in the base case. Lower SG&A per dollar of gross profit raises operating income and FCFE.
3. **Capital and financing policy:** inventory days, floor-plan borrowing, capex, impairment, debt repayment, and buybacks determine how much reported profit becomes cash available to equity holders.

Cash is calculated last because it is the result of the income statement, balance-sheet changes, investment, and financing - not a plug. A balance sheet that does not balance indicates a broken link or formula, not a forecast that can be valued.

## Inputs and labels

| Input | Base-case value | Label | Reason |
|---|---:|---|---|
| FY2025 revenue | $17,999.0m | History | Opening case balance/income statement input |
| FY2025 inventory | $2,135.8m | History | Opening balance sheet input |
| FY2025 PP&E | $3,070.4m | History | Opening balance sheet input |
| FY2025 floor plan | $2,027.0m | History | Opening financing balance |
| Organic growth | 1.8% | Judgment | Base-case sales assumption |
| Gross margin | 17.05% | Judgment | Base-case profitability assumption |
| SG&A / gross profit | 66.5%, 65.5%, then 64.5% | Judgment | Profitability-recovery path |
| Depreciation / opening PP&E | 82.4 / 3,070.4 | History | Opening-year relationship |
| Inventory days | 2,135.8 / (17,999.0 - 3,071.7) x 365 | History | Ties inventory to cost of goods sold |
| Floor plan / inventory | 2,027.0 / 2,135.8 | History | Ties inventory financing to inventory |
| Capex | $250.0m yearly | Guidance | Case base-case assumption |
| Impairment | $120.0m yearly | Judgment | Noncash case assumption |
| Tax rate | 25.5% | Judgment | Applied only to positive pretax income |
| Debt repayment / buyback | $150.0m / $150.0m yearly | Judgment | Financing and capital-return policy |
| Cost of equity / terminal growth | 10.0% / 2.5% | Judgment | Equity valuation assumptions |
| Diluted shares | 17.951349m | Fact | Case share input |

## Why floor plan belongs in the model

Floor plan is dealer inventory financing: ABG borrows against vehicles held for sale. The model makes floor-plan debt rise or fall with inventory, calculates interest from the opening floor-plan balance, and includes the yearly change in floor plan in FCFE. It is not ordinary term debt and cannot simply be omitted. Removing it makes the cash forecast approximately negative $1.1 billion in the course demonstration because inventory would still consume cash but its financing source would disappear.

## Validation targets

The course’s check figures, rounded to one decimal, are:

| Check | FY2026E | FY2030E |
|---|---:|---:|
| Revenue | $18,323.0m | $19,678.3m |
| Operating income | $844.2m | $971.4m |
| Net income | about $413.6m | $527.5m |
| FCFE | about $211.4m | $342.3m |
| Cash | about $101.8m | $719.8m |
| Balance-sheet gap | $0.0m | $0.0m |

The valuation target is **$291.75 per share**, with about **80%** of value coming after 2030. The calculation discounts five years of FCFE and a terminal value based on `(2030 FCFE + 2030 debt repayment) x (1 + terminal growth)`.

## Required break test

To prove the balance check works, change the editable line near the top of `proforma.py` from:

```python
CASH_OVERRIDE = {}
```

to:

```python
CASH_OVERRIDE = {2026: 40.4}
```

Then run `python proforma.py`. The program must stop before valuation and name FY2026E with a balance-sheet gap of roughly negative $61.4m. Return the line to `{}` afterward.

## Sources

- [Part 1: Build the base case slides](https://cinderzhang.github.io/FIN43900-Fall2026/lessons/week-05/pro-forma-abg-tutorial/video-1-build-the-base-case-slides.html#0)
- [Lab 09 build instruction](https://cinderzhang.github.io/FIN43900-Fall2026/lessons/week-05/lab-09-proforma-build.html)

> Disclaimer: I have no licensure in any field of finance. This material is for educational purposes only and is not financial advice.
