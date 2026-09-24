# Lab 10 - Microsoft History Grid and Assumption Set

All amounts are USD millions. Microsoft fiscal years end June 30. I opened the SEC filings below and checked the FY2026 revenue ($331,839m) and FY2026 PP&E ($313,076m) against the filed 10-K's Consolidated Statements of Income and Consolidated Balance Sheets. The source key on every item identifies the filing and statement/section that supports it.

## Filing key

- **S24:** [Microsoft FY2024 Form 10-K, filed July 30, 2024](https://www.sec.gov/Archives/edgar/data/789019/000095017024087843/msft-20240630.htm), Item 8.
- **S25:** [Microsoft FY2025 Form 10-K, filed July 30, 2025](https://www.sec.gov/Archives/edgar/data/789019/000095017025100235/msft-20250630.htm), Item 8.
- **S26:** [Microsoft FY2026 Form 10-K, filed July 29, 2026](https://www.sec.gov/Archives/edgar/data/789019/000119312526323660/msft-20260630.htm), Item 8; Item 7 MD&A.

## Opening balance sheet and linked model

The new model is [`msft_proforma.py`](../../msft_proforma.py). Run it from the repository root with `python msft_proforma.py`. Its FY2026A opening balance sheet ties to zero before it forecasts any year.

| Opening FY2026A balance sheet item | USD millions | Source |
|---|---:|---|
| Cash and short-term investments | $76,843 | S26, Item 8, Consolidated Balance Sheets |
| Accounts receivable | $80,876 | S26, Item 8, Consolidated Balance Sheets |
| Inventory | $1,397 | S26, Item 8, Consolidated Balance Sheets |
| PP&E, net | $313,076 | S26, Item 8, Consolidated Balance Sheets |
| Other assets (aggregated) | $286,184 | S26, Item 8; total assets less separately modeled asset lines |
| **Total assets** | **$758,376** | S26, Item 8, Consolidated Balance Sheets |
| Debt | $40,294 | S26, Item 8, debt disclosures; simplified model line |
| Other liabilities (aggregated) | $275,695 | S26, Item 8; total liabilities less simplified debt line |
| Shareholders' equity | $442,387 | S26, Item 8, Consolidated Balance Sheets |
| **Total liabilities and equity** | **$758,376** | S26, Item 8, Consolidated Balance Sheets |

The first-pass model produces approximately **$238.72 per share**. It is a scenario calculation, not a price target: most sensitivity comes from the capex-normalization, gross-margin, and cost-of-equity judgments. The program refuses to print a value if a forecast balance sheet has a material gap or cash falls below its stated floor.

### Check block and market question

| Check | FY2027E | FY2028E | FY2029E | FY2030E | FY2031E |
|---|---:|---:|---:|---:|---:|
| Balance-sheet gap | $0.0m | $0.0m | $0.0m | $0.0m | $0.0m |
| Cash and short-term investments | $80,348.7m | $117,068.4m | $185,054.5m | $290,746.2m | $427,730.4m |
| Cash at or above $25,000m floor | Yes | Yes | Yes | Yes | Yes |
| Revolver draw | $0.0m | $0.0m | $0.0m | $0.0m | $0.0m |

No forecast year draws the revolver because cash remains above the stated $25.0B floor in every year.

On **September 24, 2026 at 1:37 PM EDT**, the available intraday MSFT quote was **$493.62 per share**. The model says **$238.72 per share** and the market says **$493.62 per share**, both using **7,425.545 million shares** - what capex, margin, growth, or discount-rate assumption would have to change for those two values to reconcile? [Price source](https://sogotrade2.websol.barchart.com/?1_selected=stockQuote&module=stockDetail&region=US&symbol=MSFT)

## Three-year history grid

| Fiscal year | Revenue | Gross profit | SG&A proxy* | Net income | Inventory | PP&E, net | Shareholders' equity |
|---|---:|---:|---:|---:|---:|---:|---:|
| FY2024 | $245,122 | $171,008 | $32,065 | $88,136 | $1,246 | $135,591 | $268,477 |
| FY2025 | $281,724 | $193,893 | $32,877 | $101,832 | $938 | $204,966 | $343,479 |
| FY2026 | $331,839 | $225,465 | $34,666 | $133,749 | $1,397 | $313,076 | $442,387 |

\*Microsoft does not report one consolidated line named “SG&A.” The proxy is **sales and marketing plus general and administrative**, excluding R&D. This is a presentation choice, not a reported Microsoft subtotal.

### Item-level filing record

| Year | Item | Value | Filing and locator |
|---|---|---:|---|
| FY2024 | Revenue | $245,122m | S24, Item 8, Consolidated Statements of Income |
| FY2024 | Gross profit | $171,008m | S24, Item 8, Consolidated Statements of Income |
| FY2024 | Sales and marketing | $24,456m | S24, Item 8, Consolidated Statements of Income |
| FY2024 | General and administrative | $7,609m | S24, Item 8, Consolidated Statements of Income |
| FY2024 | Net income | $88,136m | S24, Item 8, Consolidated Statements of Income |
| FY2024 | Inventory | $1,246m | S24, Item 8, Consolidated Balance Sheets |
| FY2024 | PP&E, net | $135,591m | S24, Item 8, Consolidated Balance Sheets |
| FY2024 | Shareholders' equity | $268,477m | S24, Item 8, Consolidated Balance Sheets |
| FY2025 | Revenue | $281,724m | S25, Item 8, Consolidated Statements of Income |
| FY2025 | Gross profit | $193,893m | S25, Item 8, Consolidated Statements of Income |
| FY2025 | Sales and marketing | $25,654m | S25, Item 8, Consolidated Statements of Income |
| FY2025 | General and administrative | $7,223m | S25, Item 8, Consolidated Statements of Income |
| FY2025 | Net income | $101,832m | S25, Item 8, Consolidated Statements of Income |
| FY2025 | Inventory | $938m | S25, Item 8, Consolidated Balance Sheets |
| FY2025 | PP&E, net | $204,966m | S25, Item 8, Consolidated Balance Sheets |
| FY2025 | Shareholders' equity | $343,479m | S25, Item 8, Consolidated Balance Sheets |
| FY2026 | Revenue | $331,839m | S26, Item 8, Consolidated Statements of Income |
| FY2026 | Gross profit | $225,465m | S26, Item 8, Consolidated Statements of Income |
| FY2026 | Sales and marketing | $26,710m | S26, Item 8, Consolidated Statements of Income |
| FY2026 | General and administrative | $7,956m | S26, Item 8, Consolidated Statements of Income |
| FY2026 | Net income | $133,749m | S26, Item 8, Consolidated Statements of Income |
| FY2026 | Inventory | $1,397m | S26, Item 8, Consolidated Balance Sheets |
| FY2026 | PP&E, net | $313,076m | S26, Item 8, Consolidated Balance Sheets |
| FY2026 | Shareholders' equity | $442,387m | S26, Item 8, Consolidated Balance Sheets |

## Three-year ratios and operating drivers

| Measure | FY2024 | FY2025 | FY2026 | Calculation / source |
|---|---:|---:|---:|---|
| Gross margin | 69.8% | 68.8% | 67.9% | Gross profit / revenue; history grid above |
| SG&A proxy / gross profit | 18.8% | 17.0% | 15.4% | (Sales & marketing + G&A) / gross profit; proxy is qualified above |
| Inventory days | 6.1 | 3.9 | 4.8 | Inventory / (revenue - gross profit) x 365; Item 8 income statement and balance sheet |
| Depreciation | $15,200m | $22,000m | $34,300m | Cash-flow statement, S24 / S25 / S26 Item 8 |
| Depreciation / closing PP&E | 11.2% | 10.7% | 11.0% | Depreciation / closing PP&E; closing-balance convention stated explicitly |
| Capital spending - filing | $44,477m | $64,551m | $115,948m | Cash-flow statement: payments to acquire property and equipment, S24 / S25 / S26 Item 8 |
| Capital spending - external data-provider field | Unresolved | Unresolved | Unresolved | No named external data provider or its definition was supplied. Do not silently substitute a non-comparable field; reconcile it after choosing a provider. |
| Effective tax rate | 18.2% | 17.6% | 19.4% | Income-tax expense / income before income taxes, S24 / S25 / S26 Item 8 |
| Reported revenue growth | 15.7% | 14.9% | 17.8% | Year-over-year reported revenue growth; S24 / S25 / S26 Item 7 MD&A |
| Organic / same-store growth | Not disclosed | Not disclosed | Not disclosed | Microsoft is not a store-based company and does not report a consolidated organic or same-store-sales metric in these 10-K MD&A sections. |
| Azure and other cloud-services growth | 29% | 34% | 41% | Item 7 MD&A in S24 / S25 / S26; this is a disclosed cloud KPI, not company-wide organic growth. |

## Assumption set

| Value | Label | Reason |
|---|---|---|
| Revenue growth: 18% FY2027E, then 14%, 11%, 8%, 5% | Judgment | FY2026 reported growth was 17.8% and Azure growth was 41%, but I taper consolidated growth because a company this large cannot reasonably sustain the FY2026 pace indefinitely. |
| Gross margin: 67.5%, rising to 69.0% by FY2031E | Judgment | The three-year margin fell from 69.8% to 67.9% while Microsoft invested in AI infrastructure. I assume partial efficiency recovery, not an immediate return to the FY2024 margin. |
| SG&A proxy / gross profit: 15.5% held near FY2026 | Judgment | The proxy fell to 15.4% in FY2026. Holding it near that level avoids assuming continuing leverage without evidence, while keeping R&D separately visible in a full model. |
| Inventory days: 5 days | History | FY2024-26 history ranges from 3.9 to 6.1 days; a 5-day forecast uses the midpoint rather than treating inventory as a major Microsoft cash driver. |
| Depreciation / closing PP&E: 11.0% | History | FY2024-26 values were 11.2%, 10.7%, and 11.0%. This is a simple starting relationship that must be checked against asset lives and capex timing. |
| Capital spending: explicit forecast, beginning above $115,948m and declining as a percent of revenue | Judgment | AI/cloud infrastructure is Microsoft's distinctive line. FY2026 capex was unusually large; I do not assume it disappears, but I also do not assume the FY2026 percentage repeats forever. |
| Effective tax rate: 19% | History | The three-year effective tax rate ranged from 17.6% to 19.4%; 19% is near the latest year and inside that history. |
| AI/cloud infrastructure capex and depreciation | Judgment | This replaces ABG's floor-plan row. Capex increases PP&E and reduces cash immediately; depreciation reduces earnings later but is added back in cash flow. Modeling only one side would break the economics. |
| Revolver / floor plan | None | Microsoft does not have dealer inventory financing. Do not force a floor-plan formula into this model. |

Microsoft has positive net income and historical operating cash flow in all three years. The "negative FCFE" limitation therefore does not apply to these historical years. If an explicit forecast year produces negative FCFE, label it **negative FCFE** and do not use a Gordon-growth terminal value on a negative terminal cash flow: a perpetuity of negative cash flow is not a meaningful enterprise-value number.

## Fresh-eyes review

### AI skeptical-review draft - replace or confirm with your partner's own words

**Attack:** Why should capital spending fall from 34% of revenue in FY2027E to 20% in FY2031E when FY2026 AI-infrastructure spending was still increasing and Microsoft has not guided to that percentage decline?

**Answer (two sentences):** I used a slow decline because FY2026 capex of $115.948B, or about 35% of revenue, is a very high starting point and the forecast does not assume it disappears; it remains $112.4B in FY2031E under this model. I would raise the capex ratios if Microsoft reports continued capex intensity, lease commitments, or cloud-margin pressure without evidence that utilization and efficiency are improving.

### Partner-model attack - requires your partner's assumption table

I cannot truthfully record an attack on a partner model I have not seen. Ask this evidence-focused question after opening it: **“Which judgment changes your cash balance most, and what filing history or guidance supports that number rather than the most recent year?”** Record your partner's answer and whether it changed your view.

> Disclaimer: I have no licensure in any field of finance. This material is for educational purposes only and is not financial advice.
