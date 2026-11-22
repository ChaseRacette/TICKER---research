"""Racette Investments: personal planning and portfolio-policy dashboard."""
from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import sys

import streamlit as st

PROJECT_DIRECTORY = Path(__file__).parent
sys.path.insert(0, str(PROJECT_DIRECTORY))
from goal_runway import future_value, money, required_monthly_investment  # noqa: E402
from portfolio_engine import (  # noqa: E402
    CPI_ASSUMPTION,
    DRAWDOWN_REVIEW_TRIGGER,
    LIQUIDITY_FLOOR,
    NOMINAL_OBJECTIVE,
    REAL_RETURN_OBJECTIVE,
    SLEEVES,
    TICKERS,
    VOLATILITY_CEILING,
    YahooDataError,
    benchmark_baseline,
    equal_weight_baseline,
    estimate_inputs_from_prices,
    fetch_yahoo_monthly_prices,
    monthly_returns,
    recommended_portfolio,
)


@st.cache_data(ttl=60 * 60 * 6, show_spinner=False)
def live_market_inputs():
    """Get latest completed monthly Yahoo Finance data and calculate policy inputs."""
    dates, prices = fetch_yahoo_monthly_prices()
    estimates, correlations = estimate_inputs_from_prices(prices)
    return dates, prices, estimates, correlations


def verdict_badge(verdict: str) -> str:
    return "PASS" if verdict == "pass" else "FAIL"


def allocation_rail(result):
    """Show portfolio weights as a compact visual rail."""
    if result is None:
        st.warning("No feasible allocation cleared every guardrail.")
        return
    colors = ["#94a3b8", "#5eead4", "#14b8a6", "#0f766e", "#064e3b"]
    segments = "".join(
        f'<div style="width:{result["weights"][sleeve] * 100:.1f}%;background:{color};" '
        f'title="{sleeve}: {result["weights"][sleeve]:.0%}"></div>'
        for sleeve, color in zip(SLEEVES, colors)
        if result["weights"][sleeve] > 0
    )
    st.markdown(f'<div class="allocation-rail">{segments}</div>', unsafe_allow_html=True)
    legend = st.columns(len(SLEEVES))
    for column, sleeve, color in zip(legend, SLEEVES, colors):
        with column:
            st.markdown(f'<span class="legend-dot" style="background:{color}"></span> {sleeve}', unsafe_allow_html=True)
            st.markdown(f'**{result["weights"][sleeve]:.0%}**')


def portfolio_detail(title, result):
    st.markdown(f"### {title}")
    if result is None:
        st.error("No feasible portfolio meets the return objective and every guardrail.")
        return
    expected, risk, verdict = st.columns(3)
    expected.metric("Historical expected return", f"{result['expected_return']:.2%}")
    risk.metric("Estimated volatility", f"{result['volatility']:.2%}")
    verdict.metric("Mandate verdict", verdict_badge(result["verdict"]))
    allocation_rail(result)
    st.markdown("#### Guardrail audit")
    st.dataframe(
        [
            {"Policy rule": label, "Measured": f"{measured:.2%}", "Result": "Pass" if passed else "Fail"}
            for label, measured, passed in result["checks"]
        ],
        column_config={"Policy rule": st.column_config.TextColumn("Policy rule", width="large")},
        hide_index=True,
        width="stretch",
    )


def point_in_time_signal(dates, prices):
    """Return a monitoring-only 10-month ACWI trend reading."""
    closes = prices["ACWI"]
    latest = closes[-1]
    average = sum(closes[-10:]) / 10
    state = "Growth trend intact" if latest >= average else "Caution: trend below average"
    return state, latest, average, dates[-1]


def historical_drawdown_stress(weights, dates, prices):
    """Measure static-target portfolio losses through the available monthly history.

    The calculation rebalances to the supplied target weights each month. It is a
    backward-looking stress observation, not a forecast of the next drawdown.
    """
    returns_by_ticker = monthly_returns(prices)
    monthly_portfolio_returns = [
        sum(weights[sleeve] * returns_by_ticker[TICKERS[sleeve]][index] for sleeve in SLEEVES)
        for index in range(len(dates) - 1)
    ]
    nav = 1.0
    peak = 1.0
    max_drawdown = 0.0
    max_drawdown_date = dates[1]
    for index, monthly_return in enumerate(monthly_portfolio_returns):
        nav *= 1 + monthly_return
        peak = max(peak, nav)
        drawdown = nav / peak - 1
        if drawdown < max_drawdown:
            max_drawdown = drawdown
            max_drawdown_date = dates[index + 1]

    worst_12_month_return = None
    worst_12_month_start = None
    worst_12_month_end = None
    if len(monthly_portfolio_returns) >= 12:
        windows = []
        for start in range(len(monthly_portfolio_returns) - 11):
            cumulative = 1.0
            for monthly_return in monthly_portfolio_returns[start:start + 12]:
                cumulative *= 1 + monthly_return
            windows.append((cumulative - 1, start))
        worst_12_month_return, start = min(windows)
        worst_12_month_start = dates[start + 1]
        worst_12_month_end = dates[start + 12]

    return {
        "max_drawdown": max_drawdown,
        "max_drawdown_date": max_drawdown_date,
        "worst_12_month_return": worst_12_month_return,
        "worst_12_month_start": worst_12_month_start,
        "worst_12_month_end": worst_12_month_end,
    }


def parse_currency(text: str, label: str, minimum: float = 0.0) -> float:
    """Accept dollar signs and commas from a personal-planning input field."""
    cleaned = text.replace("$", "").replace(",", "").strip()
    try:
        amount = float(cleaned)
    except ValueError as error:
        raise ValueError(f"Enter a valid dollar amount for {label}.") from error
    if amount < minimum:
        raise ValueError(f"{label} must be at least {money(minimum)}.")
    return amount


def apply_style():
    st.markdown(
        """<style>
        :root { color-scheme: light; }
        html, body, [data-testid="stAppViewContainer"], .stApp { background: #f8fafc !important; color: #0f172a !important; }
        .block-container { max-width: 1240px; padding-top: 2.5rem; }
        .hero { background: #0f172a; color: #f8fafc; border-radius: 22px; padding: 1.7rem 1.9rem; margin-bottom: 1rem; }
        .hero h1 { margin: 0 0 .35rem; font-size: 2.45rem; }
        .hero p { margin: 0; color: #cbd5e1; font-size: 1.03rem; }
        .eyebrow { color: #5eead4; font-size: .8rem; font-weight: 750; letter-spacing: .11em; text-transform: uppercase; }
        .section-label { color: #0f766e; font-size: .8rem; letter-spacing: .11em; font-weight: 750; margin-top: 1.35rem; }
        [data-testid="stMetric"] { background: #ffffff; border: 1px solid #cbd5e1; border-radius: 14px; padding: .8rem; }
        [data-testid="stMetric"] * { color: #0f172a !important; }
        [data-testid="stWidgetLabel"], [data-testid="stWidgetLabel"] p { color: #334155 !important; font-weight: 650; }
        [data-testid="stForm"] { background: #f1f5f9; border: 1px solid #cbd5e1; border-radius: 16px; padding: 1.1rem; }
        [data-baseweb="input"] > div, [data-baseweb="select"] > div { background: #ffffff !important; border-color: #94a3b8 !important; }
        [data-baseweb="input"] input, [data-baseweb="select"] input, [data-baseweb="select"] div { color: #0f172a !important; -webkit-text-fill-color: #0f172a !important; }
        [data-baseweb="select"] svg { fill: #0f766e !important; }
        [data-testid="stSlider"] [data-baseweb="slider"] > div > div { background-color: #0f766e; }
        .allocation-rail { display:flex; height:30px; overflow:hidden; border-radius:10px; background:#cbd5e1; margin:1.05rem 0 .65rem; }
        .legend-dot { display:inline-block; width:10px; height:10px; border-radius:50%; margin-right:5px; }
        .outcome { background:#ecfdf5; border-left:5px solid #059669; border-radius:10px; padding:1rem 1.1rem; color:#064e3b; }
        .pilot-note { background:#fffbeb; border-left:4px solid #d97706; border-radius:8px; padding:.9rem 1rem; color:#78350f; }
        div[data-testid="stTabs"] button [data-testid="stMarkdownContainer"] p { color:#0f766e; font-weight:700; }
        [data-testid="stDeployButton"], .stDeployButton, button[title="Deploy"], button[aria-label="Deploy"],
        [data-testid="stHeaderActionElements"] { display: none !important; }
        @media (prefers-color-scheme: dark) {
            .stApp { color: #ffffff !important; }
        }
        </style>""",
        unsafe_allow_html=True,
    )


def intake_screen():
    """Collect personal inputs before showing the dashboard."""
    st.markdown(
        """<div class="hero"><div class="eyebrow">Personal investing workspace</div>
        <h1>Racette Investments</h1>
        <p>Start with your plan. Then review the portfolio, guardrails, and stress tests that fit it.</p></div>""",
        unsafe_allow_html=True,
    )
    st.caption("Educational planning tool only; inputs stay in this browser session and are not saved by the app. Not investment, tax, or financial advice.")
    st.markdown('<div class="section-label">Enter your starting point</div>', unsafe_allow_html=True)
    with st.form("personal_plan_input"):
        first, second, third = st.columns(3)
        with first:
            st.text_input("Investable balance", value="$10,000", key="plan_savings")
        with second:
            st.text_input("Cash Emergency Fund", value="$9,000", key="plan_reserve")
            st.caption("Recommended: 6 months of living expenses")
            st.text_input("Planned monthly investment", value="$1,000", key="plan_monthly")
        with third:
            st.text_input("Desired final portfolio value", value="$1,000,000", key="plan_goal")
            st.slider("Years to goal", min_value=1, max_value=40, value=15, key="plan_years")
            st.selectbox("Risk preference", ("Medium-high growth", "Moderate growth", "Conservative"), key="plan_risk")
        submitted = st.form_submit_button("Run my plan", type="primary", use_container_width=True)
    if submitted:
        try:
            st.session_state.submitted_plan = {
                "savings": parse_currency(st.session_state.plan_savings, "investable balance"),
                "reserve": parse_currency(st.session_state.plan_reserve, "cash emergency fund"),
                "monthly": parse_currency(st.session_state.plan_monthly, "planned monthly investment"),
                "goal": parse_currency(st.session_state.plan_goal, "desired final portfolio value"),
                "years": st.session_state.plan_years,
                "risk": st.session_state.plan_risk,
            }
        except ValueError as error:
            st.error(str(error))
            return
        st.session_state.plan_ready = True
        st.rerun()


def plan_values():
    """Read the submitted personal-plan values from the Streamlit session."""
    return st.session_state["submitted_plan"]


def personal_plan_tab(values):
    """Render the personal-planning view using the submitted inputs."""
    years = values["years"]
    projected = future_value(values["savings"], values["monthly"], NOMINAL_OBJECTIVE, years)
    required = required_monthly_investment(values["savings"], values["goal"], NOMINAL_OBJECTIVE, years)
    gap = projected - values["goal"]

    st.markdown('<div class="section-label">Your runway</div>', unsafe_allow_html=True)
    first, second, third, fourth = st.columns(4)
    first.metric(f"Projected value in {years} years", money(projected))
    second.metric("Desired final value", money(values["goal"]))
    third.metric("Ahead / behind goal", money(gap), delta_color="normal" if gap >= 0 else "inverse")
    fourth.metric("Cash Emergency Fund", money(values["reserve"]))
    if gap >= 0:
        st.markdown(f'<div class="outcome"><b>On pace.</b> At the {NOMINAL_OBJECTIVE:.1%} planning objective, your current plan projects {money(gap)} above the selected goal. This is a planning estimate, not a forecast.</div>', unsafe_allow_html=True)
    else:
        additional = max(0.0, required - values["monthly"])
        st.markdown(f'<div class="outcome"><b>Not on pace yet.</b> Reaching the goal at the {NOMINAL_OBJECTIVE:.1%} planning objective would require about {money(required)} per month—{money(additional)} more than the current monthly plan.</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-label">Your path</div>', unsafe_allow_html=True)
    milestones = [
        {"Year": year, "Projected portfolio value": future_value(values["savings"], values["monthly"], NOMINAL_OBJECTIVE, year)}
        for year in range(years + 1)
    ]
    st.line_chart(milestones, x="Year", y="Projected portfolio value", color="#0f766e", height=290)

    horizon_fit = years >= 10
    risk_fit = values["risk"] == "Medium-high growth"
    st.markdown('<div class="section-label">Fit with the Racette policy</div>', unsafe_allow_html=True)
    fit = st.columns(3)
    fit[0].metric("Long-horizon fit", "PASS" if horizon_fit else "REVIEW", f"Input: {years} years")
    fit[1].metric("Medium-high growth preference", "PASS" if risk_fit else "REVIEW", values["risk"])
    fit[2].metric("Cash held outside projection", money(values["reserve"]), "Not invested in the return estimate")
    if not (horizon_fit and risk_fit):
        st.warning("Your inputs do not fully fit the current medium-high-growth policy. Review the goal horizon or risk preference instead of forcing this allocation onto your situation.")


def portfolio_tab():
    """Render the live-data portfolio comparison and policy checks."""
    st.markdown('<div class="section-label">Live market feed</div>', unsafe_allow_html=True)
    left, right = st.columns([4, 1])
    with left:
        st.markdown("**Live source:** Yahoo Finance monthly adjusted-close history · refreshes at most every six hours")
    with right:
        if st.button("Refresh live data", use_container_width=True):
            live_market_inputs.clear()
            st.rerun()
    try:
        dates, prices, estimates, correlations = live_market_inputs()
    except YahooDataError as error:
        st.error(str(error))
        st.info("Reconnect to the internet and use **Refresh live data** to run this view.")
        return

    data_date, window, decision = st.columns(3)
    data_date.metric("Latest completed month", dates[-1])
    window.metric("Estimation window", f"{dates[0]} to {dates[-1]}")
    decision.metric("Committee posture", "PILOT")
    st.dataframe(
        [
            {"Sleeve": sleeve, "Ticker": TICKERS[sleeve], "Historical annual return": f"{estimates[sleeve]['expected_return']:.2%}", "Historical annual volatility": f"{estimates[sleeve]['volatility']:.2%}"}
            for sleeve in SLEEVES
        ],
        column_config={"Sleeve": st.column_config.TextColumn("Sleeve", width="large")},
        hide_index=True,
        width="stretch",
    )
    with st.expander("Data card · what the live feed means"):
        st.markdown("Yahoo Finance supplies monthly adjusted closing prices for SGOV, LQD, ACWI, BIZD, and IGF. The app excludes the partial current month, then uses the most recent 60 completed monthly returns. Returns, volatility, and correlations are calculated locally from those prices. Historical averages are inputs, not forecasts.")

    st.markdown('<div class="section-label">Strategy guardrails</div>', unsafe_allow_html=True)
    objective, volatility, liquidity, horizon = st.columns(4)
    objective.metric("Return objective", f"CPI + {REAL_RETURN_OBJECTIVE:.0%}", f"{NOMINAL_OBJECTIVE:.1%} nominal at {CPI_ASSUMPTION:.1%} CPI")
    volatility.metric("Volatility ceiling", f"{VOLATILITY_CEILING:.0%}")
    liquidity.metric("Liquidity floor", f"{LIQUIDITY_FLOOR:.0%}")
    horizon.metric("Investment horizon", "15 years")
    st.caption("At least 90% must be redeemable within five business days. Alternatives are capped at 15%; private credit is capped at 10%. Annual review only; rebalance after a sleeve drifts more than five percentage points.")

    st.markdown('<div class="section-label">Compare the routes</div>', unsafe_allow_html=True)
    equal = equal_weight_baseline(estimates, correlations)
    benchmark = benchmark_baseline(estimates, correlations)
    recommended = recommended_portfolio(estimates, correlations)
    for column, title, description, portfolio in zip(
        st.columns(3),
        ("Equal start", "Liquid benchmark", "Racette route"),
        ("20% in every sleeve", "70% global equity · 20% bonds · 10% Treasuries", "Maximum historical return after every guardrail"),
        (equal, benchmark, recommended),
    ):
        with column:
            st.markdown(f"**{title}**")
            st.caption(description)
            st.metric("Mandate status", "NO FEASIBLE MIX" if portfolio is None else verdict_badge(portfolio["verdict"]))
            if portfolio is not None:
                st.caption(f"Return {portfolio['expected_return']:.2%} · Volatility {portfolio['volatility']:.2%}")

    equal_tab, benchmark_tab, recommended_tab = st.tabs(["Equal start", "Liquid benchmark", "Racette route"])
    with equal_tab:
        portfolio_detail("Equal-weight baseline", equal)
    with benchmark_tab:
        portfolio_detail("70 / 20 / 10 benchmark", benchmark)
    with recommended_tab:
        portfolio_detail("Constrained pilot allocation", recommended)
        st.markdown('<div class="pilot-note"><b>Pilot decision:</b> test this process before adopting it. It is selected from live historical inputs, but remains subject to the monitoring triggers below.</div>', unsafe_allow_html=True)


def monitoring_tab():
    """Render the monitoring signal, stress test, and stopping condition."""
    try:
        dates, prices, estimates, correlations = live_market_inputs()
    except YahooDataError as error:
        st.error(str(error))
        return
    base_recommendation = recommended_portfolio(estimates, correlations)
    if base_recommendation is None:
        st.error("No base portfolio is available for the historical drawdown stress test.")
        return

    st.markdown('<div class="section-label">Historical drawdown stress</div>', unsafe_allow_html=True)
    drawdown_stress = historical_drawdown_stress(base_recommendation["weights"], dates, prices)
    drawdown_columns = st.columns(3)
    drawdown_columns[0].metric("Maximum historical drawdown", f"{drawdown_stress['max_drawdown']:.2%}")
    drawdown_columns[1].metric(
        "Worst rolling 12-month return",
        f"{drawdown_stress['worst_12_month_return']:.2%}",
        f"{drawdown_stress['worst_12_month_start']} to {drawdown_stress['worst_12_month_end']}",
    )
    trigger_hit = abs(drawdown_stress["max_drawdown"]) >= DRAWDOWN_REVIEW_TRIGGER
    drawdown_columns[2].metric(
        f"{DRAWDOWN_REVIEW_TRIGGER:.0%} review trigger",
        "HIT" if trigger_hit else "NOT HIT",
        f"Worst point: {drawdown_stress['max_drawdown_date']}",
    )
    if trigger_hit:
        st.error("PAUSE AND REVIEW: the historical drawdown crossed the policy trigger.")
    else:
        st.success("The observed historical drawdown stayed inside the 25% pause-and-review trigger. This is history, not a guarantee about future losses.")
    with st.expander("How the historical drawdown stress works"):
        st.markdown(
            "The app applies the recommended target weights to the actual monthly Yahoo Finance returns, rebalanced monthly, across the available five-year window. "
            "It records the largest peak-to-trough portfolio decline and the worst rolling 12-month return. This is more realistic than changing one assumption because it uses the assets' actual co-movements during the observed period; it still does not forecast the next crisis."
        )

    st.markdown('<div class="section-label">Assumption, window, cost, and constraint stress</div>', unsafe_allow_html=True)
    signal, close, moving_average, signal_date = point_in_time_signal(dates, prices)
    signal_column, stress_column = st.columns(2)
    with signal_column:
        st.metric("ACWI 10-month trend", signal)
        st.caption(f"As of {signal_date}: ACWI adjusted close {close:.2f} versus its trailing 10-month average of {moving_average:.2f}.")
        with st.expander("Signal data card"):
            st.markdown("**Purpose:** monitoring only, not an automatic trading rule.  \n**Availability:** calculated from completed ACWI month-end closes available on or before the displayed month.  \n**Limitation:** it can lag reversals and does not predict returns.")
    with stress_column:
        st.markdown("#### Changed-input stress test")
        bond_return_percent = st.slider("Assumed annual return for investment-grade bonds (%)", min_value=-2.0, max_value=8.0, value=4.0, step=0.5, format="%.1f%%")
        stressed_estimates = deepcopy(estimates)
        original = stressed_estimates["Investment-grade bonds"]["expected_return"]
        stressed_estimates["Investment-grade bonds"]["expected_return"] = bond_return_percent / 100
        stressed = recommended_portfolio(stressed_estimates, correlations)
        st.caption(f"Changes LQD's historical input from {original:.2%} to {bond_return_percent:.1f}%; all other live inputs remain unchanged.")
        if stressed is None:
            st.error("STOP: no portfolio meets the objective and every guardrail under this input.")
        else:
            st.metric("Stress-test result", "STILL FEASIBLE")
            st.caption(f"Return {stressed['expected_return']:.2%} · Volatility {stressed['volatility']:.2%}")
    window_column, cost_column, constraint_column = st.columns(3)
    with window_column:
        st.markdown("#### Estimation-window stress")
        window_months = st.select_slider("Completed monthly returns", options=[36, 48, 60], value=36)
        window_estimates, window_correlations = estimate_inputs_from_prices(prices, months=window_months)
        window_recommendation = recommended_portfolio(window_estimates, window_correlations)
        if window_recommendation is None:
            st.error("STOP: no feasible portfolio using this history window.")
        else:
            st.metric("Window result", "STILL FEASIBLE")
            st.caption(f"Return {window_recommendation['expected_return']:.2%} · Volatility {window_recommendation['volatility']:.2%}")
    with cost_column:
        st.markdown("#### Implementation-cost stress")
        annual_cost_percent = st.slider("Annual all-in implementation cost (%)", min_value=0.0, max_value=2.0, value=0.25, step=0.05, format="%.2f%%")
        net_return = base_recommendation["expected_return"] - annual_cost_percent / 100
        cost_passes = net_return >= NOMINAL_OBJECTIVE
        st.metric("Net return after cost", f"{net_return:.2%}")
        if cost_passes:
            st.caption(f"PASS: still above the {NOMINAL_OBJECTIVE:.1%} planning objective after cost.")
        else:
            st.error(f"STOP: net return falls below the {NOMINAL_OBJECTIVE:.1%} planning objective.")
    with constraint_column:
        st.markdown("#### Tighter-constraint stress")
        stress_volatility = st.slider("Tighter volatility ceiling (%)", min_value=10.0, max_value=15.0, value=12.5, step=0.5, format="%.1f%%")
        stress_liquidity = st.slider("Tighter liquidity floor (%)", min_value=90.0, max_value=100.0, value=95.0, step=5.0, format="%.0f%%")
        constrained = recommended_portfolio(
            estimates,
            correlations,
            liquidity_floor=stress_liquidity / 100,
            volatility_ceiling=stress_volatility / 100,
        )
        if constrained is None:
            st.error("STOP: no feasible portfolio under the tighter rules.")
        else:
            st.metric("Constraint result", "STILL FEASIBLE")
            st.caption(f"Return {constrained['expected_return']:.2%} · Volatility {constrained['volatility']:.2%}")
    st.warning(f"**Pause and review:** stop new allocations if no feasible portfolio clears the CPI + 5% objective and every guardrail. Also pause and review liquidity, assumptions, and mandate compliance after a {DRAWDOWN_REVIEW_TRIGGER:.0%} drawdown; do not automatically sell.")


def main():
    st.set_page_config(page_title="Racette Investments", page_icon="R", layout="wide")
    apply_style()
    if not st.session_state.get("plan_ready", False):
        intake_screen()
        return

    values = plan_values()
    top_left, top_right = st.columns([5, 1])
    with top_left:
        st.markdown("<div class='eyebrow'>Personal investing workspace</div><h1>Racette Investments</h1>", unsafe_allow_html=True)
    with top_right:
        if st.button("Edit inputs", use_container_width=True):
            st.session_state.plan_ready = False
            st.rerun()
    st.caption("Educational planning tool only; inputs stay in this browser session and are not saved. Not investment, tax, or financial advice.")

    plan_tab, portfolio_view, monitoring_view = st.tabs(["My Plan", "My Portfolio", "Stress Test & Monitoring"])
    with plan_tab:
        personal_plan_tab(values)
    with portfolio_view:
        portfolio_tab()
    with monitoring_view:
        monitoring_tab()


if __name__ == "__main__":
    main()
