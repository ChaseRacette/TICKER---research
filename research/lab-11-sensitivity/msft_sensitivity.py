"""Lab 11 sensitivity runner for the Microsoft pro-forma.

Run from the repository root:
    python research\lab-11-sensitivity\msft_sensitivity.py

This file leaves msft_proforma.py unchanged. Each scenario changes only one
independent driver from the locked record and holds all other inputs fixed.
"""

# USD millions except per-share data.
OPENING = {
    "revenue": 331_839.0,
    "cash": 76_843.0,
    "ar": 80_876.0,
    "inventory": 1_397.0,
    "ppe": 313_076.0,
    "other_assets": 286_184.0,
    "debt": 40_294.0,
    "other_liabilities": 275_695.0,
    "equity": 442_387.0,
}

YEARS = [2027, 2028, 2029, 2030, 2031]
BASE_GROWTH = [0.18, 0.14, 0.11, 0.08, 0.05]
BASE_CAPEX_TO_REVENUE = [0.34, 0.30, 0.27, 0.23, 0.20]
GROSS_MARGIN = [0.675, 0.680, 0.685, 0.688, 0.690]
SGA_TO_GROSS_PROFIT = 0.155
RND_TO_GROSS_PROFIT = 0.158
TAX_RATE = 0.19
AR_DAYS = 89.0
INVENTORY_DAYS = 4.8
OTHER_ASSET_TO_REVENUE_CHANGE = 0.10
OTHER_LIABILITY_TO_REVENUE_CHANGE = 0.10
DEPRECIATION_TO_OPENING_PPE = 0.110
DEBT_REPAYMENT = 0.0
SHARE_REPURCHASES = 30_000.0
MINIMUM_CASH = 25_000.0
COST_OF_EQUITY = 0.10
TERMINAL_GROWTH = 0.025
SHARES = 7_425.545491


def run_case(growth_rates, capex_to_revenue):
    """Return five linked years and the FCFE valuation for supplied inputs."""
    prior = OPENING.copy()
    years = []

    for year, growth, gross_margin, capex_ratio in zip(
        YEARS, growth_rates, GROSS_MARGIN, capex_to_revenue
    ):
        revenue = prior["revenue"] * (1.0 + growth)
        gross_profit = revenue * gross_margin
        operating_income = gross_profit * (1.0 - SGA_TO_GROSS_PROFIT - RND_TO_GROSS_PROFIT)
        net_income = operating_income * (1.0 - TAX_RATE)
        depreciation = prior["ppe"] * DEPRECIATION_TO_OPENING_PPE
        capex = revenue * capex_ratio
        ar = revenue * AR_DAYS / 365.0
        inventory = (revenue - gross_profit) * INVENTORY_DAYS / 365.0
        revenue_change = revenue - prior["revenue"]
        other_assets = prior["other_assets"] + OTHER_ASSET_TO_REVENUE_CHANGE * revenue_change
        other_liabilities = (
            prior["other_liabilities"]
            + OTHER_LIABILITY_TO_REVENUE_CHANGE * revenue_change
        )
        ppe = prior["ppe"] + capex - depreciation
        equity = prior["equity"] + net_income - SHARE_REPURCHASES
        fcfe = (
            net_income
            + depreciation
            - capex
            - (ar - prior["ar"])
            - (inventory - prior["inventory"])
            - (other_assets - prior["other_assets"])
            + (other_liabilities - prior["other_liabilities"])
            - DEBT_REPAYMENT
        )
        cash = prior["cash"] + fcfe - SHARE_REPURCHASES
        total_assets = cash + ar + inventory + ppe + other_assets
        total_liabilities_equity = prior["debt"] + other_liabilities + equity
        balance_gap = total_assets - total_liabilities_equity
        if abs(balance_gap) > 0.01:
            raise ValueError(f"FY{year}E does not balance: gap ${balance_gap:,.1f}m")
        if cash < MINIMUM_CASH:
            raise ValueError(f"FY{year}E cash is below floor: ${cash:,.1f}m")

        current = {
            "year": year, "revenue": revenue, "operating_income": operating_income,
            "fcfe": fcfe, "cash": cash, "ar": ar, "inventory": inventory,
            "ppe": ppe, "other_assets": other_assets,
            "other_liabilities": other_liabilities, "equity": equity,
        }
        years.append(current)
        prior = current
        prior["debt"] = OPENING["debt"]

    pv_fcfe = sum(y["fcfe"] / ((1.0 + COST_OF_EQUITY) ** period)
                  for period, y in enumerate(years, start=1))
    terminal_value = years[-1]["fcfe"] * (1.0 + TERMINAL_GROWTH) / (COST_OF_EQUITY - TERMINAL_GROWTH)
    equity_value = pv_fcfe + terminal_value / ((1.0 + COST_OF_EQUITY) ** len(years))
    return years, equity_value / SHARES, min(y["cash"] for y in years)


def report_case(driver, case, growth_rates, capex_to_revenue):
    years, value_per_share, minimum_cash = run_case(growth_rates, capex_to_revenue)
    final = years[-1]
    print(
        f"{driver:<18} {case:<6} "
        f"FY2031 operating income: ${final['operating_income']:>12,.1f}m | "
        f"FY2031 FCFE: ${final['fcfe']:>12,.1f}m | "
        f"Value/share: ${value_per_share:>8,.2f} | "
        f"FY2027-31 checks: passed; low cash ${minimum_cash:,.1f}m"
    )


def main():
    growth_lower = [rate - 0.02 for rate in BASE_GROWTH]
    growth_higher = [rate + 0.02 for rate in BASE_GROWTH]
    capex_lower = [rate - 0.05 for rate in BASE_CAPEX_TO_REVENUE]
    capex_higher = [rate + 0.05 for rate in BASE_CAPEX_TO_REVENUE]

    print("Lab 11 Microsoft sensitivity - FCFE, USD millions except value per share")
    print("All scenarios retain the same share count and all non-tested assumptions.")
    print("-" * 118)
    report_case("Revenue growth", "Lower", growth_lower, BASE_CAPEX_TO_REVENUE)
    report_case("Revenue growth", "Base", BASE_GROWTH, BASE_CAPEX_TO_REVENUE)
    report_case("Revenue growth", "Higher", growth_higher, BASE_CAPEX_TO_REVENUE)
    print()
    report_case("Capex / revenue", "Lower", BASE_GROWTH, capex_lower)
    report_case("Capex / revenue", "Base", BASE_GROWTH, BASE_CAPEX_TO_REVENUE)
    report_case("Capex / revenue", "Higher", BASE_GROWTH, capex_higher)


if __name__ == "__main__":
    main()
