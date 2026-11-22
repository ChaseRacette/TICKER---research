# Lab 20 Changed-Input Stress Run

**Run date:** 2026-11-17  
**Live data window:** Yahoo Finance monthly adjusted closes, October 2021 through October 2026 (60 completed monthly returns)  
**Changed input:** investment-grade bond (LQD) assumed annual return, from **4.0%** to **2.0%**.

| Result | Before: 4.0% LQD assumption | After: 2.0% LQD assumption |
|---|---:|---:|
| Racette mandate verdict | Pass | Pass |
| Historical expected return | 9.69% | 9.49% |
| Estimated volatility | 13.18% | 13.18% |
| Treasury reserve | 5% | 5% |
| Investment-grade bonds | 10% | 10% |
| Global equity index | 80% | 80% |
| Private-credit proxy | 0% | 0% |
| Listed infrastructure | 5% | 5% |
| Committee decision | Pilot | Pilot |

## Interpretation

The expected return fell by 0.20 percentage points, as expected, while volatility and the allocation did not change. Investment-grade bonds remained at their 10% policy minimum, and the recommendation still met the 7.5% nominal objective and every mandate guardrail. The changed input therefore did not reverse the PILOT decision.

## Additional Project 2 stress runs

**Run date:** 2026-11-22  
**Live data window:** Yahoo Finance monthly adjusted closes, October 2021 through October 2026 (60 completed monthly returns)  
**Base recommendation:** 9.25% historical expected return, 13.18% estimated volatility; 5% Treasury reserve / 10% investment-grade bonds / 80% global equity / 0% private-credit proxy / 5% listed infrastructure.

| Challenge | Base case | Stress case | Actual result | Committee implication |
|---|---|---|---|---|
| Estimation window | 60 completed monthly returns | 36 completed monthly returns | Pass. Historical expected return increased to 18.44%; estimated volatility fell to 9.96%; allocation stayed 5% / 10% / 80% / 0% / 5%. | The PILOT decision remained. The much higher three-year historical average is not treated as a forecast. |
| Annual implementation cost | No cost deduction | 1.00% annual all-in cost | Pass. Net expected return was 8.25%, above the 7.5% nominal objective. Volatility and target weights are unchanged by a cost deduction. | The PILOT decision remained, but costs must continue to be monitored because a sufficiently high cost would eliminate the objective margin. |
| Tighter constraints | 15.0% volatility ceiling; 90% liquidity floor | 12.5% volatility ceiling; 95% liquidity floor | Pass. Historical expected return was 8.90%; estimated volatility was 12.45%; allocation shifted to 10% Treasury / 10% bonds / 75% global equity / 0% private credit / 5% infrastructure. | The PILOT decision remained, but the growth allocation fell when the guardrails tightened. |
| Historical drawdown | 25% pause-and-review trigger | Actual five-year monthly history | Maximum drawdown was -23.36% in September 2022; worst rolling 12-month return was -18.32% from November 2021 through October 2022. | The trigger was not hit, but the loss was close enough to support continued liquidity and drawdown monitoring. |

These are educational, historical tests, not forecasts. Any future scenario with no feasible allocation, a net expected return below the objective, or a drawdown at or beyond 25% requires a pause and committee review rather than an automatic trade.
