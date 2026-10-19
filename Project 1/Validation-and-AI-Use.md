# Project 1 Validation and AI Use

**Company:** Microsoft Corporation (MSFT)  
**Project period:** September-October 2026  
**Status:** Documentation and source/code checks completed. A local terminal capture remains required before final submission.

## Named AI disclosure

| Tool | Tasks performed | How the work was checked |
|---|---|---|
| Codex | Pulled and organized information from the Microsoft 10-Ks and helped solve the formulas used in the DCF, peer-P/E, pro-forma, and sensitivity analysis. It also helped organize the written reports and Project 1 documents. | I checked reported financial facts against Microsoft's FY2026 Form 10-K and primary links. I reviewed model inputs, formulas, dates, units, accounting checks, and output logic. I retained unresolved limitations rather than treating generated text as a source. |
| Google Antigravity | Used as a second study partner for coursework and model-question clarification. | I compared its explanations against the course instructions, the Microsoft filing, and the committed model/report evidence. I did not use an AI response as a financial-data source without checking it. |

AI tools supported drafting, organization, and explanation. The reported facts, source selection, calculation conventions, and final conditional conclusion remain subject to my review.

## Locked changed-input record

The locked record was saved at **2026-09-29T13:52:57-04:00** before scenario results and is recorded in Git commit `caa7f1e`.

| Independent input | Human-authored prediction before run | Lower/base/higher design |
|---|---|---|
| Consolidated revenue-growth path | Lower growth should reduce FY2031E operating profit, FCFE, and value; higher growth should increase all three. | Base path shifted down or up by 2 percentage points in every forecast year. |
| AI/cloud capex as % of revenue | Higher capex should leave FY2031E operating profit unchanged in the simplified model but reduce FCFE and value; lower capex should increase FCFE and value. | Base path shifted down or up by 5 percentage points in every forecast year. |

## Actual scenario output and diagnosis

| Driver and case | FY2031E operating profit | FY2031E FCFE | Value/share | Diagnosis |
|---|---:|---:|---:|---|
| Revenue growth - lower | $243,208.6m | $158,744.0m | $228.37 | Direction prediction supported. Value moved less than operating profit because higher revenue also requires incremental investment and later cash flows are discounted. |
| Revenue growth - base | $266,352.1m | $166,984.2m | $238.72 | Base reference. |
| Revenue growth - higher | $291,224.2m | $175,575.4m | $249.49 | Direction prediction supported. |
| Capex intensity - lower | $266,352.1m | $186,247.0m | $270.90 | Lower cash reinvestment increased FCFE and value. |
| Capex intensity - base | $266,352.1m | $166,984.2m | $238.72 | Base reference. |
| Capex intensity - higher | $266,352.1m | $147,721.4m | $206.53 | Prediction supported: capex reduced cash available to equity without changing operating profit in this simplified model. |

The runner records a restored-base match within $0.000001, zero balance-sheet gaps in each valid scenario, cash above the $25,000m floor, and no revolver draw. These scenario outputs are documented in the committed Lab 11 sensitivity records.

## Remaining execution evidence

The environment used to assemble the documents does not expose a Python interpreter. Before submission, I must run the repository's capture command in my local VS Code terminal, review the resulting `docs/executed-output.txt`, then commit it. That file will be the real execution evidence; this disclosure does not claim to replace it.

## Source and validation index

- Primary filing: `sources/filings/MSFT-FY2026-10-K.pdf`.
- Locked record: `research/lab-11-sensitivity/locked-changed-input-record.md`.
- Scenario runner: `research/lab-11-sensitivity/msft_sensitivity.py`.
- Sensitivity output: `research/lab-11-sensitivity/lab-11-submission.md`.
- Technical validation: `research/lab-11-sensitivity/validation-check.md`.
