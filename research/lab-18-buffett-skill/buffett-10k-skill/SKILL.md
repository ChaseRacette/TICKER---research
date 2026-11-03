---
name: buffett-10k
description: Analyze a U.S. public-company ticker from SEC EDGAR 10-K facts using Buffett-style owner-earnings and ROE checks. Use when the user asks for this educational 10-K business-quality analysis; do not use price data or invent missing values.
---

# Buffett 10-K analysis

Run `python scripts/edgar_buffett.py TICKER` with `SEC_USER_AGENT` set to a name and email.
The script, not the model, obtains SEC company facts and computes every displayed number.

Use only the script's output when writing the short memo. The memo must reach **own the
business**, **watch it**, or **pass**, judge the business rather than the stock price, and say
when missing inputs prevent a check. Save it as a Markdown file in `reports/`.

Required data rules:

- Use company facts from 10-K filings only and show the five most recent fiscal-year-end dates.
- For duplicate facts for one period, retain the value from the latest filed 10-K.
- Use the tag fallbacks embedded in the script. Never estimate a missing value.
- Interpret the script's `not found` and `not known` literally.
- Do not add price targets, market prices, or a valuation recommendation.

Before presenting a memo, run its number audit in the Streamlit app or with
`memo_unprinted_numbers()`. Correct or flag every number that is not among the script's printed
numbers.
