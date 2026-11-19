# Racette Investments Portfolio Pilot

## Cold-run setup and one-command result

From the repository root:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Then this one command opens the committee-facing result:

```powershell
.\.venv\Scripts\python.exe -E -m streamlit run research\project2\app.py
```

The cold run requires Python 3.11 or newer and an internet connection. The app fetches public monthly adjusted-close data from Yahoo Finance; it does not require a CSV upload, API key, login, or local data file. A dated, readable output snapshot is available in [`docs/decision-output.md`](../../docs/decision-output.md).

## What the app does

Racette Investments pilots a 15-year, growth-oriented portfolio process. It pulls the latest completed monthly adjusted-close history from Yahoo Finance, calculates historical return, volatility, and correlation inputs locally, then maximizes historical expected return only after enforcing the policy rules: sleeve ranges, a 15% alternatives cap, at least 90% liquidity, and at most 15% estimated annual volatility.

The app compares an equal-weight baseline, a 70/20/10 liquid benchmark, and the constrained pilot allocation. It requests enough Yahoo Finance history to use the most recent 60 completed monthly returns and excludes the partial current month. The **Refresh live data** button clears the six-hour local cache. The app needs an internet connection to Yahoo Finance, but a reviewer never needs to upload a CSV.

The app also includes a monitoring-only, point-in-time ACWI ten-month trend signal and a changed-input stress test that replaces the investment-grade bond expected-return input. A failed stress test means the process pauses for review rather than automatically changing allocations.

## Ticker map and limitation

| Sleeve | Ticker |
|---|---|
| Treasury reserve | SGOV |
| Investment-grade bonds | LQD |
| Global equity index | ACWI |
| Private credit proxy | BIZD |
| Listed infrastructure | IGF |

BIZD is a publicly traded business-development-company ETF proxy. It does not reproduce the liquidity, valuation, fee, or redemption terms of a private-credit fund; the model treats that sleeve conservatively as less liquid.

AI use: ChatGPT/Codex assisted with code and documentation; the student owns the policy, analysis, and decision. Educational use only; not investment advice.

## Goal Runway Planner companion

The separate personal-planning companion accepts current savings, monthly expenses, monthly investment, a desired final portfolio value, and years to the goal. It projects a nominal future balance, shows the required monthly investment, and visualizes the annual path. Its default 7.5% annual assumption matches the Project 2 planning objective and is adjustable.

Run it from the repository root:

```powershell
.\.venv\Scripts\python.exe -E -m streamlit run research\project2\goal_runway.py
```

## Lab 20 readiness records

- [Decision memo](../../docs/decision-memo.md)
- [Decision output snapshot](../../docs/decision-output.md)
- [Validation and AI-use record](../../docs/validation-and-ai-use.md)
- [Changed-input stress-run output](../../docs/stress-run-output.md)
- [Partner cold-run note](../../docs/cold-run-note.md)

To regenerate a current readable decision snapshot from live Yahoo Finance data:

```powershell
.\.venv\Scripts\python.exe -E research\project2\decision_snapshot.py
```
