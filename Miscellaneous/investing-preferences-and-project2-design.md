# Investing Preferences and Project 2 Design Record

**Created:** 2026-11-19  
**Purpose:** This is a reconstructed summary of the conversation beginning when the student asked to be quizzed about investing preferences. It is not a word-for-word transcript. It records the student's stated preferences and the resulting Project 2 design decisions so another Codex chat can continue the work with context.

## Starting point

The student wanted to remake Project 2 around a portfolio process they would personally use, rather than continue the earlier portfolio design unchanged. The eventual goal is to build the personal version first, then adapt the same underlying logic into a Meridian portfolio prototype for committee use.

## Student investing preferences stated in the conversation

| Topic | Student's stated preference |
|---|---|
| Risk tolerance | Medium-high risk is acceptable because the student is young. |
| Investment style | Prefers time in the market over trying to time market dips and bumps. |
| Investment interests | Likes more aggressive ETFs in personal investing. |
| Liquidity | Wants the fund to remain generally liquid. |
| Alternatives | Is open to investments outside the public stock market, specifically private credit and infrastructure. |
| Drawdown tolerance | A temporary 25% decline is acceptable. |
| Time horizon | 15 years. |
| Return objective | CPI + 5% annualized. |
| Core portfolio preference | Slightly more global index exposure and less Treasury-bill exposure. |

## Mandate choices agreed for the portfolio process

| Policy item | Decision |
|---|---|
| Committee posture | Pilot the process before treating it as adopted. |
| Optimization goal | Seek the highest expected return while staying within every risk and mandate rule. |
| Annual volatility ceiling | 15%. |
| Treasury / cash minimum | 5% of the portfolio. |
| Alternatives allocation | Optional; capped at 15% combined. |
| Private-credit limit | 10% maximum because it is treated as the less-liquid alternative. |
| Listed-infrastructure limit | 10% maximum. |
| Liquidity floor | At least 90% redeemable within five business days. |
| Drawdown response | At a 25% drawdown, pause new allocations and review assumptions, liquidity, and mandate compliance; do not automatically sell. |
| Rebalancing | Review annually; rebalance only after a sleeve drifts more than five percentage points from target. |
| Benchmark | 70% global equity, 20% investment-grade bonds, 10% Treasuries. |
| Historical input window | Use five years of historical data. |

## Investment universe selected

| Portfolio sleeve | Ticker used in the app | Role |
|---|---|---|
| Treasury reserve | SGOV | Liquid reserve and policy minimum. |
| Investment-grade bonds | LQD | Liquid diversification. |
| Global equity index | ACWI | Growth core. |
| Private-credit proxy | BIZD | Limited, less-liquid alternatives proxy. |
| Listed infrastructure | IGF | Liquid alternatives exposure. |

## How these preferences shaped the app

The Project 2 app is called **Northstar Portfolio Pilot**. It:

1. Uses live Yahoo Finance monthly adjusted-close data for the five tickers above.
2. Compares equal weight, the 70/20/10 benchmark, and a constrained recommendation.
3. Searches long-only allocations in 5% steps and chooses the highest historical expected-return allocation that passes every guardrail.
4. Shows the mandate result for each portfolio rather than hiding failed checks.
5. Uses an ACWI ten-month trend as a monitoring-only point-in-time signal; it does not automatically trade.
6. Includes a changed-input stress test for the assumed return of investment-grade bonds.
7. Recommends a **PILOT**, not immediate adoption, with defined pause-and-review triggers.

## Personal-first, Meridian-second direction

The student later requested a two-layer build:

- **Personal version first:** connect savings, expenses, monthly contributions, final-value goals, time horizon, and portfolio planning in a tool the student would actually use.
- **Meridian prototype second:** adapt the same transparent policy engine into a committee-facing view with generalized client inputs, mandate checks, stress testing, and an audit trail.

The personal goal companion currently lives at `research/project2/goal_runway.py`. It should remain educational planning software and should not be represented as Meridian's actual production system or use real Meridian client data without explicit authorization.

## Related repository files

- `docs/project-2-policy-decisions.md` — authoritative policy record.
- `research/project2/app.py` — Northstar committee-facing Streamlit app.
- `research/project2/portfolio_engine.py` — allocation rules and decision logic.
- `research/project2/goal_runway.py` — personal savings and goal-planning companion.
- `docs/decision-memo.md` — current Pilot recommendation and conditions.

## AI-use note

ChatGPT/Codex helped organize the student's preferences into testable policy rules and implement the educational prototype. The student owns the stated preferences, mandate choices, analysis, and ultimate decision. This is educational material, not investment advice.
