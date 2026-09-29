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
