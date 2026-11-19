"""Project 2 investment-management application: a live portfolio pilot."""
from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import sys

import streamlit as st

PROJECT_DIRECTORY = Path(__file__).parent
sys.path.insert(0, str(PROJECT_DIRECTORY))
from portfolio_engine import (  # noqa: E402
    CPI_ASSUMPTION,
    NOMINAL_OBJECTIVE,
    REAL_RETURN_OBJECTIVE,
    SLEEVES,
    TICKERS,
    YahooDataError,
    benchmark_baseline,
    equal_weight_baseline,
    estimate_inputs_from_prices,
    fetch_yahoo_monthly_prices,
    recommended_portfolio,
)


@st.cache_data(ttl=60 * 60 * 6, show_spinner=False)
def live_market_inputs():
    """Get the latest complete month-end Yahoo Finance data and calculate inputs."""
    dates, prices = fetch_yahoo_monthly_prices()
    estimates, correlations = estimate_inputs_from_prices(prices)
    return dates, prices, estimates, correlations


def verdict_badge(verdict: str) -> str:
    return "PASS" if verdict == "pass" else "FAIL"


def allocation_rail(result):
    """Show a compact visual allocation rather than a dense first table."""
    if result is None:
        st.warning("No feasible allocation cleared every rule.")
        return
    colors = ["#7dd3fc", "#a7f3d0", "#fcd34d", "#f9a8d4", "#c4b5fd"]
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
    """A monitoring-only 10-month trend signal available at each month end."""
    closes = prices["ACWI"]
    latest = closes[-1]
    average = sum(closes[-10:]) / 10
    state = "Growth trend intact" if latest >= average else "Caution: trend below average"
    return state, latest, average, dates[-1]


def main():
    st.set_page_config(page_title="Northstar Portfolio Pilot", page_icon="✦", layout="wide")
    # The intake is illustrative: this prototype does not use real client data.
    with st.sidebar:
        st.header("Meridian prototype")
        st.caption("Illustrative investor intake - educational use only")
        case_label = st.text_input("Case label", value="Illustrative 15-year growth investor")
        client_horizon = st.slider("Investment horizon (years)", min_value=1, max_value=30, value=15)
        client_risk = st.selectbox("Risk preference", ("Medium-high growth", "Moderate growth", "Conservative"))
        client_liquidity = st.selectbox(
            "Liquidity need",
            ("Standard - policy floor is acceptable", "Higher than the current policy floor"),
        )
        st.caption("This intake tests mandate fit. It does not automatically change the allocation or make a recommendation.")

    horizon_fit = client_horizon == 15
    risk_fit = client_risk == "Medium-high growth"
    liquidity_fit = client_liquidity == "Standard - policy floor is acceptable"


    st.markdown(
        """<style>
        .stApp { background: #08111f; color: #e8eef7; }
        .block-container { max-width: 1320px; padding-top: 2.5rem; }
        [data-testid="stMetric"] { background: #101d31; border: 1px solid #203654; border-radius: 14px; padding: 0.8rem; }
        .hero { padding: 1.65rem 1.8rem; border: 1px solid #265a7b; border-radius: 20px; background: linear-gradient(110deg,#102941,#151d3a); margin-bottom: 1rem; }
        .eyebrow { color: #7dd3fc; font-size: .8rem; font-weight: 700; letter-spacing: .11em; text-transform: uppercase; }
        .hero h1 { margin: .2rem 0 .35rem 0; color: #f8fafc; font-size: 2.45rem; }
        .hero p { color: #cbd5e1; font-size: 1.05rem; margin: 0; }
        .section-label { color: #7dd3fc; font-size: .82rem; font-weight: 750; letter-spacing: .1em; margin-top: 1.65rem; }
        .allocation-rail { display:flex; height:30px; overflow:hidden; border-radius:10px; background:#1e293b; margin: 1.05rem 0 .65rem; }
        .legend-dot { display:inline-block; width:10px; height:10px; border-radius:50%; margin-right:5px; }
        .pilot-note { background:#0f2d2d; border-left:4px solid #5eead4; border-radius:8px; padding: .9rem 1rem; color:#d1fae5; }
        </style>""",
        unsafe_allow_html=True,
    )
    st.markdown(
        """<div class="hero"><div class="eyebrow">Project 2 · Investment-management application</div>
        <h1>Northstar Portfolio Pilot ✦</h1>
        <p>A long-horizon growth portfolio with visible guardrails—not a black-box stock picker.</p></div>""",
        unsafe_allow_html=True,
    )
    st.caption("AI use: ChatGPT/Codex assisted with code and documentation; the student owns the policy, analysis, and decision. Educational use only; not investment advice.")

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
        st.info("This version deliberately uses live Yahoo Finance data. Reconnect to the internet and use **Refresh live data** to run the analysis.")
        return

    st.markdown('<div class="section-label">01 · Live market feed</div>', unsafe_allow_html=True)
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
        st.markdown(
            "Yahoo Finance supplies monthly adjusted closing prices for SGOV, LQD, ACWI, BIZD, and IGF. "
            "The app excludes the partial current month, then uses the most recent 60 completed monthly returns. "
            "Returns, volatility, and correlations are calculated locally from those prices. Historical averages are reproducible inputs, not forecasts. "
            "BIZD is a public business-development-company ticker used only as a limited private-credit proxy; it does not reproduce private-credit fund liquidity, fees, or valuations."
        )

    st.markdown('<div class="section-label">02 - Illustrative mandate fit</div>', unsafe_allow_html=True)
    st.caption(f"Case: {case_label}. The committee view accepts no real client data and does not change the shared policy automatically.")
    fit_columns = st.columns(3)
    fit_columns[0].metric("15-year horizon", "PASS" if horizon_fit else "REVIEW", f"Input: {client_horizon} years")
    fit_columns[1].metric("Medium-high growth preference", "PASS" if risk_fit else "REVIEW", client_risk)
    fit_columns[2].metric("90% liquidity floor", "PASS" if liquidity_fit else "REVIEW", client_liquidity)
    if horizon_fit and risk_fit and liquidity_fit:
        st.success("This illustrative mandate fits the current Northstar policy. Continue to the baseline comparison and stress test before any committee decision.")
    else:
        st.warning("This illustrative mandate does not fully fit the fixed policy. A committee should redesign and validate the mandate rather than force this allocation onto the case.")


    st.markdown('<div class="section-label">02 · Strategy guardrails</div>', unsafe_allow_html=True)
    objective, volatility, liquidity, horizon = st.columns(4)
    objective.metric("Return objective", f"CPI + {REAL_RETURN_OBJECTIVE:.0%}", f"{NOMINAL_OBJECTIVE:.1%} nominal at {CPI_ASSUMPTION:.1%} CPI")
    volatility.metric("Volatility ceiling", "15%")
    liquidity.metric("Liquidity floor", "90%")
    horizon.metric("Investment horizon", "15 years")
    st.caption("At least 90% must be redeemable within five business days. Alternatives are capped at 15%; private credit is capped at 10%. Annual review only; rebalance after a sleeve drifts more than five percentage points.")

    st.markdown('<div class="section-label">03 · Compare the routes</div>', unsafe_allow_html=True)
    equal = equal_weight_baseline(estimates, correlations)
    benchmark = benchmark_baseline(estimates, correlations)
    recommended = recommended_portfolio(estimates, correlations)
    for column, title, description, portfolio in zip(
        st.columns(3),
        ("Equal start", "Liquid benchmark", "Northstar route"),
        ("20% in every sleeve", "70% global equity · 20% bonds · 10% Treasuries", "Maximum historical return after every guardrail"),
        (equal, benchmark, recommended),
    ):
        with column:
            st.markdown(f"**{title}**")
            st.caption(description)
            if portfolio is None:
                st.metric("Mandate status", "NO FEASIBLE MIX")
            else:
                st.metric("Mandate status", verdict_badge(portfolio["verdict"]))
                st.caption(f"Return {portfolio['expected_return']:.2%} · Volatility {portfolio['volatility']:.2%}")

    equal_tab, benchmark_tab, recommended_tab = st.tabs(["Equal start", "Liquid benchmark", "Northstar route"])
    with equal_tab:
        portfolio_detail("Equal-weight baseline", equal)
    with benchmark_tab:
        portfolio_detail("70 / 20 / 10 benchmark", benchmark)
    with recommended_tab:
        portfolio_detail("Constrained pilot allocation", recommended)
        st.markdown('<div class="pilot-note"><b>Pilot decision:</b> test this allocation process before adopting it. It is selected from live historical inputs, but remains subject to the monitoring triggers below.</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-label">04 · Monitor, challenge, decide</div>', unsafe_allow_html=True)
    signal, close, moving_average, signal_date = point_in_time_signal(dates, prices)
    signal_column, stress_column = st.columns(2)
    with signal_column:
        st.markdown("#### Point-in-time monitor")
        st.metric("ACWI 10-month trend", signal)
        st.caption(f"As of {signal_date}: ACWI adjusted close {close:.2f} versus its trailing 10-month average of {moving_average:.2f}.")
        with st.expander("Signal data card"):
            st.markdown(
                "**Purpose:** a monitoring signal, not an automatic trading rule.  \n"
                "**Availability:** calculated only from ACWI month-end closes available on or before the displayed month.  \n"
                "**Method:** latest completed month-end adjusted close ÷ average of the latest ten completed month-end adjusted closes.  \n"
                "**Use:** a caution reading triggers a committee discussion of assumptions; it does not change weights by itself.  \n"
                "**Limitation:** the signal can lag reversals and does not predict returns."
            )
    with stress_column:
        st.markdown("#### Changed-input stress test")
        bond_return_percent = st.slider(
            "Assumed annual return for investment-grade bonds (%)",
            min_value=-2.0,
            max_value=8.0,
            value=4.0,
            step=0.5,
            format="%.1f%%",
        )
        bond_return = bond_return_percent / 100
        stressed_estimates = deepcopy(estimates)
        original_bond_return = stressed_estimates["Investment-grade bonds"]["expected_return"]
        stressed_estimates["Investment-grade bonds"]["expected_return"] = bond_return
        stressed_recommendation = recommended_portfolio(stressed_estimates, correlations)
        st.caption(f"Changes LQD's historical input from {original_bond_return:.2%} to {bond_return:.1%}; all other live inputs remain unchanged.")
        if stressed_recommendation is None:
            st.error("STOP: no portfolio meets the objective and all guardrails under this input.")
        else:
            st.metric("Stress-test result", "STILL FEASIBLE")
            st.caption(f"Return {stressed_recommendation['expected_return']:.2%} · Volatility {stressed_recommendation['volatility']:.2%}")
    st.warning("**Pause and review:** stop new allocations if no feasible portfolio clears the CPI + 5% objective and every guardrail. Also pause and review liquidity, assumptions, and mandate compliance after a 25% drawdown; do not automatically sell.")


if __name__ == "__main__":
    main()
