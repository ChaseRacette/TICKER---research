# Lab 08 — MSFT Deal Evidence and Valuation Triangulation

**Target:** Microsoft Corporation (MSFT)  
**Week 3 valuation/comparison date:** September 1, 2026  
**Currency and share basis:** USD per share; annual GAAP diluted EPS.

## Reopen and explain: my method and focused question

A peer P/E becomes an implied MSFT share price by multiplying the peer's price-to-diluted-EPS multiple by Microsoft's diluted EPS. The comparison is informative only if the selected companies have sufficiently similar earnings economics and the earnings definitions are compatible.

Microsoft earns revenue from Productivity and Business Processes, Intelligent Cloud, and More Personal Computing. The core comparable economics for this exercise are recurring enterprise software, cloud infrastructure/platform services, support or subscription revenue, and the reinvestment needed to support those services. Microsoft reported positive FY2026 GAAP diluted EPS of $17.95.

**Focused question:** Are Oracle's cloud/software and support economics close enough to Microsoft to use directly, and does Alphabet's advertising-dominant mix require it to be only a qualified peer?

## Initial peer policy before candidate selection

I will consider an operating-company peer only when it has positive annual GAAP diluted EPS and meaningful enterprise software, cloud infrastructure, or recurring support/subscription economics. I will qualify or exclude a candidate if advertising, consumer hardware, on-premise licensing, hardware, geographic mix, or materially different capital intensity dominates its earnings.

I would reject a candidate if it lacks recurring enterprise/cloud economics, has non-comparable or negative annual GAAP EPS, or earns primarily from a business not central to Microsoft.

## Candidate evidence and decisions

| Candidate | Decision | Primary-source business evidence | Important difference | EPS evidence public by Sept. 1, 2026 |
| --- | --- | --- | --- | --- |
| Oracle (ORCL) | **Use** | [FY2026 10-K, Item 1 — Business Overview](https://www.sec.gov/Archives/edgar/data/1341439/000119312526277521/orcl-20260531.htm): cloud and software, hardware, and services; cloud includes applications and infrastructure, while software support is generally renewed annually. | Oracle has a larger legacy database/license and support exposure and separately reports hardware/services; its FY2026 free cash flow was negative amid cloud-infrastructure investment. | FY ended May 31, 2026; GAAP diluted EPS **$5.83**; [Oracle FY2026 annual release, June 10, 2026](https://www.oracle.com/news/announcement/q4fy26-earnings-release-2026-06-10/). |
| Alphabet Class A (GOOGL) | **Qualify and use** | [FY2025 10-K, Item 1 — Business](https://www.sec.gov/Archives/edgar/data/1652044/000165204426000018/goog-20251231.htm): Google Cloud grew 36% in 2025. | More than 70% of 2025 revenue came from online advertising, so its consolidated P/E reflects advertising economics more than Microsoft-like enterprise software/cloud economics. | FY ended Dec. 31, 2025; Class A GAAP diluted EPS **$10.81**; [10-K Note 12 — Net Income per Share](https://www.sec.gov/Archives/edgar/data/1652044/000165204426000018/goog-20251231.htm). |

## Inputs, dates, and sources

All prices are September 1, 2026 closes. EPS is the most recent annual reported GAAP diluted EPS public by that date. Reported and adjusted EPS are not mixed.

| Company | Role | Price | Annual GAAP diluted EPS | Fiscal year-end | Publication date | Price source | Earnings source/locator |
| --- | --- | ---: | ---: | --- | --- | --- | --- |
| Microsoft (MSFT) | Target | $501.02 | $17.95 | Jun. 30, 2026 | Jul. 29, 2026 | [Yahoo Finance historical prices](https://finance.yahoo.com/quote/MSFT/history/) | [FY2026 10-K, Item 8 — Statements of Income](https://www.sec.gov/Archives/edgar/data/789019/000119312526323660/msft-20260630.htm) |
| Oracle (ORCL) | Used peer | $141.32 | $5.83 | May 31, 2026 | Jun. 10, 2026 | [Yahoo Finance historical prices](https://uk.finance.yahoo.com/quote/ORCL/history/) | [FY2026 10-K, Item 8 — EPS](https://www.sec.gov/Archives/edgar/data/1341439/000119312526277521/orcl-20260531.htm) |
| Alphabet Class A (GOOGL) | Qualified peer | $335.02 | $10.81 | Dec. 31, 2025 | Feb. 4, 2026 earnings release; 10-K filed Feb. 2026 | [FT historical prices](https://markets.ft.markitdigital.com/data/equities/tearsheet/historical?s=GOOGL%3ANSQ) | [FY2025 10-K, Note 12 — Class A diluted EPS](https://www.sec.gov/Archives/edgar/data/1652044/000165204426000018/goog-20251231.htm) |

## P/E calculation and validation

Run from the repository root:

```powershell
python models\msft_pe_comps.py
```

| Check | Calculation/result |
| --- | ---: |
| Oracle P/E, checked by hand | $141.32 / $5.83 = **24.240137x** |
| Alphabet P/E | $335.02 / $10.81 = **30.991674x** |
| Peer median P/E | **27.615906x** |
| MSFT at minimum peer P/E | **$435.11** |
| MSFT at median peer P/E | **$495.71** |
| MSFT at maximum peer P/E | **$556.30** |
| Peer-implied range | **$435.11–$556.30** |

Before reading the leave-one-out result, I predicted that removing the higher-multiple Alphabet peer would reduce the reference estimate. It does: removing GOOGL leaves Oracle's multiple and a **$435.11** reference estimate, **$60.60 lower** than the two-peer median. With one valid peer, this is a reference estimate rather than a range.

## DCF and peer-P/E triangulation

| Method | Result and date | Main assumption or limitation |
| --- | --- | --- |
| Week 3 FCFF DCF | **$541.74 per share**; September 10, 2026 calculation using FY2026 financial inputs | FCFF-growth path, capex normalization, 8.0% WACC, 3.5% terminal growth, and treatment of cash/investments. |
| Peer P/E | **$435.11–$556.30**; September 1, 2026 prices and annual GAAP EPS | Two qualified operating peers with non-identical business mixes and different fiscal year-ends. Median reference: **$495.71**. |

I do not average these methods. The DCF is higher than the P/E median because it assumes a strong cash-flow recovery as capex normalizes. The P/E result instead reflects how the market priced Oracle's and Alphabet's reported annual earnings at the same date. The P/E range overlaps the DCF estimate, but that overlap is not validation because the earnings and business mixes are imperfectly comparable.

## Skeptical-colleague review and my judgment

**Criticism:** The weakest supported assumption is treating the two peer P/Es as equally informative. Alphabet's consolidated earnings are advertising-dominant, while Microsoft FY2026 GAAP EPS includes a gain from its OpenAI investment. The fiscal year-ends also differ, so the comparison is not a like-for-like operating-earnings multiple.

**Question that could change my decision:** If I normalize investment-related gains/losses consistently and use peers weighted more toward enterprise-cloud revenue, does MSFT still trade below the resulting comparable multiple?

**Judgment: accept.** The source evidence supports the business-mix and GAAP-EPS mismatch. I retain Alphabet as a qualified rather than direct peer and do not revise the calculated range; a normalized-EPS comparison is unresolved rather than an input I can invent.

## Conditional call

**Watch/defer.** The $495.71 peer-median reference is slightly below the $501.02 comparison-date price, while the DCF is $541.74 and rests heavily on capex normalization. **Initiate only if** updated quarterly evidence supports capex normalization and a consistently normalized enterprise-cloud peer comparison still supports a value above the market price; **otherwise, watch/defer.**

The evidence most likely to change my mind is quarterly cloud growth and AI-infrastructure capex intensity, together with a sourced normalized-EPS reconciliation for Microsoft and the admitted peers.

> Disclaimer: I have no licensure in any field of finance. This material is for educational purposes only and is not financial advice.
