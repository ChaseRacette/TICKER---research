"""10-K-only Buffett-style metrics from the SEC EDGAR companyfacts endpoint.

Set SEC_USER_AGENT to "Name email@example.edu" before downloading.
"""
from __future__ import annotations

import json
import os
import re
import sys
from collections import defaultdict
from datetime import date
from pathlib import Path
from urllib.request import Request, urlopen


TICKERS_URL = "https://www.sec.gov/files/company_tickers.json"
FACTS_URL = "https://data.sec.gov/api/xbrl/companyfacts/CIK{cik:010d}.json"
MILLION = 1_000_000
FLOW_TAGS = {
    "revenue": ("RevenueFromContractWithCustomerExcludingAssessedTax", "Revenues"),
    "net_income": ("NetIncomeLoss",),
    "operating_cash_flow": ("NetCashProvidedByUsedInOperatingActivities",),
    "capital_spending": (
        "PaymentsToAcquirePropertyPlantAndEquipment",
        "PaymentsToAcquireProductiveAssets",
    ),
}
EQUITY_TAGS = ("StockholdersEquity",)


def sec_user_agent() -> str:
    """Return the required identifying SEC User-Agent without storing it in Git."""
    value = os.environ.get("SEC_USER_AGENT", "").strip()
    if not value or "@" not in value:
        raise RuntimeError(
            "Set SEC_USER_AGENT to your name and email, for example: "
            "Chase Racette cracette@purdue.edu"
        )
    return value


def download_json(url: str) -> dict:
    """Download one SEC JSON resource with the caller's required User-Agent."""
    request = Request(url, headers={"User-Agent": sec_user_agent()})
    with urlopen(request, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def cik_for_ticker(ticker: str) -> tuple[int, str]:
    """Look up a ticker in SEC's public ticker-to-CIK file."""
    wanted = ticker.upper().strip()
    for company in download_json(TICKERS_URL).values():
        if company["ticker"].upper() == wanted:
            return int(company["cik_str"]), company["title"]
    raise ValueError(f"Ticker {wanted!r} was not found in SEC's ticker list.")


def annual_fact_entries(facts: dict, tags: tuple[str, ...], flow: bool) -> tuple[dict[str, dict], str | None]:
    """Return latest-filed 10-K fact for each fiscal end, plus the tag actually found.

    Flows must span approximately one fiscal year; equity is an instant fact.  Mapping by end date
    then replacing only when `filed` is later implements the revision/latest-filing rule.
    """
    gaap = facts.get("facts", {}).get("us-gaap", {})
    for tag in tags:
        units = gaap.get(tag, {}).get("units", {}).get("USD", [])
        by_end: dict[str, dict] = {}
        for fact in units:
            if fact.get("form") != "10-K" or fact.get("fp") != "FY" or not fact.get("end"):
                continue
            if flow:
                if not fact.get("start"):
                    continue
                days = (date.fromisoformat(fact["end"]) - date.fromisoformat(fact["start"])).days
                if not 300 <= days <= 400:
                    continue
            previous = by_end.get(fact["end"])
            if previous is None or fact.get("filed", "") >= previous.get("filed", ""):
                by_end[fact["end"]] = fact
        if by_end:
            return by_end, tag
    return {}, None


def value_for_end(entries: dict[str, dict], end: str) -> float | None:
    fact = entries.get(end)
    return None if fact is None else float(fact["val"])


def build_year_rows(ticker: str) -> tuple[str, list[dict]]:
    """Turn SEC company facts into five annual rows and Buffett's three code checks."""
    cik, company = cik_for_ticker(ticker)
    facts = download_json(FACTS_URL.format(cik=cik))
    extracted: dict[str, tuple[dict[str, dict], str | None]] = {}
    for label, tags in FLOW_TAGS.items():
        extracted[label] = annual_fact_entries(facts, tags, flow=True)
    extracted["equity"] = annual_fact_entries(facts, EQUITY_TAGS, flow=False)

    # Revenue defines a fiscal year's row when available; otherwise use every discovered 10-K end.
    ends = set(extracted["revenue"][0])
    if not ends:
        ends = set().union(*(set(entries) for entries, _ in extracted.values()))
    selected_ends = sorted(ends)[-5:]
    rows: list[dict] = []
    for end in selected_ends:
        row = {"fiscal_year_end": end, "tags": {}}
        for field, (entries, tag) in extracted.items():
            row[field] = value_for_end(entries, end)
            row["tags"][field] = tag or "not found"
        equity = row["equity"]
        net_income = row["net_income"]
        row["roe"] = None if equity is None or equity <= 0 or net_income is None else net_income / equity
        ocf = row["operating_cash_flow"]
        capex = row["capital_spending"]
        row["owner_earnings"] = None if ocf is None or capex is None else ocf - capex
        rows.append(row)
    return company, rows


def buffett_checks(rows: list[dict]) -> dict[str, str]:
    """Compute the three lab checks; a missing input deliberately yields 'not known'."""
    roe_values = [row["roe"] for row in rows]
    owner = [row["owner_earnings"] for row in rows]
    return {
        "ROE of 15% or more every year": (
            "not known" if len(rows) != 5 or any(value is None for value in roe_values)
            else "pass" if all(value >= 0.15 for value in roe_values) else "fail"
        ),
        "Owner earnings positive every year": (
            "not known" if len(rows) != 5 or any(value is None for value in owner)
            else "pass" if all(value > 0 for value in owner) else "fail"
        ),
        "Owner earnings grew, first year to last": (
            "not known" if len(rows) != 5 or any(value is None for value in owner)
            else "pass" if owner[-1] > owner[0] else "fail"
        ),
    }


def format_millions(value: float | None) -> str:
    return "not found" if value is None else f"{value / MILLION:,.0f}"


def printable_numbers(rows: list[dict]) -> set[str]:
    """Return normalized tokens that may appear in a memo without being flagged."""
    numbers = {"15"}
    for row in rows:
        for field in ("revenue", "net_income", "operating_cash_flow", "capital_spending", "equity", "owner_earnings"):
            value = row.get(field)
            if value is not None:
                millions = value / MILLION
                numbers.update({str(int(round(millions))), f"{millions:,.0f}", f"{millions:.0f}"})
        if row.get("roe") is not None:
            percent = row["roe"] * 100
            numbers.update({f"{percent:.1f}", f"{percent:.0f}"})
    return numbers


def memo_unprinted_numbers(memo: str, rows: list[dict]) -> list[str]:
    """Flag number tokens in a memo that are not shown by the script's table."""
    allowed = printable_numbers(rows)
    matches = re.finditer(r"(?<![\w.])\$?\d+(?:,\d{3})*(?:\.\d+)?%?", memo)
    bad = []
    for match in matches:
        # "10-K" names a filing type, not a numerical memo claim.
        if memo[match.end():].startswith("-K"):
            continue
        token = match.group()
        normalized = token.lstrip("$").rstrip("%")
        if normalized not in allowed and normalized not in bad:
            bad.append(normalized)
    return bad


def print_report(ticker: str) -> tuple[str, list[dict], dict[str, str]]:
    company, rows = build_year_rows(ticker)
    checks = buffett_checks(rows)
    print(f"{ticker.upper()} — {company} (USD millions; 10-K facts only)")
    print("FY end | Revenue | Net income | Operating cash flow | Capital spending | Equity | ROE % | Owner earnings")
    for row in rows:
        roe = "not known" if row["roe"] is None else f"{row['roe'] * 100:.1f}"
        print(" | ".join([
            row["fiscal_year_end"], format_millions(row["revenue"]), format_millions(row["net_income"]),
            format_millions(row["operating_cash_flow"]), format_millions(row["capital_spending"]),
            format_millions(row["equity"]), roe, format_millions(row["owner_earnings"]),
        ]))
        print("  tags: " + "; ".join(f"{field}={tag}" for field, tag in row["tags"].items()))
    print("\nBuffett checks")
    for label, result in checks.items():
        print(f"- {label}: {result}")
    return company, rows, checks


def main() -> None:
    ticker = sys.argv[1] if len(sys.argv) > 1 else "COST"
    print_report(ticker)


if __name__ == "__main__":
    main()
