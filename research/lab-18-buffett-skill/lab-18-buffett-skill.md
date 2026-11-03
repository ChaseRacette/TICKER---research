# Lab 18 — Buffett 10-K Skill

## Question

Can an investor's philosophy become a skill that runs the same way every time—every number computed by code from the 10-K, with the judgment left to the model?

## Files

- [`buffett-10k-skill/SKILL.md`](buffett-10k-skill/SKILL.md) tells Codex when and how to run the reusable workflow.
- [`buffett-10k-skill/scripts/edgar_buffett.py`](buffett-10k-skill/scripts/edgar_buffett.py) downloads public SEC EDGAR company facts and computes the table and checks.
- [`app.py`](app.py) presents the five-year table, chart, checks, memo, and memo-number audit.

## Data rules implemented

Only 10-K facts are used. The latest filed fact for a fiscal-year end replaces an older one. Revenue, capital spending, and the other facts use the required XBRL tags and fallback order. Missing values stay `not found`; a check needing a missing value is `not known`.

## Run

Set `SEC_USER_AGENT` locally to your name and email; do not commit it. Then run:

```powershell
$env:SEC_USER_AGENT = "Your Name your.email@example.edu"
.\.venv\Scripts\python.exe -E research\lab-18-buffett-skill\buffett-10k-skill\scripts\edgar_buffett.py COST
.\.venv\Scripts\python.exe -E -m streamlit run research\lab-18-buffett-skill\app.py
```

## Decision

### COST verification

The live SEC run reproduced the course table for FY ends 2022-08-28 through 2026-08-30. Its three computed checks all passed: ROE was at least 15% in every year, owner earnings were positive in every year, and owner earnings grew from the first year to the last.

The JPM probe left capital spending and owner earnings as `not found`, and the two owner-earnings checks as `not known`. That is intentional: the program never estimates a missing value.

### Decision

I trust the COST verdict as a repeatable, 10-K-only business-quality reading because the code, not the model, computes the figures and checks. It is not a price or purchase recommendation; I would revisit the verdict if later 10-K results break the ROE or owner-earnings checks.
