# Validation and AI Use — Northstar Portfolio Pilot

## Validation scope

The app compares two transparent baselines with the constrained recommendation on the same Yahoo Finance monthly adjusted-close data. It computes annualized arithmetic average returns, annualized volatility, and correlations locally after excluding the partial current month and retaining 60 completed monthly returns.

| Portfolio | Baseline / decision role | Latest dated mandate verdict |
|---|---|---|
| Equal weight | 20% in each sleeve | Fail |
| 70/20/10 benchmark | 70% global equity, 20% investment-grade bonds, 10% Treasuries | Pass |
| Northstar recommendation | Highest historical-return allocation that passes each policy rule | Pass |

The dated values and allocations are in [decision-output.md](decision-output.md). The app shows the individual policy checks for each portfolio rather than hiding a failing check.

## Data and model limitations

- Yahoo Finance is a live third-party source; a later run can produce different inputs and results.
- Historical arithmetic average return is an input for comparison, not a forecast.
- BIZD is a public BDC ETF proxy and does not reproduce private-credit fund terms, valuations, fees, or redemption restrictions.
- The ACWI ten-month trend is monitoring-only. It may lag reversals and does not predict returns.
- The allocation search uses long-only weights in 5% steps, so it does not represent every possible portfolio.

## Stress run and Locked Changed-Input Record

**Status: awaiting student completion before the Lab 20 rerun.** The student must complete the prediction below with AI closed, commit and push it *before* changing the input, then record the actual result. Do not replace this section with a retroactive prediction.

| Required item | Student entry before run |
|---|---|
| Load-bearing input | |
| Old value and units | |
| New value and units | |
| Expected direction of return / volatility / allocation | |
| Expected effect on the PILOT decision | |
| Why this is the student's prediction | |
| Commit hash before run | |

### After the committed rerun

| Required item | Actual result |
|---|---|
| Run date and data window | |
| Before result | |
| After result | |
| Did the decision change? | |
| Did the outcome match the prediction? Why or why not? | |

## AI use statement

ChatGPT/Codex helped implement and document the app, explain concepts, and assist with debugging. The student selected the mandate, constraints, pilot decision, and final interpretation. The Locked Changed-Input prediction must be authored by the student without AI assistance before the rerun. Educational use only; not investment advice.
