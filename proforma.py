"""Lab 09: ABG five-year three-statement pro-forma engine.

Run from the repository root:
    python proforma.py

USD millions except per-share data.  Inputs reproduce the course's ABG base case.
"""

# =============================================================================
# OPENING BALANCE SHEET: FY2025 ACTUAL (USD millions)
# =============================================================================
OPENING = {
    "revenue": 17_999.0,
    "inventory": 2_135.8,
    "ppe": 3_070.4,
    "other_assets": 6_371.6,
    "cash": 40.4,
    "floor_plan": 2_027.0,
    "term_debt": 3_572.0,
    "other_liabilities": 2_127.5,
    "equity": 3_891.7,
    "revolver": 0.0,
}

# =============================================================================
# ASSUMPTIONS: history, guidance, or judgment as specified in Lab 09
# =============================================================================
YEARS = [2026, 2027, 2028, 2029, 2030]
ORGANIC_GROWTH = 0.018  # judgment
GROSS_MARGIN = 0.1705  # judgment
SGA_TO_GROSS_PROFIT = [0.665, 0.655, 0.645, 0.645, 0.645]  # judgment
DEPRECIATION_TO_OPENING_PPE = 82.4 / 3_070.4  # history
IMPAIRMENT = 120.0  # judgment; noncash
CAPEX = 250.0  # guidance
TAX_RATE = 0.255  # judgment
INVENTORY_DAYS = 2_135.8 / (17_999.0 - 3_071.7) * 365.0  # history
FLOOR_PLAN_TO_INVENTORY = 2_027.0 / 2_135.8  # history
OTHER_WORKING_CAPITAL_RATE = 0.008  # judgment
MINIMUM_CASH = 25.0  # history
REVOLVER_LIMIT = 850.0  # judgment
REVOLVER_RATE = 0.06  # judgment
DEBT_REPAYMENT = 150.0  # judgment
SHARE_BUYBACK = 150.0  # judgment
FLOOR_PLAN_RATE = 0.0467  # history
TERM_DEBT_RATE = 0.0544  # history
COST_OF_EQUITY = 0.10  # judgment
TERMINAL_GROWTH = 0.025  # judgment
SHARES = 17.951349  # fact: June 30, 2026 10-Q

# For the class break test only, change to {2026: 40.4}; the assertion must fail.
CASH_OVERRIDE = {}


def assert_balanced(years):
    """Refuse valuation if a projected balance sheet does not tie or cash is too low."""
    for year in years:
        if abs(year["balance_gap"]) > 0.0001:
            raise ValueError(
                f"FY{year['year']}E does not balance: gap {year['balance_gap']:.1f}"
            )
        if year["cash"] < MINIMUM_CASH - 0.0001:
            raise ValueError(
                f"FY{year['year']}E cash is below minimum: {year['cash']:.1f}"
            )


def project_year(prior, year_number, sga_ratio):
    """Build one income statement, balance sheet, and cash flow in the required order."""
    revenue = prior["revenue"] * (1.0 + ORGANIC_GROWTH)
    gross_profit = revenue * GROSS_MARGIN
    sga = gross_profit * sga_ratio
    depreciation = prior["ppe"] * DEPRECIATION_TO_OPENING_PPE
    operating_income = gross_profit - sga - depreciation - IMPAIRMENT
    interest = (
        prior["floor_plan"] * FLOOR_PLAN_RATE
        + prior["term_debt"] * TERM_DEBT_RATE
        + prior["revolver"] * REVOLVER_RATE
    )
    pretax_income = operating_income - interest
    tax = max(0.0, pretax_income) * TAX_RATE
    net_income = pretax_income - tax

    cost_of_sales = revenue - gross_profit
    inventory = cost_of_sales * INVENTORY_DAYS / 365.0
    floor_plan = inventory * FLOOR_PLAN_TO_INVENTORY
    ppe = prior["ppe"] + CAPEX - depreciation
    revenue_change = revenue - prior["revenue"]
    other_working_capital_change = OTHER_WORKING_CAPITAL_RATE * revenue_change
    other_assets = prior["other_assets"] + other_working_capital_change - IMPAIRMENT
    term_debt = prior["term_debt"] - DEBT_REPAYMENT
    other_liabilities = prior["other_liabilities"]
    equity = prior["equity"] + net_income - SHARE_BUYBACK

    change_inventory = inventory - prior["inventory"]
    change_floor_plan = floor_plan - prior["floor_plan"]
    fcfe = (
        net_income
        + depreciation
        + IMPAIRMENT
        - CAPEX
        - change_inventory
        - other_working_capital_change
        + change_floor_plan
        - DEBT_REPAYMENT
    )

    cash_before_revolver = prior["cash"] + fcfe - SHARE_BUYBACK
    revolver = prior["revolver"]
    cash = cash_before_revolver
    if cash < MINIMUM_CASH:
        draw = MINIMUM_CASH - cash
        if revolver + draw > REVOLVER_LIMIT:
            raise ValueError(f"FY{year_number}E revolver limit exceeded.")
        revolver += draw
        cash += draw
    elif cash > MINIMUM_CASH and revolver > 0.0:
        revolver_repayment = min(revolver, cash - MINIMUM_CASH)
        revolver -= revolver_repayment
        cash -= revolver_repayment

    if year_number in CASH_OVERRIDE:
        cash = CASH_OVERRIDE[year_number]

    assets = inventory + ppe + other_assets + cash
    liabilities = floor_plan + term_debt + other_liabilities + revolver
    balance_gap = assets - liabilities - equity

    return {
        "year": year_number,
        "revenue": revenue,
        "gross_profit": gross_profit,
        "sga": sga,
        "depreciation": depreciation,
        "impairment": IMPAIRMENT,
        "operating_income": operating_income,
        "interest": interest,
        "pretax_income": pretax_income,
        "tax": tax,
        "net_income": net_income,
        "inventory": inventory,
        "ppe": ppe,
        "other_assets": other_assets,
        "cash": cash,
        "floor_plan": floor_plan,
        "term_debt": term_debt,
        "revolver": revolver,
        "other_liabilities": other_liabilities,
        "equity": equity,
        "change_inventory": change_inventory,
        "other_working_capital_change": other_working_capital_change,
        "change_floor_plan": change_floor_plan,
        "capex": CAPEX,
        "debt_repayment": DEBT_REPAYMENT,
        "fcfe": fcfe,
        "assets": assets,
        "liabilities": liabilities,
        "balance_gap": balance_gap,
    }


def print_table(title, rows, years):
    """Print a one-decimal table with fiscal years across columns."""
    print(f"\n{title}")
    print(f"{'Line item':<34}" + "".join(f"{'FY' + str(year['year']) + 'E':>14}" for year in years))
    print("-" * (34 + 14 * len(years)))
    for label, key in rows:
        print(f"{label:<34}" + "".join(f"{year[key]:>14,.1f}" for year in years))


def main():
    projected_years = []
    prior = OPENING.copy()
    for year_number, sga_ratio in zip(YEARS, SGA_TO_GROSS_PROFIT):
        current = project_year(prior, year_number, sga_ratio)
        projected_years.append(current)
        prior = current

    print_table(
        "Income Statement (USD millions)",
        [
            ("Revenue", "revenue"),
            ("Gross profit", "gross_profit"),
            ("SG&A", "sga"),
            ("Depreciation", "depreciation"),
            ("Impairment", "impairment"),
            ("Operating income", "operating_income"),
            ("Interest", "interest"),
            ("Pretax income", "pretax_income"),
            ("Tax", "tax"),
            ("Net income", "net_income"),
        ],
        projected_years,
    )
    print_table(
        "Balance Sheet (USD millions)",
        [
            ("Inventory", "inventory"),
            ("Property & equipment", "ppe"),
            ("Other assets", "other_assets"),
            ("Cash", "cash"),
            ("Total assets", "assets"),
            ("Floor plan", "floor_plan"),
            ("Term debt", "term_debt"),
            ("Revolver", "revolver"),
            ("Other liabilities", "other_liabilities"),
            ("Equity", "equity"),
        ],
        projected_years,
    )
    print_table(
        "Cash Flow / FCFE (USD millions)",
        [
            ("Net income", "net_income"),
            ("Depreciation", "depreciation"),
            ("Impairment", "impairment"),
            ("Capital spending", "capex"),
            ("Change in inventory", "change_inventory"),
            ("Change in other working capital", "other_working_capital_change"),
            ("Change in floor plan", "change_floor_plan"),
            ("Debt repayment", "debt_repayment"),
            ("Free cash flow to equity", "fcfe"),
        ],
        projected_years,
    )

    print("\nChecks")
    for year in projected_years:
        print(
            f"FY{year['year']}E: assets − liabilities − equity = {year['balance_gap']:.1f}; "
            f"cash >= minimum = {year['cash'] >= MINIMUM_CASH}"
        )

    # The valuation may run only after every projected balance sheet passes.
    assert_balanced(projected_years)

    pv_fcfe = sum(
        year["fcfe"] / ((1.0 + COST_OF_EQUITY) ** index)
        for index, year in enumerate(projected_years, start=1)
    )
    terminal_fcfe = (projected_years[-1]["fcfe"] + DEBT_REPAYMENT) * (1.0 + TERMINAL_GROWTH)
    terminal_value = terminal_fcfe / (COST_OF_EQUITY - TERMINAL_GROWTH)
    pv_terminal_value = terminal_value / ((1.0 + COST_OF_EQUITY) ** len(projected_years))
    equity_value = pv_fcfe + pv_terminal_value
    value_per_share = equity_value / SHARES

    print("\nEquity Valuation")
    print(f"Present value of five FCFE: ${pv_fcfe:,.1f} million")
    print(f"Present value of terminal value: ${pv_terminal_value:,.1f} million")
    print(f"Equity value: ${equity_value:,.1f} million")
    print(f"Share of value after 2030: {pv_terminal_value / equity_value:.1%}")
    print(f"Value per share: ${value_per_share:,.2f}")


if __name__ == "__main__":
    main()
