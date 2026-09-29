# Lab 11 Submission - Microsoft One-at-a-Time Sensitivity

**Company:** Microsoft (MSFT)  
**Model:** `msft_proforma.py` with a separate sensitivity runner  
**Cash-flow convention:** FCFE, USD millions except value per diluted share  
**Locked prediction:** [`locked-changed-input-record.md`](locked-changed-input-record.md), timestamped and committed before scenario results

## What one-at-a-time sensitivity means

One-at-a-time sensitivity changes one independent input while every other independent assumption returns to the same base value. The model then recalculates linked quantities such as revenue, gross profit, PP&E, depreciation, cash, FCFE, and value; it does not manually hold those calculated statement totals constant.

A ranking depends on the stated input ranges. A wider range can create a wider output span, so a driver is only “larger” **over these tested ranges**. A sensitivity table is not a forecast probability because it assigns no likelihood or probability weight to the lower, base, or higher cases.

## Input ranges

| Driver | Unit | Lower FY2027E-FY2031E | Base FY2027E-FY2031E | Higher FY2027E-FY2031E |
|---|---|---|---|---|
| Revenue growth | Annual growth rate; percentage of prior-year revenue | 16%, 12%, 9%, 6%, 3% | 18%, 14%, 11%, 8%, 5% | 20%, 16%, 13%, 10%, 7% |
| AI/cloud capex intensity | Capital spending as percentage of revenue | 29%, 25%, 22%, 18%, 15% | 34%, 30%, 27%, 23%, 20% | 39%, 35%, 32%, 28%, 25% |

## Visible sensitivity output

| Driver changed | Case | FY2031E operating profit | Change from base | FY2031E FCFE | Change from base | Value/share | Change from base | Accounting check |
|---|---|---:|---:|---:|---:|---:|---:|---|
| Revenue growth | Lower | $243,208.6m | -$23,143.6m | $158,744.0m | -$8,240.2m | $228.37 | -$10.35 | Pass |
| Revenue growth | Base | $266,352.1m | $0.0m | $166,984.2m | $0.0m | $238.72 | $0.00 | Pass |
| Revenue growth | Higher | $291,224.2m | +$24,872.0m | $175,575.4m | +$8,591.2m | $249.49 | +$10.77 | Pass |
| AI/cloud capex | Lower | $266,352.1m | $0.0m | $186,247.0m | +$19,262.8m | $270.90 | +$32.18 | Pass |
| AI/cloud capex | Base | $266,352.1m | $0.0m | $166,984.2m | $0.0m | $238.72 | $0.00 | Pass |
| AI/cloud capex | Higher | $266,352.1m | $0.0m | $147,721.4m | -$19,262.8m | $206.53 | -$32.18 | Pass |

All usable scenarios have a $0.0m balance-sheet gap in each forecast year, cash above the $25,000m floor, and no revolver draw. The runner labels an invalid accounting or cash-floor case and withholds value per share rather than ranking it.

## Output spans and main driver over these ranges

| Output | Revenue-growth span | AI/cloud-capex span | Larger driver over these ranges |
|---|---:|---:|---|
| FY2031E operating profit | $48,015.6m | $0.0m | Revenue growth |
| FY2031E FCFE | $16,831.4m | $38,525.6m | AI/cloud capex |
| Value per diluted share | $21.12 | $64.37 | AI/cloud capex |

Over these ranges, AI/cloud capex intensity is the main driver of FCFE and value because it directly changes cash reinvestment. It does not change final-year operating profit in this simplified model because capex is modeled as a cash investment rather than an additional operating-income expense.

The surprising result is that capex creates the wider value range while operating profit does not move. That result is a model-mechanics lesson: reported profit and cash available to equity can react differently to the same operating decision.

## Restored-base check

The final fresh base rerun matches the first base run within the runner's $0.000001 tolerance:

```text
FY2031E operating profit: $266,352.1m
FY2031E FCFE:             $166,984.2m
Value per diluted share:  $238.72
PASS: restored base matches the first base run.
```

## Reconciled locked prediction

The revenue-growth prediction got the direction right but overstated the relative value effect: higher revenue also requires incremental capex and working-capital investment, and later cash flows are discounted. The capex prediction was correct: changing capex intensity leaves operating profit unchanged in this simplified model but changes FCFE and value per share.

## Partner exchange 3 - complete during class

### Partner question to ask and answer during the exchange

**Question to ask:** Could the larger capex span reflect the chosen ranges instead of proving capex is universally more important?

**Answer:** Yes. The capex cases move five percentage points annually while revenue growth moves two percentage points, so the result identifies the larger driver only over these ranges and not a universal ranking.

**Actual partner listener summary / initials / date: JP / September 9, 2026**

> JP agreed that capex can look like the dominant driver because it cuts directly into free cash flow without first being diluted by operating costs or taxes. JP also noted that the wider tested capex range creates a larger-looking capex impact, so the ranking is conditional on the chosen ranges.

### Check I performed on my partner's analysis

JP left class before I was able to review his changed/base result, recompute the difference, verify that other independent assumptions stayed at base, or trace the result through his statements. No partner-model check is claimed.

**Partner name / model / status / date: JP / partner-model check not completed because partner left class / September 9, 2026**

> ____________________________________________________________________________

## Files and command

- Runner: [`msft_sensitivity.py`](msft_sensitivity.py)
- Validation record: [`validation-check.md`](validation-check.md)
- Full locked record: [`locked-changed-input-record.md`](locked-changed-input-record.md)

Run from the repository root:

```powershell
python research\lab-11-sensitivity\msft_sensitivity.py
```

> Disclaimer: I have no licensure in any field of finance. This material is for educational purposes only and is not financial advice.
