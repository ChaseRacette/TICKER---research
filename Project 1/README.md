# Ticker Research

Fundamental Microsoft (MSFT) research and valuation coursework. This repository contains the source filing, reproducible standard-library Python models, written analysis, and Project 1 deliverables.

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
