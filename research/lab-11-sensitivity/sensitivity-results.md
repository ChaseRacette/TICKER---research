# Microsoft Lab 11 Sensitivity Results

**Run convention:** FCFE, USD millions except value per diluted share.  
**Locked prediction record:** [`locked-changed-input-record.md`](locked-changed-input-record.md), committed before scenarios as Git commit `caa7f1e`.  
**Scenario runner:** [`msft_sensitivity.py`](msft_sensitivity.py). Run from the repository root with `python research\\lab-11-sensitivity\\msft_sensitivity.py`.

Each scenario changes only one independent input. The final-year outputs below are comparable because share count, gross-margin path, tax rate, working-capital assumptions, debt, repurchases, discount rate, and terminal growth stay at their base values unless the named driver changes.

| Driver changed | Case | FY2031E operating income | FY2031E FCFE | Value per diluted share |
|---|---|---:|---:|---:|
| Revenue-growth path | Lower: 16%, 12%, 9%, 6%, 3% | $243,208.6m | $158,744.0m | $228.37 |
| Revenue-growth path | Base: 18%, 14%, 11%, 8%, 5% | $266,352.1m | $166,984.2m | $238.72 |
| Revenue-growth path | Higher: 20%, 16%, 13%, 10%, 7% | $291,224.2m | $175,575.4m | $249.49 |
| Capex / revenue path | Lower: 29%, 25%, 22%, 18%, 15% | $266,352.1m | $186,247.0m | $270.90 |
| Capex / revenue path | Base: 34%, 30%, 27%, 23%, 20% | $266,352.1m | $166,984.2m | $238.72 |
| Capex / revenue path | Higher: 39%, 35%, 32%, 28%, 25% | $266,352.1m | $147,721.4m | $206.53 |

## Check result

All six runs balance in FY2027E through FY2031E with a $0.0m balance-sheet gap in every year, and cash remains above the $25,000m floor. No scenario draws a revolver because each path retains positive cash above that floor.

## Partner check still required

Before class submission, have your partner verify the percentage-point and percentage-of-revenue units in the locked record and confirm that each scenario changes only one driver. Record their name or initials and any correction here rather than claiming a check that did not occur.

> Disclaimer: I have no licensure in any field of finance. This material is for educational purposes only and is not financial advice.
