r"""Lab 13 Meridian Foundation Reserve mandate checker.

Run from the repository root:
    python research\lab-13-mandate\mandate.py

Run the required long-only probe without editing the saved base inputs:
    python research\lab-13-mandate\mandate.py --probe
"""

from copy import deepcopy
import sys


# Editable inputs
HOLDINGS = {
    "Cash": {
        "issuer": "none",
        "redeem_days": 0,
        "reserve_eligible": True,
        "issuer_exempt": True,
    },
    "Treasury bills": {
        "issuer": "U.S. Treasury",
        "redeem_days": 1,
        "reserve_eligible": True,
        "issuer_exempt": True,
    },
    "Treasury 10-year note": {
        "issuer": "U.S. Treasury",
        "redeem_days": 1,
        "reserve_eligible": True,
        "issuer_exempt": True,
    },
    "Global equity index fund": {
        "issuer": "diversified fund",
        "redeem_days": 2,
        "reserve_eligible": False,
        "issuer_exempt": True,
    },
    "Investment-grade bond fund": {
        "issuer": "diversified fund",
        "redeem_days": 3,
        "reserve_eligible": False,
        "issuer_exempt": True,
    },
    "Private real estate fund": {
        "issuer": "diversified fund",
        "redeem_days": 90,
        "reserve_eligible": False,
        "issuer_exempt": True,
    },
    "Acme Corp bonds": {
        "issuer": "Acme Corp",
        "redeem_days": 4,
        "reserve_eligible": False,
        "issuer_exempt": False,
    },
    "Acme Corp stock": {
        "issuer": "Acme Corp",
        "redeem_days": 1,
        "reserve_eligible": False,
        "issuer_exempt": False,
    },
}

CANDIDATES = {
    "A": {
        "Cash": 2, "Treasury bills": 2, "Treasury 10-year note": 10,
        "Global equity index fund": 60, "Investment-grade bond fund": 26,
        "Private real estate fund": 0, "Acme Corp bonds": 0, "Acme Corp stock": 0,
    },
    "B": {
        "Cash": 1, "Treasury bills": 0, "Treasury 10-year note": 0,
        "Global equity index fund": 55, "Investment-grade bond fund": 20,
        "Private real estate fund": 15, "Acme Corp bonds": 5, "Acme Corp stock": 4,
    },
    "C": {
        "Cash": 1, "Treasury bills": 1, "Treasury 10-year note": 0,
        "Global equity index fund": 70, "Investment-grade bond fund": 20,
        "Private real estate fund": 0, "Acme Corp bonds": 0, "Acme Corp stock": 8,
    },
    # Candidate D is the Lab 13 attack: checkable-rule compliant but potentially unsuitable.
    "D": {
        "Cash": 3, "Treasury bills": 0, "Treasury 10-year note": 0,
        "Global equity index fund": 89, "Investment-grade bond fund": 8,
        "Private real estate fund": 0, "Acme Corp bonds": 0, "Acme Corp stock": 0,
    },
    # Candidate E is the Lab 14 benchmark: 40% IG bonds and 60% global equity.
    "E": {
        "Cash": 0, "Treasury bills": 0, "Treasury 10-year note": 0,
        "Global equity index fund": 60, "Investment-grade bond fund": 40,
        "Private real estate fund": 0, "Acme Corp bonds": 0, "Acme Corp stock": 0,
    },
}

RESERVE_SIZE = 100.0  # USD millions
QUARTERLY_DISTRIBUTION = 0.75  # USD millions
QUARTERS_TO_COVER = 4
LIQUIDITY_WINDOW_DAYS = 5
MINIMUM_LIQUID_SHARE = 90.0  # percent
ISSUER_LIMIT = 8.0  # percent


def reserve_minimum_percent():
    return QUARTERS_TO_COVER * QUARTERLY_DISTRIBUTION / RESERVE_SIZE * 100


def issuer_exposures(weights):
    """Aggregate every non-exempt holding belonging to the same company."""
    exposures = {}
    for holding, weight in weights.items():
        metadata = HOLDINGS[holding]
        if not metadata["issuer_exempt"]:
            issuer = metadata["issuer"]
            exposures[issuer] = exposures.get(issuer, 0.0) + weight
    return exposures


def rule_results(weights):
    total_weight = sum(weights.values())
    lowest_weight = min(weights.values())
    reserve_weight = sum(
        weights[holding]
        for holding, metadata in HOLDINGS.items()
        if metadata["reserve_eligible"]
    )
    liquid_weight = sum(
        weights[holding]
        for holding, metadata in HOLDINGS.items()
        if metadata["redeem_days"] <= LIQUIDITY_WINDOW_DAYS
    )
    exposures = issuer_exposures(weights)
    largest_company = max(exposures.values(), default=0.0)

    return [
        ("Weights sum to 100", total_weight, abs(total_weight - 100.0) < 1e-9),
        ("Long-only (lowest weight)", lowest_weight, lowest_weight >= 0.0),
        (
            f"Reserve-eligible weight >= {reserve_minimum_percent():.1f}%",
            reserve_weight,
            reserve_weight >= reserve_minimum_percent(),
        ),
        (
            f"Redeemable within {LIQUIDITY_WINDOW_DAYS} days >= {MINIMUM_LIQUID_SHARE:.1f}%",
            liquid_weight,
            liquid_weight >= MINIMUM_LIQUID_SHARE,
        ),
        (
            f"Largest single company <= {ISSUER_LIMIT:.1f}%",
            largest_company,
            largest_company <= ISSUER_LIMIT,
        ),
    ]


def print_candidate(name, weights):
    print(f"\nCandidate {name}")
    failures = 0
    for label, measured, passed in rule_results(weights):
        status = "pass" if passed else "FAIL"
        print(f"  {label}: {measured:.1f}% {status}")
        failures += not passed
    print("  Calendar-year loss: requires CIO clarification")
    if failures:
        print(f"  Verdict: fails {failures} rule(s)")
    else:
        print("  Verdict: passes every checkable rule")


def main():
    print(
        "Reserve minimum: "
        f"{reserve_minimum_percent():.1f}% "
        "(quarters x distribution / reserve size)"
    )

    if "--probe" in sys.argv:
        probe = deepcopy(CANDIDATES["A"])
        probe["Cash"] = -2
        probe["Global equity index fund"] = 64
        print_candidate("A - long-only probe", probe)
        return

    for name, weights in CANDIDATES.items():
        print_candidate(name, weights)


if __name__ == "__main__":
    main()
