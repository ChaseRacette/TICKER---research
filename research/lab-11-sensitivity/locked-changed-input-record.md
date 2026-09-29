# Locked Changed-Input Record - Microsoft Sensitivity

**Locked timestamp:** 2026-09-29T13:52:57-04:00  
**Model:** `msft_proforma.py`  
**Cash-flow convention:** FCFE (free cash flow to equity), USD millions  
**Outputs used in every run:** FY2031E operating income (USD millions), FY2031E FCFE (USD millions), and value per share (USD per diluted share).

## Driver 1: consolidated revenue-growth path

| Case | FY2027E | FY2028E | FY2029E | FY2030E | FY2031E | Unit / range reason |
|---|---:|---:|---:|---:|---:|---|
| Lower | 16% | 12% | 9% | 6% | 3% | 2 percentage points below every base-year assumption; tests slower conversion of cloud/AI demand into consolidated sales. |
| Base | 18% | 14% | 11% | 8% | 5% | Current model judgment. FY2024-26 reported growth was 15.7%, 14.9%, and 17.8%. |
| Higher | 20% | 16% | 13% | 10% | 7% | 2 percentage points above every base-year assumption; tests more persistent demand and scale benefits. |

**Prediction before run:** Changing only revenue growth from the base path to the lower path should decrease FY2031E operating income, FCFE, and value per share materially because lower sales reduce gross profit and the cash produced by the existing infrastructure. Changing it to the higher path should increase all three; I expect the value effect to be larger than the final-year operating-income percentage change because the terminal value also changes.

## Driver 2: AI/cloud capital spending as a percentage of revenue

| Case | FY2027E | FY2028E | FY2029E | FY2030E | FY2031E | Unit / range reason |
|---|---:|---:|---:|---:|---:|---|
| Lower | 29% | 25% | 22% | 18% | 15% | 5 percentage points below every base-year assumption; tests faster infrastructure-capex normalization. |
| Base | 34% | 30% | 27% | 23% | 20% | Current model judgment; it begins close to FY2026 filing capex of roughly 35% of revenue. |
| Higher | 39% | 35% | 32% | 28% | 25% | 5 percentage points above every base-year assumption; tests a longer period of AI/data-center investment intensity. |

**Prediction before run:** Changing only capex intensity from the base path to the higher path should leave FY2031E operating income unchanged in this simplified model but reduce FCFE and value per share, because more cash is reinvested in PP&E. The lower-capex case should increase FCFE and value, although it may be economically implausible if demand still requires additional capacity.

## Partner unit check

Before running, a partner should verify that the revenue cases are **percentage-point shifts**, not percentage changes, and that capex is stated as a **percentage of revenue**, not a dollar amount. Only one independent input changes in each scenario; every other model input remains at its base value.

## Actual results and prediction review

**Recorded:** 2026-09-29T14:06:50-04:00  
**Calculation convention:** FCFE, USD millions except USD per diluted share. The associated runner uses a fresh independent copy of the base input set for each case and reruns a fresh base case at the end.

### Revenue-growth path results

| Case | FY2031E operating profit | Change from base | FY2031E FCFE | Change from base | Value per share | Change from base |
|---|---:|---:|---:|---:|---:|---:|
| Lower | $243,208.6m | -$23,143.6m | $158,744.0m | -$8,240.2m | $228.37 | -$10.35 |
| Base | $266,352.1m | $0.0m | $166,984.2m | $0.0m | $238.72 | $0.00 |
| Higher | $291,224.2m | +$24,872.0m | $175,575.4m | +$8,591.2m | $249.49 | +$10.77 |
| Span | $48,015.6m |  | $16,831.4m |  | $21.12 |  |

**Prediction review:** The direction prediction was correct: lower growth reduced all three outputs and higher growth increased them. The size prediction was wrong: value per share moved by a smaller percentage than final-year operating profit because the model also requires incremental capex and working-capital investment as revenue grows, and discounting reduces the present value of later cash flows.

### AI/cloud capital-spending intensity results

| Case | FY2031E operating profit | Change from base | FY2031E FCFE | Change from base | Value per share | Change from base |
|---|---:|---:|---:|---:|---:|---:|
| Lower | $266,352.1m | $0.0m | $186,247.0m | +$19,262.8m | $270.90 | +$32.18 |
| Base | $266,352.1m | $0.0m | $166,984.2m | $0.0m | $238.72 | $0.00 |
| Higher | $266,352.1m | $0.0m | $147,721.4m | -$19,262.8m | $206.53 | -$32.18 |
| Span | $0.0m |  | $38,525.6m |  | $64.37 |  |

**Prediction review:** The direction and the operating-profit prediction were correct. In this simplified model, capex is a cash-investment input rather than a separate operating-income expense, so it changes FCFE and value while final-year operating profit remains unchanged.

### Validation result and research-priority statement

The first base run and restored base run have the same inputs and outputs within the runner's $0.000001 tolerance: FY2031E operating profit $266,352.1m, FY2031E FCFE $166,984.2m, and value per share $238.72. All six lower/base/higher runs have a $0.0m balance-sheet gap in each forecast year and cash above the $25,000m floor; no run draws a revolver.

This does not change the base-case valuation output, but it reinforces the research priority: verify whether AI/cloud capital spending can actually normalize toward the stated path without weakening cloud growth or margins. The capex range creates the wider value-per-share span, so that judgment remains the most important evidence question in this model.

## Partner exchange 2 - complete in class

I have not seen a partner's model, so this section must be completed during the exchange rather than invented here.

| Whose model | Changed result checked against base | Difference recomputed | Other independent inputs confirmed at base? | Statement trace question / correction |
|---|---|---|---|---|
| My Microsoft model - JP / September 9, 2026 | AI/cloud capex higher: $206.53/share vs. $238.72 base | -$32.18/share | Yes - revenue growth and other independent assumptions remained at base | JP: capex directly cuts FCFE without first being diluted by operating costs or taxes; the wider capex range can make it appear dominant. |
| Partner's model - JP / September 9, 2026 | Not completed: JP left class before reciprocal model review | Not completed | Not completed | No partner-model result available to trace or correct. |
