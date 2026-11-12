"""Reproducible constrained portfolio engine for Project 2.

The fixed baseline uses the committed five-year monthly adjusted-close CSV. Historical
averages are inputs to test, not forecasts or investment advice.
"""
from __future__ import annotations

import csv
from io import StringIO
from math import sqrt
from statistics import fmean, stdev

SLEEVES = (
    "Treasury reserve",
    "Investment-grade bonds",
    "Global equity index",
    "Private credit proxy",
    "Listed infrastructure",
)
TICKERS = {
    "Treasury reserve": "SGOV",
    "Investment-grade bonds": "LQD",
    "Global equity index": "ACWI",
    "Private credit proxy": "BIZD",
    "Listed infrastructure": "IGF",
}
MIN_WEIGHTS = {
    "Treasury reserve": 0.05,
    "Investment-grade bonds": 0.10,
    "Global equity index": 0.60,
    "Private credit proxy": 0.00,
    "Listed infrastructure": 0.00,
}
MAX_WEIGHTS = {
    "Treasury reserve": 0.15,
    "Investment-grade bonds": 0.25,
    "Global equity index": 0.80,
    "Private credit proxy": 0.10,
    "Listed infrastructure": 0.10,
}
ALTERNATIVES = {"Private credit proxy", "Listed infrastructure"}
LIQUID_SLEEVES = set(SLEEVES) - {"Private credit proxy"}
ALTERNATIVES_CAP = 0.15
LIQUIDITY_FLOOR = 0.90
VOLATILITY_CEILING = 0.15
CPI_ASSUMPTION = 0.025
REAL_RETURN_OBJECTIVE = 0.05
NOMINAL_OBJECTIVE = CPI_ASSUMPTION + REAL_RETURN_OBJECTIVE
STEP = 0.05


def read_prices(csv_source):
    """Read monthly adjusted closes with the five required proxy tickers."""
    if hasattr(csv_source, "read"):
        text = csv_source.read()
        if isinstance(text, bytes):
            text = text.decode("utf-8-sig")
    else:
        with open(csv_source, encoding="utf-8-sig", newline="") as source:
            text = source.read()
    reader = csv.DictReader(StringIO(text))
    required = ["Date", *TICKERS.values()]
    if reader.fieldnames != required:
        raise ValueError("CSV columns must be Date, SGOV, LQD, ACWI, BIZD, and IGF in that order.")
    prices = {ticker: [] for ticker in TICKERS.values()}
    dates = []
    for row_number, row in enumerate(reader, start=2):
        dates.append(row["Date"])
        for ticker in prices:
            try:
                value = float(row[ticker])
            except (TypeError, ValueError) as error:
                raise ValueError(f"Row {row_number} has an invalid {ticker} price.") from error
            if value <= 0:
                raise ValueError(f"Row {row_number} has a non-positive {ticker} price.")
            prices[ticker].append(value)
    if len(dates) < 37:
        raise ValueError("The sensitivity CSV needs at least 37 monthly prices.")
    return dates, prices


def monthly_returns(prices):
    return {
        ticker: [current / previous - 1 for previous, current in zip(values, values[1:])]
        for ticker, values in prices.items()
    }


def correlation(left, right):
    left_mean, right_mean = fmean(left), fmean(right)
    numerator = sum((a - left_mean) * (b - right_mean) for a, b in zip(left, right))
    denominator = (len(left) - 1) * stdev(left) * stdev(right)
    if denominator == 0:
        raise ValueError("Correlation cannot be calculated for a zero-volatility return series.")
    return max(-1.0, min(1.0, numerator / denominator))


def estimate_inputs(csv_source, last_60_months=True):
    """Return annualized historical estimates and correlations mapped to policy sleeves."""
    _, prices = read_prices(csv_source)
    returns = monthly_returns(prices)
    if last_60_months:
        returns = {ticker: values[-60:] for ticker, values in returns.items()}
    estimates = {
        sleeve: {
            "expected_return": fmean(returns[ticker]) * 12,
            "volatility": stdev(returns[ticker]) * sqrt(12),
        }
        for sleeve, ticker in TICKERS.items()
    }
    correlations = {left: {} for left in SLEEVES}
    for left in SLEEVES:
        for right in SLEEVES:
            if left == right:
                correlations[left][right] = 1.0
            elif right in correlations and left in correlations[right]:
                correlations[left][right] = correlations[right][left]
            else:
                correlations[left][right] = correlation(
                    returns[TICKERS[left]], returns[TICKERS[right]]
                )
    return estimates, correlations


def expected_return(weights, estimates):
    return sum(weights[sleeve] * estimates[sleeve]["expected_return"] for sleeve in SLEEVES)


def volatility(weights, estimates, correlations):
    variance = sum(
        weights[left]
        * weights[right]
        * estimates[left]["volatility"]
        * estimates[right]["volatility"]
        * correlations[left][right]
        for left in SLEEVES
        for right in SLEEVES
    )
    return sqrt(max(variance, 0.0))


def constraint_results(weights, estimates, correlations):
    alternatives = sum(weights[sleeve] for sleeve in ALTERNATIVES)
    liquid = sum(weights[sleeve] for sleeve in LIQUID_SLEEVES)
    result = []
    for sleeve in SLEEVES:
        result.append((
            f"{sleeve} range {MIN_WEIGHTS[sleeve]:.0%}–{MAX_WEIGHTS[sleeve]:.0%}",
            weights[sleeve],
            MIN_WEIGHTS[sleeve] <= weights[sleeve] <= MAX_WEIGHTS[sleeve],
        ))
    result.extend([
        ("Total alternatives at most 15%", alternatives, alternatives <= ALTERNATIVES_CAP),
        ("Redeemable within five business days at least 90%", liquid, liquid >= LIQUIDITY_FLOOR),
        ("Estimated annual volatility at most 15%", volatility(weights, estimates, correlations), volatility(weights, estimates, correlations) <= VOLATILITY_CEILING),
    ])
    return result


def evaluate(weights, estimates, correlations):
    checks = constraint_results(weights, estimates, correlations)
    return {
        "weights": weights,
        "expected_return": expected_return(weights, estimates),
        "volatility": volatility(weights, estimates, correlations),
        "checks": checks,
        "verdict": "pass" if all(passed for _, _, passed in checks) else "fail",
    }


def weight_combinations(index=0, steps_left=20, partial=None):
    """Generate five-percent long-only portfolio weights that add to 100%."""
    partial = {} if partial is None else partial
    if index == len(SLEEVES) - 1:
        yield {**partial, SLEEVES[index]: steps_left * STEP}
        return
    for steps in range(steps_left + 1):
        yield from weight_combinations(index + 1, steps_left - steps, {**partial, SLEEVES[index]: steps * STEP})


def recommended_portfolio(estimates, correlations):
    """Maximize expected return among portfolios meeting policy limits and CPI + 5%."""
    best = None
    for weights in weight_combinations():
        evaluated = evaluate(weights, estimates, correlations)
        if evaluated["verdict"] != "pass" or evaluated["expected_return"] < NOMINAL_OBJECTIVE:
            continue
        if best is None or (evaluated["expected_return"], -evaluated["volatility"]) > (
            best["expected_return"], -best["volatility"]
        ):
            best = evaluated
    return best


def equal_weight_baseline(estimates, correlations):
    return evaluate({sleeve: 1 / len(SLEEVES) for sleeve in SLEEVES}, estimates, correlations)


def benchmark_baseline(estimates, correlations):
    return evaluate({
        "Treasury reserve": 0.10,
        "Investment-grade bonds": 0.20,
        "Global equity index": 0.70,
        "Private credit proxy": 0.00,
        "Listed infrastructure": 0.00,
    }, estimates, correlations)
