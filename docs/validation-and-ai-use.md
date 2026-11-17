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

**Status: locked before rerun.** The student reported that the professor permitted AI assistance for this prediction. Therefore, this is honestly labeled an **AI-assisted prediction**, rather than described as AI-off. This prediction is committed and pushed before the 2.0% rerun.

| Required item | Locked prediction before run |
|---|---|
| Load-bearing input | Investment-grade bond (LQD) assumed annual return inside the changed-input stress test |
| Old value and units | 4.0% nominal annual return |
| New value and units | 2.0% nominal annual return |
| Expected direction of return / volatility / allocation | Expected portfolio return will decrease. Estimated volatility should not materially change because only an expected-return input changes. The allocation is expected to remain 5% Treasury reserve, 10% investment-grade bonds, 80% global equity, 0% private credit, and 5% listed infrastructure because bonds are already at their policy minimum and global equity has the stronger historical return input. |
| Expected effect on the PILOT decision | The decision should remain PILOT because the expected return should remain above the 7.5% nominal objective and all mandate guardrails should still pass. |
| Why this is the prediction | It tests whether the recommendation depends heavily on the 4.0% bond-return assumption while leaving the risk, liquidity, and allocation rules unchanged. |
| Pre-run evidence | This document's GitHub commit history is the locked, pre-rerun record. |

### After the committed rerun

| Required item | Actual result |
|---|---|
| Run date and data window | |
| Before result | |
| After result | |
| Did the decision change? | |
| Did the outcome match the prediction? Why or why not? | |

## AI use statement

ChatGPT/Codex helped implement and document the app, explain concepts, and assist with debugging. The student selected the mandate, constraints, pilot decision, and final interpretation. The professor permitted AI assistance for the recorded Lab 20 prediction; that assistance is disclosed above. Educational use only; not investment advice.
