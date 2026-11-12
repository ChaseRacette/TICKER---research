# Project 2 Portfolio Pilot

## Run

From the repository root:

```powershell
.\.venv\Scripts\python.exe -E -m streamlit run research\project2\app.py
```

## What the app does

The app pilots a 15-year, growth-oriented portfolio process. It maximizes the historical expected return from its fixed baseline only after enforcing the student’s policy rules: sleeve ranges, a 15% alternatives cap, at least 90% liquidity, and at most 15% estimated annual volatility. It compares an equal-weight baseline, a 70/20/10 liquid benchmark, and the constrained recommendation.

The default inputs come from the committed five-year monthly adjusted-close file at `../lab-15-portfolio-stability/prices.csv`, covering October 2021 through September 2026. The user may upload a CSV with the same columns for a sensitivity run; that does not replace the fixed baseline recommendation.

## Proxy map and limitation

| Sleeve | Proxy |
|---|---|
| Treasury reserve | SGOV |
| Investment-grade bonds | LQD |
| Global equity index | ACWI |
| Private credit proxy | BIZD |
| Listed infrastructure | IGF |

BIZD is a publicly traded business-development-company ETF proxy. It does not reproduce the liquidity, valuation, fee, or redemption terms of a private-credit fund; the model treats the sleeve conservatively as less liquid.

AI use: ChatGPT/Codex assisted with code and documentation; the student owns the policy, analysis, and decision. Educational use only; not investment advice.
