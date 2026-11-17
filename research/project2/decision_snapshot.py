"""Print a dated Markdown snapshot of the current Northstar decision."""
from __future__ import annotations

import argparse
from copy import deepcopy
from datetime import datetime, timezone

from portfolio_engine import (
    benchmark_baseline,
    equal_weight_baseline,
    estimate_inputs_from_prices,
    fetch_yahoo_monthly_prices,
    recommended_portfolio,
)


def percentages(weights):
    return "; ".join(f"{sleeve}: {weight:.0%}" for sleeve, weight in weights.items())


def row(name, portfolio):
    return (
        f"| {name} | {portfolio['verdict'].upper()} | {portfolio['expected_return']:.2%} | "
        f"{portfolio['volatility']:.2%} | {percentages(portfolio['weights'])} |"
    )


def main():
    parser = argparse.ArgumentParser(description="Print the Northstar decision snapshot.")
    parser.add_argument(
        "--bond-return-percent",
        type=float,
        help="Replace LQD's historical annual expected-return input for a changed-input stress run.",
    )
    args = parser.parse_args()
    dates, prices = fetch_yahoo_monthly_prices()
    estimates, correlations = estimate_inputs_from_prices(prices)
    stress_note = None
    if args.bond_return_percent is not None:
        historical_bond_return = estimates["Investment-grade bonds"]["expected_return"]
        estimates = deepcopy(estimates)
        estimates["Investment-grade bonds"]["expected_return"] = args.bond_return_percent / 100
        stress_note = (
            "Changed-input stress run: investment-grade bond expected return replaced from "
            f"{historical_bond_return:.2%} to {args.bond_return_percent:.1f}%."
        )
    equal = equal_weight_baseline(estimates, correlations)
    benchmark = benchmark_baseline(estimates, correlations)
    recommended = recommended_portfolio(estimates, correlations)
    signal = "Growth trend intact" if prices["ACWI"][-1] >= sum(prices["ACWI"][-10:]) / 10 else "Caution: trend below average"

    print("# Northstar Decision Output Snapshot")
    print()
    print(f"Generated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}")
    print(f"Yahoo Finance monthly adjusted-close window: {dates[0]} through {dates[-1]} (60 completed monthly returns)")
    if stress_note:
        print(stress_note)
    print()
    print("| Portfolio | Mandate verdict | Historical expected return | Estimated volatility | Allocation |")
    print("|---|---|---:|---:|---|")
    print(row("Equal weight", equal))
    print(row("70/20/10 benchmark", benchmark))
    print(row("Northstar constrained recommendation", recommended))
    print()
    print(f"Point-in-time monitor: **{signal}** as of {dates[-1]}. It is monitoring-only and does not automatically change allocations.")
    print()
    print("Committee decision: **PILOT**. Pause new allocations if no feasible portfolio clears the CPI + 5% objective and every guardrail, or when a 25% drawdown triggers committee review.")


if __name__ == "__main__":
    main()
