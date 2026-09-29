"""Lab 11: one-at-a-time sensitivity analysis for msft_proforma.py.

Run from repository root:
    python research\lab-11-sensitivity\msft_sensitivity.py
"""

from copy import deepcopy


# Base input set copied from msft_proforma.py. USD millions except per-share data.
BASE_INPUTS = {
    "opening": {"revenue": 331_839.0, "cash": 76_843.0, "ar": 80_876.0,
                "inventory": 1_397.0, "ppe": 313_076.0, "other_assets": 286_184.0,
                "debt": 40_294.0, "other_liabilities": 275_695.0, "equity": 442_387.0},
    "years": [2027, 2028, 2029, 2030, 2031],
    "revenue_growth": [0.18, 0.14, 0.11, 0.08, 0.05],
    "capex_to_revenue": [0.34, 0.30, 0.27, 0.23, 0.20],
    "gross_margin": [0.675, 0.680, 0.685, 0.688, 0.690],
    "sga_to_gross_profit": 0.155, "rnd_to_gross_profit": 0.158,
    "tax_rate": 0.19, "ar_days": 89.0, "inventory_days": 4.8,
    "other_asset_to_revenue_change": 0.10,
    "other_liability_to_revenue_change": 0.10,
    "depreciation_to_opening_ppe": 0.110, "debt_repayment": 0.0,
    "share_repayments": 30_000.0, "minimum_cash": 25_000.0,
    "cost_of_equity": 0.10, "terminal_growth": 0.025, "shares": 7_425.545491,
}

# Existing locked ranges only. Percentage points are not percent changes.
DRIVERS = {
    "Revenue growth": {
        "key": "revenue_growth", "unit": "% of prior-year revenue; annual growth rates",
        "lower": [0.16, 0.12, 0.09, 0.06, 0.03],
        "base": BASE_INPUTS["revenue_growth"],
        "higher": [0.20, 0.16, 0.13, 0.10, 0.07],
    },
    "AI/cloud capex": {
        "key": "capex_to_revenue", "unit": "% of revenue; capital spending intensity",
        "lower": [0.29, 0.25, 0.22, 0.18, 0.15],
        "base": BASE_INPUTS["capex_to_revenue"],
        "higher": [0.39, 0.35, 0.32, 0.28, 0.25],
    },
}


def values_as_percent(values):
    return ", ".join(f"{value:.0%}" for value in values)


def run_linked_model(inputs):
    """Run linked statements; retain signed FCFE and mark invalid valuation."""
    prior = deepcopy(inputs["opening"])
    years, invalid_reason = [], None
    for year, growth, margin, capex_rate in zip(
        inputs["years"], inputs["revenue_growth"], inputs["gross_margin"], inputs["capex_to_revenue"]
    ):
        revenue = prior["revenue"] * (1 + growth)
        gross_profit = revenue * margin
        sga = gross_profit * inputs["sga_to_gross_profit"]
        rnd = gross_profit * inputs["rnd_to_gross_profit"]
        operating_income = gross_profit - sga - rnd
        net_income = operating_income * (1 - inputs["tax_rate"])
        depreciation = prior["ppe"] * inputs["depreciation_to_opening_ppe"]
        capex = revenue * capex_rate
        ar = revenue * inputs["ar_days"] / 365
        inventory = (revenue - gross_profit) * inputs["inventory_days"] / 365
        revenue_change = revenue - prior["revenue"]
        other_assets = prior["other_assets"] + inputs["other_asset_to_revenue_change"] * revenue_change
        other_liabilities = prior["other_liabilities"] + inputs["other_liability_to_revenue_change"] * revenue_change
        ppe = prior["ppe"] + capex - depreciation
        equity = prior["equity"] + net_income - inputs["share_repayments"]
        fcfe = (net_income + depreciation - capex - (ar - prior["ar"])
                - (inventory - prior["inventory"]) - (other_assets - prior["other_assets"])
                + (other_liabilities - prior["other_liabilities"]) - inputs["debt_repayment"])
        cash = prior["cash"] + fcfe - inputs["share_repayments"]
        total_assets = cash + ar + inventory + ppe + other_assets
        total_le = prior["debt"] + other_liabilities + equity
        gap = total_assets - total_le
        cash_passes = cash >= inputs["minimum_cash"]
        current = {"year": year, "revenue": revenue, "gross_profit": gross_profit,
                   "sga": sga, "rnd": rnd, "operating_income": operating_income,
                   "net_income": net_income, "depreciation": depreciation, "capex": capex,
                   "ar": ar, "inventory": inventory, "ppe": ppe,
                   "other_assets": other_assets, "other_liabilities": other_liabilities,
                   "equity": equity, "cash": cash, "fcfe": fcfe,
                   "total_assets": total_assets, "total_le": total_le,
                   "balance_gap": gap, "cash_passes": cash_passes, "debt": prior["debt"]}
        years.append(current)
        if abs(gap) > 0.01 and invalid_reason is None:
            invalid_reason = f"FY{year}E balance gap ${gap:,.1f}m"
        if not cash_passes and invalid_reason is None:
            invalid_reason = f"FY{year}E cash ${cash:,.1f}m below ${inputs['minimum_cash']:,.1f}m floor"
        prior = current

    final = years[-1]
    value = None
    if invalid_reason is None and final["fcfe"] > 0:
        pv_fcfe = sum(item["fcfe"] / ((1 + inputs["cost_of_equity"]) ** period)
                      for period, item in enumerate(years, 1))
        terminal = final["fcfe"] * (1 + inputs["terminal_growth"]) / (inputs["cost_of_equity"] - inputs["terminal_growth"])
        value = (pv_fcfe + terminal / ((1 + inputs["cost_of_equity"]) ** len(years))) / inputs["shares"]
    elif invalid_reason is None:
        invalid_reason = "FY2031E FCFE is non-positive; terminal value is unavailable."
    return {"valid": invalid_reason is None, "reason": invalid_reason, "years": years,
            "final_operating_income": final["operating_income"], "final_fcfe": final["fcfe"],
            "value_per_share": value, "minimum_cash": min(item["cash"] for item in years)}


def run_scenario(driver, case, values):
    """Fresh independent base copy; modify only the named driver."""
    inputs = deepcopy(BASE_INPUTS)
    inputs[DRIVERS[driver]["key"]] = deepcopy(values)
    result = run_linked_model(inputs)
    result.update(driver=driver, case=case, input_values=deepcopy(values))
    return result


def money(value, decimals=1):
    return "N/A" if value is None else f"${value:,.{decimals}f}"


def delta(value, base, decimals=1):
    return "N/A" if value is None or base is None else f"${value - base:+,.{decimals}f}"


def print_trace(result):
    """Statement detail retained for the selected base result."""
    year = result["years"][-1]
    print(f"\nTrace detail: {result['driver']} / {result['case']} - FY{year['year']}E (USD millions)")
    for label, key in [("Revenue", "revenue"), ("Gross profit", "gross_profit"),
                       ("SG&A proxy", "sga"), ("R&D", "rnd"),
                       ("Operating income", "operating_income"), ("Net income", "net_income"),
                       ("Depreciation", "depreciation"), ("Capital spending", "capex"),
                       ("Accounts receivable", "ar"), ("Inventory", "inventory"),
                       ("PP&E", "ppe"), ("Cash", "cash"), ("FCFE", "fcfe"),
                       ("Total assets", "total_assets"), ("Liabilities + equity", "total_le"),
                       ("Balance gap", "balance_gap")]:
        print(f"  {label:<27} {money(year[key])}m")


def print_driver(driver):
    print(f"\n{driver} ({DRIVERS[driver]['unit']})")
    results = [run_scenario(driver, case, DRIVERS[driver][case.lower()]) for case in ("Lower", "Base", "Higher")]
    base = results[1]
    print("Case   Actual FY2027E-FY2031E input values     FY2031E operating profit   FY2031E FCFE   Value/share   Accounting check")
    print("-" * 130)
    for result in results:
        check = "PASS: all five years" if result["valid"] else f"INVALID: {result['reason']}"
        print(f"{result['case']:<7}{values_as_percent(result['input_values']):<42}"
              f"{money(result['final_operating_income']):>17}m ({delta(result['final_operating_income'], base['final_operating_income'])}m) "
              f"{money(result['final_fcfe']):>14}m ({delta(result['final_fcfe'], base['final_fcfe'])}m) "
              f"{money(result['value_per_share'], 2):>11} ({delta(result['value_per_share'], base['value_per_share'], 2)})  {check}")
    for label, key, precision, unit in [("FY2031E operating profit", "final_operating_income", 1, "USD millions"),
                                        ("FY2031E FCFE", "final_fcfe", 1, "USD millions"),
                                        ("Value per share", "value_per_share", 2, "USD per diluted share")]:
        values = [result[key] for result in results if result["valid"] and result[key] is not None]
        span = None if not values else max(values) - min(values)
        print(f"{label} span: {money(span, precision)} {unit}")
    print_trace(base)
    return base


def main():
    print("Lab 11 Microsoft one-at-a-time sensitivity analysis")
    print("Cash-flow label: FCFE. USD millions except value per diluted share.")
    print("Every scenario begins with a fresh independent copy of the base input set.")
    first_base = None
    for driver in DRIVERS:
        base = print_driver(driver)
        if first_base is None:
            first_base = base
    restored = run_scenario("Revenue growth", "Base restored", DRIVERS["Revenue growth"]["base"])
    outputs_match = restored["valid"] and all(abs(first_base[key] - restored[key]) < 0.000001
                                                for key in ("final_operating_income", "final_fcfe", "value_per_share"))
    print("\nBase restoration check")
    print("PASS: restored base matches the first base run." if outputs_match else "INVALID: restored base does not match first base run.")
    print_trace(restored)


if __name__ == "__main__":
    main()
