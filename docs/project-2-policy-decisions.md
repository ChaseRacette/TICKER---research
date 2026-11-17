# Project 2 — Portfolio Policy Decisions

**Purpose:** This record captures the student's policy choices before building the Project 2 investment-management app. It is a design record, not a forecast or investment recommendation.

## Committee decision

The committee should **pilot**, rather than immediately adopt, the portfolio process. The pilot must demonstrate that the process can meet its stated objective and constraints before it guides real allocations.

## Investment philosophy

- Favor time in the market over market timing.
- Accept medium-high market risk in pursuit of long-term growth.
- Maintain general liquidity even while permitting a limited alternatives allocation.
- Use annual review and tolerance-band rebalancing instead of reacting to ordinary market movements.

## Mandate

| Policy item | Decision |
|---|---|
| Horizon | 15 years |
| Return objective | CPI + 5% annualized |
| Optimization objective | Highest expected return that remains within every stated risk and mandate rule |
| Estimated annual-volatility ceiling | 15% |
| Liquidity floor | At least 90% redeemable within five business days |
| Treasury/cash minimum | At least 5% of portfolio weight |
| Alternatives cap | At most 15% combined |
| Less-liquid alternatives cap | At most 10% combined |
| Drawdown trigger | 25% maximum drawdown triggers a committee review |
| Drawdown response | Pause new allocations and review assumptions, liquidity, and mandate compliance; do not automatically sell |
| Rebalancing | Review annually; rebalance only after an asset class drifts more than 5 percentage points from target |

## Investment universe and allocation ranges

| Sleeve | Allowed range | Liquidity role |
|---|---:|---|
| Global equity index | 60%–80% | Liquid growth core |
| Treasury bills/notes | 5%–15% | Liquid reserve |
| Investment-grade bonds | 10%–25% | Liquid diversification |
| Private credit | 0%–10% | Less-liquid alternative |
| Listed infrastructure ETF/fund | 0%–10% | Liquid alternative |
| Total alternatives | 0%–15% | Combined private-credit and infrastructure cap |

## Benchmark and baselines

The transparent benchmark is 70% global equity index, 20% investment-grade bonds, and 10% Treasury bills/notes. The app also shows an equal-weight baseline. Each baseline and the constrained portfolio receive a mandate verdict.

## Assumption and data approach

- The primary recommendation uses live Yahoo Finance monthly adjusted-close history for the five tickers. The app excludes the partial current month, retains the latest 60 completed monthly returns, then computes annualized arithmetic return, volatility, and correlation inputs locally at runtime. The date range displayed in the app identifies the exact live window used.
- The proxy mapping is SGOV for Treasury reserve, LQD for investment-grade bonds, ACWI for global equity, BIZD for the private-credit proxy, and IGF for listed infrastructure.
- BIZD is a public business-development-company ETF proxy, not a private-credit fund. The model nevertheless treats that sleeve conservatively as less liquid to keep the policy conservative; it does not reproduce private-credit fund terms, fees, or redemption mechanics.
- The changed-input stress test replaces the investment-grade bond expected-return input with a user-selected value; it does not replace other live observations after seeing a favorable output.
- The ACWI ten-month-trend data card is a monitoring signal. It can trigger committee review of assumptions; it does not automatically change weights.

## AI and ownership

ChatGPT/Codex helped translate the student's stated preferences into a testable policy record. The student owns the policy choices, financial analysis, and final committee decision. Educational use only; not investment advice.
