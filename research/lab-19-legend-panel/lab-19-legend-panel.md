# Lab 19 — Legend Panel

## Files

- `panel_skill.py` downloads 10-K-only facts and computes all three investors' checks.
- `app.py` shows the common facts, panel table, verdicts, side-by-side memos, and one audit across all memos.
- `graham-skill/SKILL.md` and `burry-skill/SKILL.md` document the two added expert skills.

## Run

```powershell
$env:SEC_USER_AGENT = "Your Name your.email@example.edu"
.\.venv\Scripts\python.exe -E research\lab-19-legend-panel\panel_skill.py COST
.\.venv\Scripts\python.exe -E -m streamlit run research\lab-19-legend-panel\app.py
```

## Panel decision

I would let the panel screen Project 2 companies only with a condition: it is a first-pass 10-K screen, and any pass must be followed by filing, business, and valuation research. A threshold probe changes a verdict without changing the company; screens are disciplined prompts, not complete decisions.
