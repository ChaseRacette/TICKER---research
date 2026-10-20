"""5-Year FCFF Discounted Cash Flow (DCF) Model
Standard Library implementation adhering to FIN 43900 training convention.
"""

import sys

# ==============================================================================
# EDITABLE INPUTS (in USD millions, except share count in millions and rates)
# ==============================================================================
starting_fcff = 44_229.34                   # FY2026 FCFF (t=0) in $M
growth_rates = [1.0508601451, 0.3322077922, 0.2523583654, 0.2294316842, 0.1656309448]
wacc = 0.08                                 # Assumption: weighted average cost of capital
terminal_growth = 0.035                     # Assumption: long-run terminal growth rate
cash = 76_843.0                             # Cash and short-term investments at June 30, 2026, in $M
debt = 40_294.0                             # Current and long-term debt at June 30, 2026, in $M
shares = 7_427.0                            # Shares outstanding at June 30, 2026, in millions
# ==============================================================================

# =============================================================================
# ADDITIONAL ANALYSIS SETTINGS (edit these without changing the base DCF inputs)
# =============================================================================
sensitivity_wacc_values = [0.09, 0.10, 0.11]
sensitivity_terminal_growth_values = [0.02, 0.03, 0.04]
reverse_target_share_price = 491.65
reverse_shift_lower_bound = -0.05           # -5 percentage points
reverse_shift_upper_bound = 0.10            # +10 percentage points

# Boundary check: Terminal growth must be strictly less than WACC
if terminal_growth >= wacc:
    sys.exit(
        f"Error: Terminal growth rate ({terminal_growth:.4f}) must be strictly less than "
        f"WACC ({wacc:.4f}). At g >= WACC, Gordon Growth is mathematically undefined."
    )

if shares <= 0:
    sys.exit(f"Error: Diluted shares outstanding must be positive, got {shares}.")

# Step 1: Forecast 5 years of explicit FCFF
fcff = []
current_fcff = starting_fcff
for g in growth_rates:
    current_fcff *= (1.0 + g)
    fcff.append(current_fcff)

# Step 2: Discount explicit cash flows back to Year 0
pv_fcff = [cf / ((1.0 + wacc) ** (t + 1)) for t, cf in enumerate(fcff)]
pv_explicit = sum(pv_fcff)

# Step 3: Terminal Value at Year 5 via Gordon Growth Model
# TV_5 = FCFF_6 / (WACC - g) = FCFF_5 * (1 + g) / (WACC - g)
tv_year_5 = fcff[-1] * (1.0 + terminal_growth) / (wacc - terminal_growth)

# Step 4: Present Value of Terminal Value discounted from Year 5 back to Year 0
pv_tv = tv_year_5 / ((1.0 + wacc) ** 5)

# Step 5: Enterprise Value (PV of explicit cash flows + PV of Terminal Value)
enterprise_value = pv_explicit + pv_tv

# Step 6: Enterprise-to-Equity Bridge
equity_value = enterprise_value + cash - debt
value_per_share = equity_value / shares

# Step 7: Terminal Value Concentration
tv_share_of_ev = pv_tv / enterprise_value

# ==============================================================================
# OUTPUT (12 labelled lines formatted to 4 decimal places)
# ==============================================================================
print(f"FCFF Year 1:                                        {fcff[0]:.4f}")
print(f"FCFF Year 2:                                        {fcff[1]:.4f}")
print(f"FCFF Year 3:                                        {fcff[2]:.4f}")
print(f"FCFF Year 4:                                        {fcff[3]:.4f}")
print(f"FCFF Year 5:                                        {fcff[4]:.4f}")
print(f"Present value of explicit FCFF:                     {pv_explicit:.4f}")
print(f"Terminal value at Year 5:                           {tv_year_5:.4f}")
print(f"Present value of terminal value:                    {pv_tv:.4f}")
print(f"Enterprise value:                                   {enterprise_value:.4f}")
print(f"Equity value:                                       {equity_value:.4f}")
print(f"Value per diluted share:                            {value_per_share:.4f}")
print(f"PV of terminal value as share of enterprise value:  {tv_share_of_ev:.4f}")


def calculate_value_per_share(wacc_rate, terminal_growth_rate, explicit_growth_rates):
    """Return the DCF value per diluted share for a supplied assumption set."""
    forecast_fcff = []
    forecast_current_fcff = starting_fcff
    for growth_rate in explicit_growth_rates:
        forecast_current_fcff *= 1.0 + growth_rate
        forecast_fcff.append(forecast_current_fcff)

    forecast_pv_explicit = sum(
        cash_flow / ((1.0 + wacc_rate) ** (period + 1))
        for period, cash_flow in enumerate(forecast_fcff)
    )
    forecast_terminal_value = (
        forecast_fcff[-1] * (1.0 + terminal_growth_rate)
        / (wacc_rate - terminal_growth_rate)
    )
    forecast_pv_terminal_value = forecast_terminal_value / ((1.0 + wacc_rate) ** 5)
    forecast_equity_value = forecast_pv_explicit + forecast_pv_terminal_value + cash - debt
    return forecast_equity_value / shares


# Sensitivity grid: terminal-growth rates are columns and WACC rates are rows.
print("\nSensitivity analysis: value per diluted share")
header = "WACC \\ Terminal Growth | " + " | ".join(
    f"{rate:.2%}" for rate in sensitivity_terminal_growth_values
)
print(header)
print("-" * len(header))

for sensitivity_wacc in sensitivity_wacc_values:
    cells = []
    for sensitivity_terminal_growth in sensitivity_terminal_growth_values:
        if sensitivity_terminal_growth >= sensitivity_wacc:
            cells.append("INVALID")
        else:
            sensitivity_value = calculate_value_per_share(
                sensitivity_wacc, sensitivity_terminal_growth, growth_rates
            )
            cells.append(f"${sensitivity_value:,.2f}")
    print(f"{sensitivity_wacc:.2%}                 | " + " | ".join(cells))


# Reverse DCF: solve by bisection for one uniform shift to all explicit growth rates.
print("\nReverse DCF: uniform shift to all five explicit growth rates")
print(f"Target price: ${reverse_target_share_price:,.2f}")
print(
    "Held fixed: "
    f"starting FCFF=${starting_fcff:,.2f}M; "
    f"base growth rates={growth_rates}; "
    f"WACC={wacc:.2%}; terminal growth={terminal_growth:.2%}; "
    f"cash=${cash:,.2f}M; debt=${debt:,.2f}M; shares={shares:,.2f}M"
)
print(
    f"Search bounds: {reverse_shift_lower_bound:.2%} to "
    f"{reverse_shift_upper_bound:.2%}"
)

if reverse_shift_lower_bound > reverse_shift_upper_bound:
    print("No solution: lower bound exceeds upper bound.")
elif any(rate + reverse_shift_lower_bound <= -1.0 for rate in growth_rates) or any(
    rate + reverse_shift_upper_bound <= -1.0 for rate in growth_rates
):
    print("No solution: the supplied bracket pushes an annual growth rate to -100% or below.")
else:
    def shifted_value_per_share(shift):
        shifted_growth_rates = [rate + shift for rate in growth_rates]
        return calculate_value_per_share(wacc, terminal_growth, shifted_growth_rates)

    lower_value = shifted_value_per_share(reverse_shift_lower_bound)
    upper_value = shifted_value_per_share(reverse_shift_upper_bound)
    lower_difference = lower_value - reverse_target_share_price
    upper_difference = upper_value - reverse_target_share_price

    if lower_difference == 0.0:
        print(f"Solved uniform shift: {reverse_shift_lower_bound:.6%} (exact lower-bound solution)")
    elif upper_difference == 0.0:
        print(f"Solved uniform shift: {reverse_shift_upper_bound:.6%} (exact upper-bound solution)")
    elif lower_difference * upper_difference > 0.0:
        print("No solution in this bracket: target price is not bracketed by the endpoint values.")
        print(f"Value at lower bound: ${lower_value:,.4f}")
        print(f"Value at upper bound: ${upper_value:,.4f}")
    else:
        lower_bound = reverse_shift_lower_bound
        upper_bound = reverse_shift_upper_bound
        solved_shift = None
        for _ in range(200):
            midpoint = (lower_bound + upper_bound) / 2.0
            midpoint_value = shifted_value_per_share(midpoint)
            midpoint_difference = midpoint_value - reverse_target_share_price

            if abs(midpoint_difference) < 0.000001:
                solved_shift = midpoint
                break
            if lower_difference * midpoint_difference < 0.0:
                upper_bound = midpoint
            else:
                lower_bound = midpoint
                lower_difference = midpoint_difference
        else:
            solved_shift = (lower_bound + upper_bound) / 2.0

        solved_value = shifted_value_per_share(solved_shift)
        print(f"Solved uniform shift: {solved_shift:.6%}")
        print(f"Value per diluted share at solved shift: ${solved_value:,.4f}")
