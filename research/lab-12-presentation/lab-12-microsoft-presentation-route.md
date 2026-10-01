# Lab 12 - Microsoft Presentation Route

**Question:** How did I get from choosing Microsoft to my valuation conclusion, which assumptions drive it, and what evidence could change my mind?

Use this as a speaking route, not a script to read. Show the linked files while presenting; the numbers below are prompts for explaining the work in your own words.

## 1. Target selection

I selected Microsoft because it combines recurring enterprise software and cloud economics with material AI/data-center investment. My initial view was watch/defer: cloud growth and contracted revenue supported research, but I needed to test whether infrastructure spending would convert into durable cash flow.

**Show:** [`2026-09-03-company-research.md`](../reports/2026-09-03-company-research.md), especially the initial thesis and MD&A evidence.

## 2. Company and evidence

Microsoft earns revenue from Productivity and Business Processes, Intelligent Cloud, and More Personal Computing. The FY2026 10-K reports $331.839B revenue, $155.237B operating income, 27% Microsoft Cloud growth to $214.4B, 41% Azure and other cloud-services growth, and $678B commercial remaining performance obligation.

The key counterweight is reinvestment: Microsoft Cloud gross margin declined to 66%, while the filing attributes cost pressure to AI infrastructure and product usage. Financial-statement values are in USD millions; fiscal year-end is June 30.

**Show:** [FY2026 Microsoft 10-K, Item 7 and Item 8](https://www.sec.gov/Archives/edgar/data/789019/000119312526323660/msft-20260630.htm) and [`2026-09-24-lab-10-msft-history-and-assumptions.md`](../reports/2026-09-24-lab-10-msft-history-and-assumptions.md).

## 3. Pro-forma

The FY2026 opening balance sheet starts with $758.376B total assets and $758.376B liabilities plus equity. The model forecasts revenue growth from 18% to 5%, gross margin from 67.5% to 69.0%, and AI/cloud capital spending from 34% to 20% of revenue. These are labeled judgments rather than management guidance.

The company-specific line is AI/cloud infrastructure capex and the depreciation it produces. Capex reduces cash and grows PP&E; depreciation affects earnings and is added back in FCFE. Cash is calculated last, and each FY2027E-FY2031E balance sheet has a $0.0m gap with cash above the $25B floor.

**Show:** [`msft_proforma.py`](../../msft_proforma.py) and the Lab 10 history/assumption report.

## 4. Valuation

Keep the valuation objects and dates separate:

| Method | Value / range | Date, currency, and share basis | Main limitation |
|---|---:|---|---|
| Week 3 FCFF DCF | $541.74/share | Sept. 10, 2026; USD/share; 7,427m shares | 8.0% WACC, 3.5% terminal growth, and strong FCFF recovery as capex normalizes |
| Peer P/E | $435.11-$556.30/share; $495.71 median | Sept. 1, 2026; USD/share; FY2026 MSFT GAAP diluted EPS $17.95 | Oracle and Alphabet have non-identical business mixes; EPS comparability is qualified |
| Lab 10 FCFE pro-forma | $238.72/share | FY2031 terminal calculation; USD/share; 7,425.545m shares | First-pass simplified FCFE model; capex and margin judgments dominate |
| Reverse DCF | Market price implied a -2.777 percentage-point shift to five FCFF growth rates | Sept. 10, 2026; $491.65 target price; FCFF model share basis | Assumptions-matching exercise, not proof of mispricing |

I do not average these values. The FCFF DCF assumes strong cash-flow recovery, the P/E comparison reflects peers' reported earnings, and the simplified FCFE pro-forma uses a different set of operating and reinvestment assumptions.

**Show:** [`2026-09-10-msft-reverse-dcf.md`](../reports/2026-09-10-msft-reverse-dcf.md), [`2026-09-17-msft-pe-triangulation-lab.md`](../reports/2026-09-17-msft-pe-triangulation-lab.md), and `msft_proforma.py`.

## 5. Sensitivity and drivers

At the Lab 11 base case, FY2031E operating profit is $266.352B, FCFE is $166.984B, and value is $238.72/share. The two tested drivers were revenue growth (two percentage-point annual shifts) and AI/cloud capex intensity (five-percentage-point annual shifts).

The causal capex path is: **capex as % of revenue -> capital spending and PP&E -> cash and depreciation -> FCFE -> value per share**. Over these ranges, revenue growth has the larger operating-profit span ($48.016B versus $0.0B), while capex has the larger FCFE span ($38.526B versus $16.831B) and value span ($64.37 versus $21.12/share).

This ranking is conditional on the tested ranges. It does not assign probability to any case and does not establish that capex is universally more important than growth.

**Show:** [`lab-11-submission.md`](../lab-11-sensitivity/lab-11-submission.md) and [`msft_sensitivity.py`](../lab-11-sensitivity/msft_sensitivity.py).

## 6. Interpretation

**Current conditional call:** Watch/defer. The FCFF DCF and peer range are sensitive to different assumptions, while the first-pass FCFE pro-forma is highly sensitive to capex intensity. I will not average conflicting methods to create a single answer.

**What could change my view:** sourced evidence that capex intensity can normalize without a corresponding loss of cloud growth or margin, plus a consistently normalized enterprise-cloud peer comparison. The next research priority is to reconcile the capex range to reported quarterly investment, cloud-margin, utilization, and lease-commitment evidence.

## Presentation close

The question that most changed my understanding is not whether Microsoft can grow revenue, but whether AI infrastructure converts into cash available to equity holders at the forecast rate. My sensitivity table shows impact over my chosen ranges; it does not tell me the probability of those endpoints.

> Disclaimer: I have no licensure in any field of finance. This material is for educational purposes only and is not financial advice.
