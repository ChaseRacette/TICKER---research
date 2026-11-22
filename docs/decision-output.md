# Racette Investments Decision Output Snapshot

**Generated:** 2026-11-22 17:15 UTC  
**Live source:** Yahoo Finance monthly adjusted closes  
**Estimation window:** October 2021 through October 2026, using 60 completed monthly returns

| Portfolio | Mandate verdict | Historical expected return | Estimated volatility | Allocation |
|---|---|---:|---:|---|
| Equal weight | FAIL | 5.99% | 9.37% | Treasury reserve 20%; investment-grade bonds 20%; global equity index 20%; private-credit proxy 20%; listed infrastructure 20% |
| 70/20/10 benchmark | PASS | 7.80% | 11.97% | Treasury reserve 10%; investment-grade bonds 20%; global equity index 70%; private-credit proxy 0%; listed infrastructure 0% |
| Racette constrained recommendation | PASS | 9.25% | 13.18% | Treasury reserve 5%; investment-grade bonds 10%; global equity index 80%; private-credit proxy 0%; listed infrastructure 5% |

## Decision

**PILOT** the Racette Investments process. The recommendation is selected only after passing the sleeve ranges, 15% alternatives cap, 90% five-business-day liquidity floor, and 15% estimated-volatility ceiling.

The point-in-time ACWI ten-month monitor was **Growth trend intact** as of October 2026. It is monitoring-only and does not automatically change the allocation.

**Reversal condition:** pause new allocations if no feasible portfolio clears the CPI + 5% objective and every guardrail, or if a 25% drawdown triggers committee review.

This snapshot is a dated record of a live-data run. Run `research/project2/decision_snapshot.py` to produce a new current snapshot; results can differ when Yahoo Finance history updates.
