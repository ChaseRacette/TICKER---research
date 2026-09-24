"""Lab 10: Microsoft five-year three-statement pro-forma.

Run from the repository root:
    python msft_proforma.py

USD millions except per-share data. This is an educational simplified model.
It keeps the balance check active and will not value an unbalanced forecast.
"""

# =============================================================================
# OPENING BALANCE SHEET: FY2026 ACTUAL (USD millions)
# Source: Microsoft FY2026 10-K, Item 8 - Consolidated Balance Sheets.
# "Other" lines aggregate disclosed items not separately forecast in this model.
# =============================================================================
OPENING = {
    "revenue": 331_839.0,
    "cash_and_investments": 76_843.0,
    "accounts_receivable": 80_876.0,
    "inventory": 1_397.0,
    "ppe": 313_076.0,
    "other_assets": 286_184.0,
    "debt": 40_294.0,
    "other_liabilities": 275_695.0,
    "equity": 442_387.0,
}

# =============================================================================
# ASSUMPTIONS
# Labels and reasons are in the accompanying Lab 10 history-and-assumptions file.
# =============================================================================
YEARS = [2027, 2028, 2029, 2030, 2031]
REVENUE_GROWTH = [0.18, 0.14, 0.11, 0.08, 0.05]       # judgment: growth tapers
GROSS_MARGIN = [0.675, 0.680, 0.685, 0.688, 0.690]    # judgment: partial recovery
SGA_TO_GROSS_PROFIT = 0.155                           # judgment: near FY2026 proxy
RND_TO_GROSS_PROFIT = 0.158                           # history-based: FY2026 implied ratio
TAX_RATE = 0.19                                       # history: near FY2026 effective rate

AR_DAYS = 89.0                                        # history: FY2026 AR / revenue x 365
INVENTORY_DAYS = 4.8                                  # history: FY2024-26 midpoint
OTHER_ASSET_TO_REVENUE_CHANGE = 0.10                  # judgment: modest working-asset use
OTHER_LIABILITY_TO_REVENUE_CHANGE = 0.10              # judgment: matching operating accruals

DEPRECIATION_TO_OPENING_PPE = 0.110                   # history: FY2024-26 average
CAPEX_TO_REVENUE = [0.34, 0.30, 0.27, 0.23, 0.20]      # judgment: AI capex normalizes slowly
DEBT_REPAYMENT = 0.0                                  # judgment: hold reported debt constant
SHARE_REPURCHASES = 30_000.0                           # judgment: simplified annual capital return
MINIMUM_CASH = 25_000.0                                # judgment: liquidity floor
REVOLVER_LIMIT = 100_000.0                             # judgment: emergency balancing financing
REVOLVER_RATE = 0.05                                  # judgment: illustrative borrowing cost
COST_OF_EQUITY = 0.10                                 # judgment: valuation discount rate
TERMINAL_GROWTH = 0.025                               # judgment: mature long-run growth
SHARES = 7_425.545491                                 # fact: July 23, 2026 shares outstanding, millions


def assert_balanced(years):
    """Refuse to value an unbalanced forecast or a cash-floor breach."""
    for year in years:
        if abs(year["balance_gap"]) > 0.01:
            raise ValueError(
                f"FY{year['year']}E does not balance: gap ${year['balance_gap']:,.1f}m"
            )
        if year["cash_and_investments"] < MINIMUM_CASH - 0.01:
            raise ValueError(
                f"FY{year['year']}E cash is below minimum: "
                f"${year['cash_and_investments']:,.1f}m"
            )


def project_year(prior, year_number, growth, gross_margin, capex_ratio):
    """Project income statement, balance sheet, and FCFE in a linked order."""
    revenue = prior["revenue"] * (1.0 + growth)
    gross_profit = revenue * gross_margin
    sga_proxy = gross_profit * SGA_TO_GROSS_PROFIT
    research_and_development = gross_profit * RND_TO_GROSS_PROFIT
    depreciation = prior["ppe"] * DEPRECIATION_TO_OPENING_PPE

    # Microsoft reports gross profit after depreciation in cost of revenue.
    # Therefore, depreciation is added back in cash flow but is not subtracted again here.
    operating_income = gross_profit - sga_proxy - research_and_development
    interest = prior["revolver"] * REVOLVER_RATE
    pretax_income = operating_income - interest
    tax = max(0.0, pretax_income) * TAX_RATE
    net_income = pretax_income - tax

    cost_of_revenue = revenue - gross_profit
    accounts_receivable = revenue * AR_DAYS / 365.0
    inventory = cost_of_revenue * INVENTORY_DAYS / 365.0
    capex = revenue * capex_ratio
    ppe = prior["ppe"] + capex - depreciation
    revenue_change = revenue - prior["revenue"]
    other_assets = prior["other_assets"] + OTHER_ASSET_TO_REVENUE_CHANGE * revenue_change
    other_liabilities = (
        prior["other_liabilities"] + OTHER_LIABILITY_TO_REVENUE_CHANGE * revenue_change
    )
    debt = prior["debt"] - DEBT_REPAYMENT
    equity = prior["equity"] + net_income - SHARE_REPURCHASES

    change_ar = accounts_receivable - prior["accounts_receivable"]
    change_inventory = inventory - prior["inventory"]
    change_other_assets = other_assets - prior["other_assets"]
    change_other_liabilities = other_liabilities - prior["other_liabilities"]
    fcfe = (
        net_income
        + depreciation
        - capex
        - change_ar
        - change_inventory
        - change_other_assets
        + change_other_liabilities
        - DEBT_REPAYMENT
    )

    cash_before_revolver = prior["cash_and_investments"] + fcfe - SHARE_REPURCHASES
    draw = min(max(0.0, MINIMUM_CASH - cash_before_revolver), REVOLVER_LIMIT - prior["revolver"])
    repay = min(prior["revolver"], max(0.0, cash_before_revolver - MINIMUM_CASH))
    revolver = prior["revolver"] + draw - repay
    cash_and_investments = cash_before_revolver + draw - repay

    total_assets = accounts_receivable + inventory + ppe + other_assets + cash_and_investments
    total_liabilities_equity = debt + other_liabilities + revolver + equity
    balance_gap = total_assets - total_liabilities_equity

    return {
        "year": year_number,
        "revenue": revenue,
        "gross_profit": gross_profit,
        "sga_proxy": sga_proxy,
        "research_and_development": research_and_development,
        "depreciation": depreciation,
        "operating_income": operating_income,
        "interest": interest,
        "pretax_income": pretax_income,
        "tax": tax,
        "net_income": net_income,
        "accounts_receivable": accounts_receivable,
        "inventory": inventory,
        "ppe": ppe,
        "other_assets": other_assets,
        "cash_and_investments": cash_and_investments,
        "debt": debt,
        "other_liabilities": other_liabilities,
        "revolver": revolver,
        "equity": equity,
        "change_ar": change_ar,
        "change_inventory": change_inventory,
        "change_other_assets": change_other_assets,
        "change_other_liabilities": change_other_liabilities,
        "capex": capex,
        "fcfe": fcfe,
        "share_repurchases": SHARE_REPURCHASES,
        "total_assets": total_assets,
        "total_liabilities_equity": total_liabilities_equity,
        "balance_gap": balance_gap,
    }


def print_table(title, rows, years):
    print(f"\n{title}")
    print(f"{'Line item':<35}" + "".join(f"{'FY' + str(y['year']) + 'E':>15}" for y in years))
    print("-" * (35 + 15 * len(years)))
    for label, key in rows:
        print(f"{label:<35}" + "".join(f"{y[key]:>15,.1f}" for y in years))


def main():
    opening_gap = (
        OPENING["cash_and_investments"]
        + OPENING["accounts_receivable"]
        + OPENING["inventory"]
        + OPENING["ppe"]
        + OPENING["other_assets"]
        - OPENING["debt"]
        - OPENING["other_liabilities"]
        - OPENING["equity"]
    )
    if abs(opening_gap) > 0.01:
        raise ValueError(f"FY2026A opening balance sheet does not balance: gap ${opening_gap:,.1f}m")

    years = []
    prior = OPENING.copy()
    prior["revolver"] = 0.0
    for year, growth, margin, capex_ratio in zip(YEARS, REVENUE_GROWTH, GROSS_MARGIN, CAPEX_TO_REVENUE):
        current = project_year(prior, year, growth, margin, capex_ratio)
        years.append(current)
        prior = current

    print_table("Income Statement (USD millions)", [
        ("Revenue", "revenue"), ("Gross profit", "gross_profit"),
        ("SG&A proxy", "sga_proxy"), ("Research and development", "research_and_development"),
        ("Operating income", "operating_income"), ("Interest", "interest"),
        ("Tax", "tax"), ("Net income", "net_income"),
    ], years)
    print_table("Balance Sheet (USD millions)", [
        ("Cash and short-term investments", "cash_and_investments"),
        ("Accounts receivable", "accounts_receivable"), ("Inventory", "inventory"),
        ("PP&E, net", "ppe"), ("Other assets", "other_assets"),
        ("Total assets", "total_assets"), ("Debt", "debt"),
        ("Other liabilities", "other_liabilities"), ("Revolver", "revolver"),
        ("Equity", "equity"), ("Liabilities + equity", "total_liabilities_equity"),
    ], years)
    print_table("Cash Flow / FCFE (USD millions)", [
        ("Net income", "net_income"), ("Depreciation", "depreciation"),
        ("Capital spending", "capex"), ("Change in accounts receivable", "change_ar"),
        ("Change in inventory", "change_inventory"),
        ("Change in other assets", "change_other_assets"),
        ("Change in other liabilities", "change_other_liabilities"),
        ("Free cash flow to equity", "fcfe"),
        ("Share repurchases", "share_repurchases"),
    ], years)

    print("\nChecks")
    print(f"FY2026A opening balance-sheet gap: ${opening_gap:,.1f}m")
    for year in years:
        print(
            f"FY{year['year']}E: assets - liabilities - equity = ${year['balance_gap']:,.1f}m; "
            f"cash >= minimum = {year['cash_and_investments'] >= MINIMUM_CASH}"
        )

    assert_balanced(years)
    if years[-1]["fcfe"] <= 0.0:
        raise ValueError("FY2031E has negative FCFE; terminal value is not meaningful.")

    pv_fcfe = sum(y["fcfe"] / ((1.0 + COST_OF_EQUITY) ** i) for i, y in enumerate(years, 1))
    terminal_value = years[-1]["fcfe"] * (1.0 + TERMINAL_GROWTH) / (COST_OF_EQUITY - TERMINAL_GROWTH)
    pv_terminal_value = terminal_value / ((1.0 + COST_OF_EQUITY) ** len(years))
    equity_value = pv_fcfe + pv_terminal_value
    value_per_share = equity_value / SHARES
    print("\nEquity Valuation")
    print(f"Present value of five FCFE: ${pv_fcfe:,.1f}m")
    print(f"Present value of terminal value: ${pv_terminal_value:,.1f}m")
    print(f"Equity value: ${equity_value:,.1f}m")
    print(f"Value per share: ${value_per_share:,.2f}")


if __name__ == "__main__":
    main()
