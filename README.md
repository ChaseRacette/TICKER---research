# Ticker Research

Fundamental Microsoft (MSFT) research and valuation coursework, plus the Racette Investments Project 2 portfolio pilot.

## Project 2 — Racette Investments Portfolio Pilot

**[Open the live Racette Investments app](https://racette-investments.streamlit.app/)**

From the repository root, install the app dependency and launch the investment-management application:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -E -m streamlit run "Project 2\app.py"
```

The app uses public Yahoo Finance monthly adjusted-close data and needs an internet connection. It compares two transparent baselines with a constrained Racette allocation, shows each mandate verdict, provides a point-in-time monitoring signal, and includes estimate, history-window, cost, constraint, and drawdown stress tests. Read the [Project 2 README](Project%202/README.md) for the cold-run setup and limitations, and the [Project 2 manifest](Project%202/manifest.md) for every submission artifact.

### Open the app by double-clicking

After completing the one-time setup above, double-click [Open-Racette-Investments.cmd](Open-Racette-Investments.cmd) in your local `ticker-research` folder. It starts the app and opens it in your browser. GitHub cannot run local programs from a README link, so the link is a shortcut to the launcher file rather than a browser-only launch button.

AI use: ChatGPT/Codex assisted with code and documentation. The student owns the policy, analysis, and decision. Educational use only; not investment advice.

## Setup

Use Python 3 from the repository root. No third-party packages are required.

```powershell
git clone https://github.com/ChaseRacette/TICKER---research.git
cd TICKER---research
python --version
```

If `python` is not recognized on Windows, install Python 3 and select **Add Python to PATH**, then reopen the terminal.

## Run the models

```powershell
# Five-year FCFF DCF, sensitivity grid, and reverse DCF
python models\dcf.py

# MSFT peer P/E comparison
python models\msft_pe_comps.py

# MSFT five-year pro-forma
python msft_proforma.py

# One-at-a-time revenue-growth and capex-intensity sensitivity
python research\lab-11-sensitivity\msft_sensitivity.py
```

To create real terminal evidence for Project 1 after confirming the results, run:

```powershell
powershell -ExecutionPolicy Bypass -File docs\capture-executed-output.ps1
```

## Repository layout

| Path | Contents |
| --- | --- |
| `models/` | DCF and comparable-company calculators. |
| `research/reports/` | Dated research, valuation, and pro-forma reports. |
| `research/lab-11-sensitivity/` | Sensitivity runner, locked record, and validation materials. |
| `sources/filings/` | Primary-source FY2026 Microsoft Form 10-K. |
| `docs/` | Execution-capture script and resulting terminal output. |
| `Project 1/` | Project submission manifest, research evolution, decision memo, and validation disclosure. |

## Important conventions

- Financial-statement amounts are USD millions unless a file says otherwise.
- Per-share values are USD per diluted share.
- Dates and source periods are stated in each report; do not mix values from different valuation dates without labeling the difference.
- The FCFF DCF and FCFE pro-forma use different cash-flow and discount-rate conventions. They are not averaged.

This repository supports coursework and independent learning; it is not investment advice.
