r"""Download the Lab 15 monthly adjusted-close data from Yahoo Finance.

The date range contains 60 complete calendar months: October 2021 through
September 2026. Run from the Course/Work Folder:
    .\.venv\Scripts\python.exe -E MSFT\ticker-research\research\lab-15-portfolio-stability\download_prices.py
"""

import csv
from datetime import datetime, timezone
import json
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen


TICKERS = ("QQQ", "SGOV", "VGIT", "ACWI")
PERIOD_START = 1633046400  # 2021-10-01 UTC
PERIOD_END = 1790812800  # 2026-10-01 UTC, exclusive
OUTPUT_PATH = Path(__file__).with_name("prices.csv")


def fetch_adjusted_closes(ticker):
    """Return a date-to-adjusted-close mapping for one ticker from Yahoo Finance."""
    parameters = urlencode(
        {
            "period1": PERIOD_START,
            "period2": PERIOD_END,
            "interval": "1mo",
            "events": "history",
            "includeAdjustedClose": "true",
        }
    )
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?{parameters}"
    request = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urlopen(request) as response:
        payload = json.load(response)

    result = payload["chart"]["result"][0]
    adjusted_closes = result["indicators"]["adjclose"][0]["adjclose"]
    observations = {}
    for timestamp, adjusted_close in zip(result["timestamp"], adjusted_closes):
        if adjusted_close is None:
            raise ValueError(f"Yahoo Finance returned a missing adjusted close for {ticker}.")
        date = datetime.fromtimestamp(timestamp, timezone.utc).date().isoformat()
        observations[date] = adjusted_close
    return observations


def main():
    prices_by_ticker = {ticker: fetch_adjusted_closes(ticker) for ticker in TICKERS}
    dates = sorted(prices_by_ticker[TICKERS[0]])
    for ticker, observations in prices_by_ticker.items():
        if sorted(observations) != dates:
            raise ValueError(f"Yahoo Finance returned different monthly dates for {ticker}.")
    if len(dates) != 60:
        raise ValueError(f"Expected 60 complete monthly observations, received {len(dates)}.")

    with OUTPUT_PATH.open("w", newline="", encoding="utf-8") as output_file:
        writer = csv.writer(output_file)
        writer.writerow(["Date", *TICKERS])
        for date in dates:
            writer.writerow([date, *(prices_by_ticker[ticker][date] for ticker in TICKERS)])

    print(f"Created {OUTPUT_PATH} with {len(dates)} monthly adjusted-close rows.")
    print("Source: Yahoo Finance chart API, retrieved 2026-10-22.")


if __name__ == "__main__":
    main()
