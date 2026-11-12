# Project 2 — Portfolio Policy Decisions

**Purpose:** This record captures the student’s policy choices before rebuilding the Project 2 investment-management app. It is a design record, not a forecast or an investment recommendation.

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

The transparent benchmark is 70% global equity index, 20% investment-grade bonds, and 10% Treasury bills/notes. The app will also show an equal-weight baseline. Each baseline and the constrained portfolio must receive a mandate verdict.

## Assumption and data approach

- The primary recommendation will use a fixed, documented baseline-assumption set so a reviewer can reproduce the result.
- A five-year historical-price window will be available as a sensitivity mode, not as a replacement selected after seeing a favorable output.
- The DFF point-in-time data card is a monitoring signal. It can trigger committee review of assumptions; it does not automatically change weights.

## AI and ownership

ChatGPT/Codex helped translate the student’s stated preferences into a testable policy record. The student owns the policy choices, financial analysis, and final committee decision. Educational use only; not investment advice.
