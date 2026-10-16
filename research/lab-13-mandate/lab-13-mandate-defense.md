# Lab 13 - Meridian Foundation Portfolio Mandate Defense

**Student:** Chase Racette  
**Case:** Meridian Foundation Reserve (fictional)  
**Reserve size:** $100 million  
**Run command:** `python research\lab-13-mandate\mandate.py`  
**Required probe command:** `python research\lab-13-mandate\mandate.py --probe`

## S1-S10 classification before building

| Statement | Type | Reason |
|---|---|---|
| S1. Seven-year horizon; annual rebalancing | Hard constraint | It gives an explicit investment horizon and an operational rebalancing schedule that the portfolio process must follow. |
| S2. CPI + 4% net of costs over rolling five years | Objective | It states the return outcome the reserve seeks over a stated measurement period. |
| S3. $0.75m quarterly payout; twelve months held in cash or daily-liquid government securities | Hard constraint | It specifies both a cash need and the eligible instruments that must cover it. |
| S4. 60% global equities / 40% U.S. investment-grade bonds benchmark | Preference | A benchmark is a comparison reference. The statement does not say a portfolio must match it or stay within an active-risk band. |
| S5. Long-only; no borrowing, short sales, or derivatives | Hard constraint | These are explicit prohibitions. The checker tests the long-only weight condition; the permitted holdings list contains no borrowing or derivatives. |
| S6. No single issuer above 8% | Hard constraint | It is a measurable issuer concentration limit, with stated exemptions for cash, Treasury, and diversified funds. |
| S7. Annual turnover at most 25% without committee approval | Hard constraint | It is an explicit limit, although it needs prior holdings/trades and approval data before it can be calculated. |
| S8. At least 90% redeemable within five business days | Hard constraint | It gives a measurable liquidity threshold and window. |
| S9. Calendar-year loss cannot exceed 10% | Unverifiable promise | No measurement convention, timing, treatment of payouts, or breach response is defined, so it must not be tested as a rule. |
| S10. No sector, ESG, tax, or home-bias preference; no pilot optimization target | Missing | The CIO has not selected what the pilot should optimize, so a computer has no authorized objective function. |

## Checker and validation

The checker computes every result from the editable holdings, candidate weights, and mandate inputs in `mandate.py`. It aggregates Acme Corp bonds and Acme Corp stock into one issuer exposure. It does not test S9; it prints `requires CIO clarification` exactly as instructed.

### Base-case output to validate

```text
Reserve minimum: 3.0% (quarters x distribution / reserve size)

Candidate A
  Weights sum to 100: 100.0% pass
  Long-only (lowest weight): 0.0% pass
  Reserve-eligible weight >= 3.0%: 14.0% pass
  Redeemable within 5 days >= 90.0%: 100.0% pass
  Largest single company <= 8.0%: 0.0% pass
  Calendar-year loss: requires CIO clarification
  Verdict: passes every checkable rule

Candidate B
  Weights sum to 100: 100.0% pass
  Long-only (lowest weight): 0.0% pass
  Reserve-eligible weight >= 3.0%: 1.0% FAIL
  Redeemable within 5 days >= 90.0%: 85.0% FAIL
  Largest single company <= 8.0%: 9.0% FAIL
  Calendar-year loss: requires CIO clarification
  Verdict: fails 3 rule(s)

Candidate C
  Weights sum to 100: 100.0% pass
  Long-only (lowest weight): 0.0% pass
  Reserve-eligible weight >= 3.0%: 2.0% FAIL
  Redeemable within 5 days >= 90.0%: 100.0% pass
  Largest single company <= 8.0%: 8.0% pass
  Calendar-year loss: requires CIO clarification
  Verdict: fails 1 rule(s)

Candidate D
  Weights sum to 100: 100.0% pass
  Long-only (lowest weight): 0.0% pass
  Reserve-eligible weight >= 3.0%: 3.0% pass
  Redeemable within 5 days >= 90.0%: 100.0% pass
  Largest single company <= 8.0%: 0.0% pass
  Calendar-year loss: requires CIO clarification
  Verdict: passes every checkable rule
```

### Required long-only probe

The saved base inputs remain unchanged. The `--probe` option makes a fresh copy of Candidate A, sets Cash to -2.0% and the global equity index fund to 64.0%, and reruns the same checker.

```text
Candidate A - long-only probe
  Weights sum to 100: 100.0% pass
  Long-only (lowest weight): -2.0% FAIL
  Reserve-eligible weight >= 3.0%: 10.0% pass
  Redeemable within 5 days >= 90.0%: 100.0% pass
  Largest single company <= 8.0%: 0.0% pass
  Calendar-year loss: requires CIO clarification
  Verdict: fails 1 rule(s)
```

This proves that the negative Cash weight fails long-only while the sum, reserve, liquidity, and issuer checks still pass.

## Quiz question I understood least

**Question:** Why does Candidate B fail the 8% issuer limit even though neither Acme Corp bonds nor Acme Corp stock is individually greater than 8%?  
**My answer:** The mandate counts all securities from one company together. Candidate B has 5.0% Acme bonds plus 4.0% Acme stock, so Acme Corp exposure is 9.0% and fails.

## Candidate D attack

Candidate D is 3% Cash, 89% Global equity index fund, and 8% Investment-grade bond fund. It passes every checkable rule: 3.0% reserve-eligible, 100.0% redeemable within five business days, and no non-exempt single-company exposure.

**Miles asked:** "Candidate D passes the reserve, liquidity, and issuer rules. Why could the CIO still reject it?"  
**I answered:** The objection holds because Candidate D is 92% equity-oriented and could reasonably expose the reserve to a calendar-year loss beyond 10%. S9 does not define the measure or breach response needed to reject it mechanically, so S9 is the statement that decides the objection.

**Miles asked:** "What statement would you cite against this portfolio if I had proposed it?"  
**I answered:** I would cite S9. Passing the mechanical reserve, liquidity, and issuer checks does not establish compliance with the undefined calendar-year-loss promise.

## One question for the CIO before optimization

**Question:** What exact optimization objective and measurable risk/breach rule should govern the pilot, including how the "no calendar-year loss greater than 10%" statement is measured and enforced?

**Answer that changes the portfolio:** If the CIO makes the 10% calendar-year-loss rule a binding ex-ante risk constraint, the portfolio would need a materially lower equity risk budget and more Treasury/cash exposure than Candidate D. If the CIO instead treats it as a non-binding aspiration and prioritizes CPI + 4% expected return, a higher equity allocation could be considered.

## Reflection and investment-policy-statement mapping

A portfolio can pass every checkable rule and still be unsuitable because a computer can only test definitions that the client actually made measurable. Candidate D passes reserve, liquidity, issuer, and long-only checks, but it may conflict with the client’s unresolved loss tolerance.

The type I was least sure of was S4. I classify the benchmark as a preference because it provides a performance reference, not a stated allocation or active-risk constraint. The CIO could change it into a hard constraint by specifying an allowed tracking-error, equity-weight, or duration range relative to the benchmark.

### Skeptical-colleague review: Miles

**Miles asked:** "Why does Candidate B fail the issuer limit when its Acme bonds and Acme stock are each below 8%?"  
**I answered:** The mandate combines all securities issued by the same company. Candidate B has 5.0% Acme bonds plus 4.0% Acme stock, so its Acme exposure is 9.0% and fails the 8.0% issuer limit.

**Miles asked:** "How do you know the probe fails only long-only rather than also failing the reserve or total-weight checks?"  
**I answered:** I changed Cash from 2.0% to -2.0% and Global equity index fund from 60.0% to 64.0%, which keeps the portfolio total at 100.0%. Reserve-eligible weight remains 10.0% from Cash, Treasury bills, and the Treasury note, so it still exceeds the 3.0% minimum; the negative Cash weight is the only failure.

> This is a fictional coursework case, not investment advice.
