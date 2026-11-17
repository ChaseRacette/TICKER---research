"""A personal goal-planning companion for the Project 2 portfolio pilot."""
from __future__ import annotations

from math import isclose

import streamlit as st


DEFAULT_RETURN = 0.075  # CPI + 5% objective from the Project 2 policy


def future_value(current_savings: float, monthly_investment: float, annual_return: float, years: int) -> float:
    """Calculate nominal future value using monthly compounding and end-month deposits."""
    months = years * 12
    monthly_rate = annual_return / 12
    if isclose(monthly_rate, 0.0):
        return current_savings + monthly_investment * months
    growth = (1 + monthly_rate) ** months
    return current_savings * growth + monthly_investment * ((growth - 1) / monthly_rate)


def required_monthly_investment(current_savings: float, final_goal: float, annual_return: float, years: int) -> float:
    """Return the monthly contribution needed to meet a nominal final-value goal."""
    months = years * 12
    monthly_rate = annual_return / 12
    if isclose(monthly_rate, 0.0):
        return max(0.0, (final_goal - current_savings) / months)
    growth = (1 + monthly_rate) ** months
    amount = (final_goal - current_savings * growth) * monthly_rate / (growth - 1)
    return max(0.0, amount)


def money(amount: float) -> str:
    return f"${amount:,.0f}"


def main():
    st.set_page_config(page_title="Goal Runway Planner", page_icon="↗", layout="wide")
    st.markdown(
        """<style>
        .stApp { background: #f7f7f2; color: #18221c; }
        .block-container { max-width: 1180px; padding-top: 2.5rem; }
        .hero { background: #173b2d; color: #f9fbf8; border-radius: 22px; padding: 1.7rem 1.9rem; margin-bottom: 1rem; }
        .hero h1 { margin: 0 0 .35rem; font-size: 2.35rem; }
        .hero p { margin: 0; color: #d9e9de; font-size: 1.03rem; }
        .step { color: #307454; font-size: .8rem; letter-spacing: .11em; font-weight: 750; margin-top: 1.4rem; }
        [data-testid="stMetric"] { background: #ffffff; border: 1px solid #d7dfd8; border-radius: 14px; padding: .8rem; }
        .outcome { background: #e2f2e7; border-left: 5px solid #2f855a; border-radius: 10px; padding: 1rem 1.1rem; font-size: 1.02rem; }
        </style>""",
        unsafe_allow_html=True,
    )
    st.markdown(
        """<div class="hero"><h1>Goal Runway Planner ↗</h1>
        <p>See whether your saving habit puts a future dollar goal within reach—and what would need to change if it does not.</p></div>""",
        unsafe_allow_html=True,
    )
    st.caption("Educational planning tool only; not investment, tax, or financial advice. Dollar outputs are nominal future dollars and do not guarantee investment results.")

    st.markdown('<div class="step">01 · Start with today</div>', unsafe_allow_html=True)
    left, middle, right = st.columns(3)
    with left:
        current_savings = st.number_input("Current savings / investable balance ($)", min_value=0.0, value=10000.0, step=1000.0, format="%.0f")
    with middle:
        monthly_expenses = st.number_input("Monthly essential expenses ($)", min_value=1.0, value=3000.0, step=100.0, format="%.0f")
    with right:
        monthly_investment = st.number_input("Planned monthly investment ($)", min_value=0.0, value=1000.0, step=100.0, format="%.0f")

    st.markdown('<div class="step">02 · Name the destination</div>', unsafe_allow_html=True)
    goal_column, horizon_column, return_column = st.columns(3)
    with goal_column:
        final_goal = st.number_input("Desired final portfolio value ($)", min_value=0.0, value=1_000_000.0, step=25_000.0, format="%.0f")
    with horizon_column:
        years = st.slider("Years to goal", min_value=1, max_value=40, value=15, step=1)
    with return_column:
        annual_return_percent = st.slider("Assumed annual return (%)", min_value=0.0, max_value=12.0, value=DEFAULT_RETURN * 100, step=0.5, format="%.1f%%")
    annual_return = annual_return_percent / 100
    st.caption("The default return is 7.5%—your Project 2 CPI + 5% nominal planning objective—not a forecast. Change it to see how sensitive the goal is to the assumption.")

    projected = future_value(current_savings, monthly_investment, annual_return, years)
    required = required_monthly_investment(current_savings, final_goal, annual_return, years)
    gap = projected - final_goal
    months_of_expenses = current_savings / monthly_expenses

    st.markdown('<div class="step">03 · Read your runway</div>', unsafe_allow_html=True)
    projection_column, goal_column, gap_column, reserve_column = st.columns(4)
    projection_column.metric(f"Projected value in {years} years", money(projected))
    goal_column.metric("Desired final value", money(final_goal))
    gap_column.metric("Ahead / behind goal", money(gap), delta_color="normal" if gap >= 0 else "inverse")
    reserve_column.metric("Current expenses covered", f"{months_of_expenses:.1f} months")

    if gap >= 0:
        st.markdown(
            f'<div class="outcome"><b>On pace.</b> At the selected assumptions, investing {money(monthly_investment)} per month projects to finish {money(gap)} above the {money(final_goal)} goal.</div>',
            unsafe_allow_html=True,
        )
    else:
        additional = required - monthly_investment
        st.markdown(
            f'<div class="outcome"><b>Not on pace yet.</b> At the selected assumptions, the plan is {money(-gap)} short. Reaching the goal would require about {money(required)} per month—{money(max(0, additional))} more than the current monthly plan.</div>',
            unsafe_allow_html=True,
        )

    st.markdown('<div class="step">04 · See the path, not just the finish line</div>', unsafe_allow_html=True)
    milestones = []
    for year in range(0, years + 1):
        value = future_value(current_savings, monthly_investment, annual_return, year)
        milestones.append({"Year": year, "Projected portfolio value": value})
    st.line_chart(milestones, x="Year", y="Projected portfolio value", color="#307454", height=280)
    st.dataframe(
        [
            {"Planning check": "Current savings as months of expenses", "Value": f"{months_of_expenses:.1f} months"},
            {"Planning check": "Monthly investment as share of monthly expenses", "Value": f"{monthly_investment / monthly_expenses:.0%}"},
            {"Planning check": "Required monthly investment to meet goal", "Value": money(required)},
            {"Planning check": "Assumed annual return", "Value": f"{annual_return:.1%}"},
        ],
        hide_index=True,
        width="stretch",
    )
    with st.expander("How the calculation works"):
        st.markdown(
            "The planner compounds the current balance monthly, then adds the selected monthly investment at the end of each month. "
            "It compares that projected nominal future value with the final-value goal. The required monthly investment reverses the same calculation to solve for the monthly amount needed. "
            "Taxes, fees, inflation, market losses, changing income, and deposits made at different times are not modeled."
        )


if __name__ == "__main__":
    main()
