r"""Lab 14 — Meridian portfolio baseline risk engine.

Run from the Course/Work Folder:
    .\.venv\Scripts\python.exe -E MSFT\ticker-research\research\lab-14-portfolio\portfolio.py
"""

from math import sqrt


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
    return sum(weights[sleeve] for sleeve in reserve_eligible)


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
