# Lab 17 — FRED Point-in-Time Data Card

## DFF — Federal Funds Effective Rate

- **Source:** [Federal Reserve Economic Data (FRED), Federal Reserve Bank of St. Louis](https://fred.stlouisfed.org/series/DFF)
- **Series ID:** `DFF`
- **What it measures:** The effective federal funds rate, the overnight rate at which depository institutions lend federal-funds balances to one another.
- **Units:** Percent, not seasonally adjusted.
- **Frequency:** Daily, 7-day.
- **Release:** H.15 Selected Interest Rates.
- **Download date:** 2026-10-29.

## Point-in-time check

With 2026-09-30 as the as-of date, the newest DFF observation available was 2026-09-29 at 3.88%. The observed publication lag was one calendar day. The app showed 28 values in today's data after that observation date, so those observations were not knowable on 2026-09-30.

The app found 0 same-date revised values for this vintage. In this test, DFF was not revised.

## Three-value FRED check

| Observation date | DFF value (percent) |
|---|---:|
| 2026-09-29 | 3.88 |
| 2026-10-01 | 3.88 |
| 2026-10-27 | 3.88 |

These values match the current FRED DFF data downloaded by the app.

## Project 2 use

Project 2 may use DFF as an external rate input, not as a fund price. Any historical decision must use the ALFRED vintage available on the decision date, not today's FRED series.

## Partner attack — publication date

My partner trusted the publication-date field least. The app showed that on 2026-09-30 the latest DFF observation available was 2026-09-29 at 3.88%, while today's FRED data contains 28 later observations; this supports using the ALFRED vintage and an explicit lag rather than treating today's FRED series as contemporaneously knowable.

## My call

**Admit:** DFF may be used as an external Project 2 rate input because the app found a one-calendar-day publication lag and 0 same-date revisions for the 2026-09-30 vintage. I would quarantine it if a strategy requires same-day information or if a later vintage test finds revisions, until the rule specifies a safe publication lag and uses ALFRED vintages for every decision date.

## Learn and reflect

A data card records the source, series definition, units, frequency, publication timing, revisions, download date, and checked observations. Those fields prevent look-ahead bias because they distinguish the day a value measures from the day it became available and identify whether a later revision changed the earlier value; simply cleaning missing or duplicate rows does not establish either fact.

For DFF, the app showed a one-calendar-day lag: on 2026-09-30, the newest value available measured 2026-09-29. A backtest based on today's values would have included 28 observations that were not available then and could overstate how promptly a trading rule could react, even though this particular vintage had no same-date revisions.
