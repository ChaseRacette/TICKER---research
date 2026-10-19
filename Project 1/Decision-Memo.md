# Microsoft Corporation (MSFT) Decision Memo

**Recommendation: WATCH / DEFER**  
**Valuation reference date:** September 1-10, 2026  
**Currency and share basis:** USD per diluted share

## Committee view

Microsoft has material strengths in Azure/cloud growth, recurring commercial revenue, and contracted revenue. The present evidence does not yet support initiating a position because the central valuation question is whether AI-infrastructure capital spending can normalize while cloud growth, cloud margins, and cash conversion remain strong.

## Valuation evidence

| Method | Result | Key basis and limitation |
|---|---:|---|
| Five-year FCFF DCF | $541.74/share | September 10 calculation. Depends on FCFF-growth path, capex normalization, 8.0% WACC, 3.5% terminal growth, cash/debt treatment, and diluted shares. |
| Peer P/E | $435.11-$556.30/share | September 1 prices and annual GAAP diluted EPS. Median reference is $495.71/share. Oracle is used; Alphabet is qualified because its consolidated earnings are advertising-dominant. |

The defensible valuation reference range is **$435 to $556 per share**. The DCF result falls inside that range. I do not average the methods because they use different valuation objects and have different limitations.

## Top sensitivities

1. **AI/cloud capex intensity:** over the stated ranges, it creates a $64.37 per-share value span in the FCFE sensitivity model because capex directly affects cash reinvestment.
2. **Revenue growth:** it creates the larger final-year operating-profit span, $48,015.6m, because it changes revenue and gross profit.
3. **Discounting and terminal assumptions:** the FCFF DCF remains sensitive to its 8.0% WACC and 3.5% terminal-growth assumptions.

Sensitivity measures the model's response over the selected ranges. It does not assign probabilities to the lower, base, or higher cases.

## Failure conditions and monitoring

Do not initiate if any of the following emerge:

- AI-infrastructure capex stays elevated longer than the forecast path assumes.
- Cloud growth slows materially before utilization or scale benefits improve margins.
- Microsoft Cloud margins do not recover as infrastructure is deployed.
- A consistently normalized enterprise-cloud peer comparison fails to support value above the market price.

Monitor quarterly AI-infrastructure capex as a percentage of revenue, cloud growth, cloud-margin performance, and any normalized-EPS reconciliation for Microsoft and its admitted peers.

## Committee ask

**Do not initiate a position today.** Revisit the decision after the next reported results provide evidence on capex normalization, cloud-margin recovery, and cash-flow conversion. A more favorable view requires that evidence to support the valuation path rather than only a higher reported revenue figure.

## Sources and reproducibility

- Microsoft FY2026 Form 10-K, filed July 29, 2026.
- `models/dcf.py` and `research/reports/2026-09-10-msft-reverse-dcf.md`.
- `models/msft_pe_comps.py` and `research/reports/2026-09-17-msft-pe-triangulation-lab.md`.
- `research/lab-11-sensitivity/lab-11-submission.md`.

Educational coursework only. Not investment advice.
