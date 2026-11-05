"""SEC 10-K fact extraction and three-investor Lab 19 panel."""
from __future__ import annotations

import json, os, re
from datetime import date
from urllib.request import Request, urlopen

TICKERS_URL = "https://www.sec.gov/files/company_tickers.json"
FACTS_URL = "https://data.sec.gov/api/xbrl/companyfacts/CIK{cik:010d}.json"
MILLION = 1_000_000
TAGS = {
    "revenue": (("RevenueFromContractWithCustomerExcludingAssessedTax", "Revenues"), True),
    "net_income": (("NetIncomeLoss",), True),
    "operating_cash_flow": (("NetCashProvidedByUsedInOperatingActivities",), True),
    "capital_spending": (("PaymentsToAcquirePropertyPlantAndEquipment", "PaymentsToAcquireProductiveAssets"), True),
    "equity": (("StockholdersEquity",), False),
    "assets_current": (("AssetsCurrent",), False),
    "liabilities_current": (("LiabilitiesCurrent",), False),
    "liabilities": (("Liabilities",), False),
}

def sec_user_agent():
    value = os.environ.get("SEC_USER_AGENT", "").strip()
    if not value or "@" not in value:
        raise RuntimeError("Set SEC_USER_AGENT to your name and email, for example: Chase Racette cracette@purdue.edu")
    return value

def download(url):
    with urlopen(Request(url, headers={"User-Agent": sec_user_agent()}), timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))

def cik_for_ticker(ticker):
    for company in download(TICKERS_URL).values():
        if company["ticker"].upper() == ticker.upper().strip():
            return int(company["cik_str"]), company["title"]
    raise ValueError(f"Ticker {ticker!r} was not found in the SEC ticker list.")

def annual_entries(facts, tags, flow):
    gaap = facts.get("facts", {}).get("us-gaap", {})
    for tag in tags:
        selected = {}
        for fact in gaap.get(tag, {}).get("units", {}).get("USD", []):
            if fact.get("form") != "10-K" or fact.get("fp") != "FY" or not fact.get("end"):
                continue
            if flow:
                if not fact.get("start"): continue
                days = (date.fromisoformat(fact["end"]) - date.fromisoformat(fact["start"])).days
                if not 300 <= days <= 400: continue
            if fact.get("filed", "") >= selected.get(fact["end"], {}).get("filed", ""):
                selected[fact["end"]] = fact
        if selected: return selected, tag
    return {}, None

def build_year_rows(ticker):
    cik, company = cik_for_ticker(ticker)
    facts, extracted = download(FACTS_URL.format(cik=cik)), {}
    for field, (tags, flow) in TAGS.items(): extracted[field] = annual_entries(facts, tags, flow)
    ends = set(extracted["revenue"][0]) or set().union(*(set(values) for values, _ in extracted.values()))
    rows = []
    for end in sorted(ends)[-5:]:
        row = {"fiscal_year_end": end, "tags": {}}
        for field, (entries, tag) in extracted.items():
            fact = entries.get(end); row[field] = None if fact is None else float(fact["val"]); row["tags"][field] = tag or "not found"
        row["roe"] = None if row["equity"] is None or row["equity"] <= 0 or row["net_income"] is None else row["net_income"] / row["equity"]
        row["owner_earnings"] = None if row["operating_cash_flow"] is None or row["capital_spending"] is None else row["operating_cash_flow"] - row["capital_spending"]
        row["current_ratio"] = None if row["assets_current"] is None or row["liabilities_current"] in (None, 0) else row["assets_current"] / row["liabilities_current"]
        row["liabilities_to_equity"] = None if row["liabilities"] is None or row["equity"] in (None, 0) else row["liabilities"] / row["equity"]
        rows.append(row)
    return company, rows

def all_known(rows, fields): return len(rows) == 5 and all(row.get(field) is not None for row in rows for field in fields)
def result(known, condition): return "not known" if not known else "pass" if condition else "fail"

def investor_checks(rows):
    owner = [r["owner_earnings"] for r in rows]; income = [r["net_income"] for r in rows]
    latest_current = rows[-1].get("current_ratio") if rows else None
    latest_leverage = rows[-1].get("liabilities_to_equity") if rows else None
    return {
        "Buffett": {
            "ROE of 15% or more every year": result(all_known(rows, ("roe",)), all(r["roe"] >= .15 for r in rows) if all_known(rows, ("roe",)) else False),
            "Owner earnings positive every year": result(all_known(rows, ("owner_earnings",)), all(v > 0 for v in owner) if all_known(rows, ("owner_earnings",)) else False),
            "Owner earnings grew, first year to last": result(all_known(rows, ("owner_earnings",)), owner[-1] > owner[0] if all_known(rows, ("owner_earnings",)) else False),
        },
        "Cathie Wood": {
            "Revenue grew, first year to last": result(all_known(rows, ("revenue",)), rows[-1]["revenue"] > rows[0]["revenue"] if all_known(rows, ("revenue",)) else False),
            "Operating cash flow positive every year": result(all_known(rows, ("operating_cash_flow",)), all(r["operating_cash_flow"] > 0 for r in rows) if all_known(rows, ("operating_cash_flow",)) else False),
            "Disruptive innovation and adoption evidence": "not known",
        },
        "Burry": {
            "Operating cash flow at least net income every year": result(all_known(rows, ("operating_cash_flow", "net_income")), all(r["operating_cash_flow"] >= r["net_income"] for r in rows) if all_known(rows, ("operating_cash_flow", "net_income")) else False),
            "Liabilities no more than twice equity, latest year": result(latest_leverage is not None, latest_leverage <= 2 if latest_leverage is not None else False),
        },
    }

def verdict(checks):
    values = list(checks.values())
    if "fail" in values: return "watch it"
    return "own the business" if values and "not known" not in values else "watch it"

def display(value, ratio=False): return "not found" if value is None else (f"{value:.2f}" if ratio else f"{value / MILLION:,.0f}")
def printed_tokens(rows):
    allowed = {"15", "2"}
    for r in rows:
        for key in set(TAGS) | {"owner_earnings"}:
            if r.get(key) is not None: allowed.add(f"{r[key]/MILLION:,.0f}".replace(",", "")); allowed.add(f"{r[key]/MILLION:,.0f}")
        for key in ("roe", "current_ratio", "liabilities_to_equity"):
            if r.get(key) is not None: allowed.add(f"{r[key] * 100:.1f}" if key == "roe" else f"{r[key]:.2f}")
    return allowed
def memo_unprinted_numbers(memo, rows):
    allowed = printed_tokens(rows); bad = []
    for match in re.finditer(r"(?<![\w.])\$?\d+(?:,\d{3})*(?:\.\d+)?%?", memo):
        if memo[match.end():].startswith("-K"): continue
        token = match.group()
        norm = token.lstrip("$").rstrip("%").replace(",", "")
        if norm not in allowed and norm not in bad: bad.append(norm)
    return bad

def print_report(ticker):
    company, rows = build_year_rows(ticker); checks = investor_checks(rows)
    print(f"{ticker.upper()} — {company} (USD millions; 10-K facts only)")
    print("FY end | Net income | Operating cash flow | Equity | Current assets | Current liabilities | Liabilities | Current ratio | Liabilities/equity")
    for r in rows: print(" | ".join([r["fiscal_year_end"], *[display(r[x]) for x in ("net_income", "operating_cash_flow", "equity", "assets_current", "liabilities_current", "liabilities")], display(r["current_ratio"], True), display(r["liabilities_to_equity"], True)]))
    for investor, criteria in checks.items():
        print(f"\n{investor}: {verdict(criteria)}"); [print(f"- {name}: {value}") for name, value in criteria.items()]
    return company, rows, checks

if __name__ == "__main__":
    import sys; print_report(sys.argv[1] if len(sys.argv) > 1 else "COST")
