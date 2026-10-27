r"""Lab 16 — point-in-time data filter.

Run from the Course/Work Folder:
    .\.venv\Scripts\python.exe -E MSFT\ticker-research\research\lab-16-asof\asof.py
"""

from collections import defaultdict
from datetime import date, datetime


# Editable inputs
DECISION_DATE = "2026-03-31"
ROWS = [
    {"row": 1, "ticker": "AAA", "month": "2026-01", "published_on": "2026-02-10", "index": 101.0},
    {"row": 2, "ticker": "AAA", "month": "2026-02", "published_on": "2026-03-10", "index": 104.0},
    {"row": 3, "ticker": "AAA", "month": "2026-03", "published_on": "2026-04-10", "index": 109.0},
    {"row": 4, "ticker": "AAA", "month": "2026-02", "published_on": "2026-03-25", "index": 103.0},
    {"row": 5, "ticker": "BBB", "month": "2026-01", "published_on": "2026-02-10", "index": 98.0},
    {"row": 6, "ticker": "BBB", "month": "2026-02", "published_on": "2026-03-10", "index": 97.0},
    {"row": 7, "ticker": "BBB", "month": "2026-02", "published_on": "2026-03-10", "index": 97.0},
    {"row": 8, "ticker": "BBB", "month": "2026-03", "published_on": "2026-04-10", "index": 92.0},
    {"row": 9, "ticker": "CCC", "month": "2026-01", "published_on": "2026-02-10", "index": 110.0},
    {"row": 10, "ticker": "CCC", "month": "2026-02", "published_on": "2026-04-05", "index": 112.0},
    {"row": 11, "ticker": "", "month": "2026-02", "published_on": "2026-03-10", "index": 99.0},
    {"row": 12, "ticker": "CCC", "month": "2026-02", "published_on": "2026-03-10", "index": 111.0},
]


def parse_date(value):
    """Convert an ISO date string to a date object."""
    return date.fromisoformat(value)


def month_key(row):
    """Return a sortable date for a YYYY-MM measurement month."""
    return datetime.strptime(row["month"], "%Y-%m").date()


def print_funnel_step(rule_name, removed_rows):
    """Print the number and source row numbers removed by one rule."""
    row_numbers = [row["row"] for row in removed_rows]
    print(f"  {rule_name}: removed {len(removed_rows)} row(s): {row_numbers}")


def quarantine_missing_tickers(rows):
    """Remove rows without a ticker before any other processing."""
    removed = [row for row in rows if not row["ticker"]]
    kept = [row for row in rows if row["ticker"]]
    return kept, removed


def remove_exact_duplicates(rows):
    """Keep the first occurrence of an otherwise identical input row."""
    seen = set()
    kept = []
    removed = []
    for row in rows:
        signature = (row["ticker"], row["month"], row["published_on"], row["index"])
        if signature in seen:
            removed.append(row)
        else:
            seen.add(signature)
            kept.append(row)
    return kept, removed


def remove_post_decision_publications(rows, decision_date):
    """Remove rows that were not public on the decision date."""
    removed = [row for row in rows if parse_date(row["published_on"]) > decision_date]
    kept = [row for row in rows if parse_date(row["published_on"]) <= decision_date]
    return kept, removed


def keep_latest_publication(rows):
    """Keep the latest publication for each ticker and measurement month."""
    latest_by_ticker_month = {}
    for row in rows:
        key = (row["ticker"], row["month"])
        if (
            key not in latest_by_ticker_month
            or parse_date(row["published_on"])
            > parse_date(latest_by_ticker_month[key]["published_on"])
        ):
            latest_by_ticker_month[key] = row
    kept_row_numbers = {row["row"] for row in latest_by_ticker_month.values()}
    kept = [row for row in rows if row["row"] in kept_row_numbers]
    removed = [row for row in rows if row["row"] not in kept_row_numbers]
    return kept, removed


def asof_filter(rows, decision_date):
    """Apply the four point-in-time rules in their required order."""
    print("Row funnel")
    filtered, removed = quarantine_missing_tickers(rows)
    print_funnel_step("1. Quarantine no ticker", removed)

    filtered, removed = remove_exact_duplicates(filtered)
    print_funnel_step("2. Remove exact duplicate", removed)

    filtered, removed = remove_post_decision_publications(filtered, decision_date)
    print_funnel_step("3. Remove after decision date", removed)

    filtered, removed = keep_latest_publication(filtered)
    print_funnel_step("4. Keep latest known revision", removed)
    return filtered


def naive_filter(rows):
    """Make a hindsight panel: no decision-date filter, but still clean bad and duplicate rows."""
    filtered, _ = quarantine_missing_tickers(rows)
    filtered, _ = remove_exact_duplicates(filtered)
    filtered, _ = keep_latest_publication(filtered)
    return filtered


def print_panel(title, rows):
    """Print a date-sorted data panel."""
    print(f"\n{title}")
    print("  Row  Ticker  Month measured  Published on  Index")
    for row in sorted(rows, key=lambda item: (item["ticker"], month_key(item), item["row"])):
        print(
            f"  {row['row']:>3}  {row['ticker']:<6}  {row['month']:<14}  "
            f"{row['published_on']:<12}  {row['index']:.1f}"
        )


def signals(rows):
    """Return each ticker's percent change from its prior to latest available month."""
    rows_by_ticker = defaultdict(list)
    for row in rows:
        rows_by_ticker[row["ticker"]].append(row)

    results = {}
    for ticker, ticker_rows in rows_by_ticker.items():
        ordered = sorted(ticker_rows, key=month_key)
        if len(ordered) < 2:
            continue
        previous, latest = ordered[-2:]
        percent_change = (latest["index"] / previous["index"] - 1.0) * 100
        results[ticker] = {
            "latest_month": latest["month"],
            "percent_change": percent_change,
        }
    return results


def print_signals(title, rows):
    """Print one percent-change signal for every ticker with two observations."""
    print(f"\n{title}")
    for ticker, result in sorted(signals(rows).items()):
        print(
            f"  {ticker}: {result['percent_change']:+.2f}% "
            f"to {result['latest_month']}"
        )


def main():
    decision_date = parse_date(DECISION_DATE)
    print(f"Decision date: {decision_date.isoformat()}")
    asof_panel = asof_filter(ROWS, decision_date)
    print_panel("As-of panel", asof_panel)
    print_signals("As-of signals", asof_panel)

    naive_panel = naive_filter(ROWS)
    print_signals("Naive signals (ignores publication date)", naive_panel)


if __name__ == "__main__":
    main()
