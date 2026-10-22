r"""Lab 14 — Meridian portfolio baseline risk engine.

Run from the Course/Work Folder:
    .\.venv\Scripts\python.exe -E MSFT\ticker-research\research\lab-14-portfolio\portfolio.py
"""

import csv
from io import StringIO
from math import sqrt
from statistics import fmean, stdev


# Editable inputs: expected returns and volatilities are annual decimals.
SLEEVES = {
    "Treasury bills": {"expected_return": 0.035, "volatility": 0.005},
    "Treasury 10-year note": {"expected_return": 0.043, "volatility": 0.070},
    "Investment-grade bond fund": {"expected_return": 0.050, "volatility": 0.060},
    "Global equity index fund": {"expected_return": 0.080, "volatility": 0.160},
}

CORRELATIONS = {
    "Treasury bills": {
        "Treasury bills": 1.00,
        "Treasury 10-year note": 0.10,
        "Investment-grade bond fund": 0.05,
        "Global equity index fund": 0.00,
    },
    "Treasury 10-year note": {
        "Treasury bills": 0.10,
        "Treasury 10-year note": 1.00,
        "Investment-grade bond fund": 0.80,
        "Global equity index fund": -0.10,
    },
    "Investment-grade bond fund": {
        "Treasury bills": 0.05,
        "Treasury 10-year note": 0.80,
        "Investment-grade bond fund": 1.00,
        "Global equity index fund": 0.25,
    },
    "Global equity index fund": {
        "Treasury bills": 0.00,
        "Treasury 10-year note": -0.10,
        "Investment-grade bond fund": 0.25,
        "Global equity index fund": 1.00,
    },
}

OBJECTIVE_RETURN = 0.065  # CPI estimate of 2.5% + 4.0%
RESERVE_ELIGIBLE = {"Treasury bills", "Treasury 10-year note"}


def validate_correlation_table(sleeves, correlations):
    """Raise ValueError when a correlation table is incomplete, asymmetric, or invalid."""
    names = list(sleeves)
    for left in names:
        if left not in correlations:
            raise ValueError(f"Correlation table is missing the row for {left}.")
        for right in names:
            if right not in correlations[left]:
                raise ValueError(f"Correlation table is missing {left} / {right}.")
            correlation = correlations[left][right]
            if not -1.0 <= correlation <= 1.0:
                raise ValueError(
                    f"Correlation for {left} / {right} is {correlation}; it must be between -1 and 1."
                )
            if correlations.get(right, {}).get(left) != correlation:
                raise ValueError(f"Correlation table is not symmetric at {left} / {right}.")


def covariance_matrix(sleeves, correlations):
    """Return covariances calculated as correlation × volatility × volatility."""
    return {
        left: {
            right: correlations[left][right]
            * sleeves[left]["volatility"]
            * sleeves[right]["volatility"]
            for right in sleeves
        }
        for left in sleeves
    }


def benchmark_weights(sleeves):
    """Return Lab 13 candidate S4: 40% IG bonds and 60% global equity."""
    return {
        sleeve: 0.40 if sleeve == "Investment-grade bond fund"
        else 0.60 if sleeve == "Global equity index fund"
        else 0.0
        for sleeve in sleeves
    }


def equal_weight_weights(sleeves):
    """Give every sleeve the same portfolio weight."""
    return {sleeve: 1.0 / len(sleeves) for sleeve in sleeves}


def inverse_volatility_weights(sleeves):
    """Scale weights proportional to 1 / volatility so they sum to 100%."""
    inverse_volatilities = {
        sleeve: 1.0 / details["volatility"] for sleeve, details in sleeves.items()
    }
    total_inverse_volatility = sum(inverse_volatilities.values())
    return {
        sleeve: inverse_volatilities[sleeve] / total_inverse_volatility
        for sleeve in sleeves
    }


def expected_return(weights, sleeves):
    """Calculate the weighted expected return."""
    return sum(weights[sleeve] * sleeves[sleeve]["expected_return"] for sleeve in sleeves)


def portfolio_variance(weights, covariances):
    """Calculate w'Σw by including every pair of sleeve weights and covariance."""
    return sum(
        weights[left] * weights[right] * covariances[left][right]
        for left in weights
        for right in weights
    )


def portfolio_volatility(weights, covariances):
    """Calculate portfolio volatility as the square root of portfolio variance."""
    return sqrt(portfolio_variance(weights, covariances))


def reserve_eligible_weight(weights, reserve_eligible):
    """Add the weights of bills and the 10-year note."""
    return sum(weights.get(sleeve, 0.0) for sleeve in reserve_eligible)


def weight_combinations(asset_names, step_percentage=5):
    """Yield long-only weight dictionaries that add to 100% in fixed-size steps."""
    if not asset_names:
        raise ValueError("At least one asset is required for a portfolio search.")
    if step_percentage <= 0 or 100 % step_percentage != 0:
        raise ValueError("The search step must be a positive factor of 100.")

    total_steps = 100 // step_percentage

    def build_weights(index, steps_left, partial_weights):
        if index == len(asset_names) - 1:
            yield {
                **partial_weights,
                asset_names[index]: steps_left * step_percentage / 100,
            }
            return
        for steps in range(steps_left + 1):
            yield from build_weights(
                index + 1,
                steps_left - steps,
                {
                    **partial_weights,
                    asset_names[index]: steps * step_percentage / 100,
                },
            )

    yield from build_weights(0, total_steps, {})


def lowest_risk_mix(
    sleeves,
    correlations,
    objective_return,
    reserve_eligible,
    minimum_reserve_weight,
    step_percentage=5,
):
    """Return the lowest-volatility feasible mix, or None when no mix qualifies."""
    validate_correlation_table(sleeves, correlations)
    covariances = covariance_matrix(sleeves, correlations)
    best_result = None

    for weights in weight_combinations(list(sleeves), step_percentage):
        calculated_return = expected_return(weights, sleeves)
        reserve_weight = reserve_eligible_weight(weights, reserve_eligible)
        if (
            calculated_return < objective_return
            or reserve_weight < minimum_reserve_weight
        ):
            continue

        calculated_volatility = portfolio_volatility(weights, covariances)
        if (
            best_result is None
            or calculated_volatility < best_result["volatility"]
        ):
            best_result = {
                "weights": weights,
                "expected_return": calculated_return,
                "volatility": calculated_volatility,
                "reserve_eligible_weight": reserve_weight,
            }

    return best_result


def read_monthly_prices(csv_source):
    """Read a date-first CSV path or text file object into dates and price series."""
    if hasattr(csv_source, "read"):
        csv_text = csv_source.read()
        if isinstance(csv_text, bytes):
            csv_text = csv_text.decode("utf-8-sig")
    else:
        with open(csv_source, encoding="utf-8-sig", newline="") as price_file:
            csv_text = price_file.read()

    reader = csv.DictReader(StringIO(csv_text))
    fieldnames = reader.fieldnames or []
    if len(fieldnames) < 4 or fieldnames[0] != "Date":
        raise ValueError("The CSV needs Date first and at least three ticker columns.")

    tickers = fieldnames[1:]
    dates = []
    prices = {ticker: [] for ticker in tickers}
    for row_number, row in enumerate(reader, start=2):
        date = (row.get("Date") or "").strip()
        if not date:
            raise ValueError(f"Row {row_number} has no Date value.")
        dates.append(date)
        for ticker in tickers:
            try:
                price = float(row[ticker])
            except (TypeError, ValueError) as error:
                raise ValueError(
                    f"Row {row_number} has an invalid price for {ticker}."
                ) from error
            if price <= 0:
                raise ValueError(f"Row {row_number} has a non-positive price for {ticker}.")
            prices[ticker].append(price)

    if len(dates) < 3:
        raise ValueError("The CSV needs at least three monthly price rows.")
    return dates, prices


def monthly_returns(prices):
    """Calculate each ticker's month-over-month percentage returns."""
    return {
        ticker: [
            current_price / previous_price - 1.0
            for previous_price, current_price in zip(values, values[1:])
        ]
        for ticker, values in prices.items()
    }


def correlation_from_returns(left_returns, right_returns):
    """Calculate sample correlation for two equally long monthly-return series."""
    if len(left_returns) != len(right_returns) or len(left_returns) < 2:
        raise ValueError("Correlation needs two equal-length return series.")
    left_mean = fmean(left_returns)
    right_mean = fmean(right_returns)
    numerator = sum(
        (left - left_mean) * (right - right_mean)
        for left, right in zip(left_returns, right_returns)
    )
    denominator = (len(left_returns) - 1) * stdev(left_returns) * stdev(right_returns)
    if denominator == 0:
        raise ValueError("Correlation cannot be calculated when a return series has zero volatility.")
    # Keep insignificant floating-point rounding from producing 1.0000000000000002.
    return max(-1.0, min(1.0, numerator / denominator))


def estimate_from_prices(csv_source, last_36_months=False):
    """Estimate annual return, volatility, and correlation from monthly adjusted-close prices."""
    _, prices = read_monthly_prices(csv_source)
    returns = monthly_returns(prices)
    if last_36_months:
        returns = {ticker: values[-36:] for ticker, values in returns.items()}
    observations = len(next(iter(returns.values())))
    if observations < 2:
        raise ValueError("At least two monthly returns are required for an estimate.")

    sleeves = {
        ticker: {
            "expected_return": fmean(values) * 12,
            "volatility": stdev(values) * sqrt(12),
        }
        for ticker, values in returns.items()
    }
    tickers = list(returns)
    correlations = {ticker: {} for ticker in tickers}
    for left_index, left in enumerate(tickers):
        for right_index, right in enumerate(tickers):
            if left == right:
                correlation = 1.0
            elif right_index < left_index:
                correlation = correlations[right][left]
            else:
                correlation = correlation_from_returns(returns[left], returns[right])
            correlations[left][right] = correlation
    validate_correlation_table(sleeves, correlations)
    return sleeves, correlations


def print_portfolio(name, weights, sleeves, covariances):
    """Print the required portfolio results from calculated values."""
    print(f"\n{name}")
    print("  Weights:")
    for sleeve in sleeves:
        print(f"    {sleeve}: {weights[sleeve]:.1%}")

    calculated_return = expected_return(weights, sleeves)
    calculated_volatility = portfolio_volatility(weights, covariances)
    reserve_weight = reserve_eligible_weight(weights, RESERVE_ELIGIBLE)
    meets_objective = calculated_return >= OBJECTIVE_RETURN

    print(f"  Expected return: {calculated_return:.2%}")
    print(f"  Volatility: {calculated_volatility:.2%}")
    print(f"  Reserve-eligible weight: {reserve_weight:.1%}")
    print(f"  Meets {OBJECTIVE_RETURN:.1%} objective: {'yes' if meets_objective else 'no'}")


def main():
    try:
        validate_correlation_table(SLEEVES, CORRELATIONS)
    except ValueError as error:
        print(f"Input error: {error}")
        return

    covariances = covariance_matrix(SLEEVES, CORRELATIONS)
    portfolios = {
        "Benchmark": benchmark_weights(SLEEVES),
        "Equal weight": equal_weight_weights(SLEEVES),
        "Inverse volatility": inverse_volatility_weights(SLEEVES),
    }
    for name, weights in portfolios.items():
        print_portfolio(name, weights, SLEEVES, covariances)


if __name__ == "__main__":
    main()
