"""Project 2 investment-management application."""
from __future__ import annotations

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
    benchmark_baseline,
    equal_weight_baseline,
    estimate_inputs,
    recommended_portfolio,
)

FROZEN_PRICES = PROJECT_DIRECTORY.parent / "lab-15-portfolio-stability" / "prices.csv"


@st.cache_data(show_spinner=False)
def load_estimates(csv_bytes: bytes | None):
    """Load either the committed baseline file or a reviewer-supplied sensitivity file."""
    if csv_bytes is None:
        return (*estimate_inputs(FROZEN_PRICES), "Fixed baseline: 60 monthly adjusted closes, Oct. 2021–Sep. 2026")
    return (*estimate_inputs(csv_bytes), "Sensitivity mode: uploaded price CSV, latest 60 monthly returns")


def display_portfolio(title, result):
    st.subheader(title)
    if result is None:
        st.error("No feasible portfolio meets CPI + 5% and every policy rule.")
        return
    first, second, third = st.columns(3)
    first.metric("Expected return", f"{result['expected_return']:.2%}")
    second.metric("Estimated volatility", f"{result['volatility']:.2%}")
    third.metric("Policy verdict", result["verdict"].upper())
    st.dataframe(
        {"Sleeve": list(SLEEVES), "Weight": [f"{result['weights'][sleeve]:.0%}" for sleeve in SLEEVES]},
        column_config={"Sleeve": st.column_config.TextColumn("Sleeve", width="large")},
        hide_index=True,
        width="stretch",
    )
    st.dataframe(
        [{"Rule": label, "Measured": f"{measured:.2%}", "Result": "pass" if passed else "fail"}
         for label, measured, passed in result["checks"]],
        column_config={"Rule": st.column_config.TextColumn("Rule", width="large")},
        hide_index=True,
        width="stretch",
    )


def main():
    st.set_page_config(page_title="Project 2 Portfolio Pilot", layout="wide")
    st.title("Project 2 Portfolio Pilot")
    st.caption("AI use: ChatGPT/Codex assisted with code and documentation; the student owns the policy, analysis, and decision. Educational use only; not investment advice.")
    st.info("Committee decision: PILOT the process. The app maximizes expected return only after applying every policy limit.")

    uploaded = st.sidebar.file_uploader("Sensitivity prices CSV", type="csv")
    st.sidebar.caption("Required columns: Date, SGOV, LQD, ACWI, BIZD, IGF. The uploaded file changes sensitivity mode only.")
    try:
        estimates, correlations, source_label = load_estimates(None if uploaded is None else uploaded.getvalue())
    except ValueError as error:
        st.error(f"Could not load sensitivity inputs: {error}")
        return

    st.subheader("Policy and fixed baseline")
    st.caption(source_label)
    objective, volatility, liquidity = st.columns(3)
    objective.metric("Objective", f"CPI + {REAL_RETURN_OBJECTIVE:.0%}", f"{NOMINAL_OBJECTIVE:.1%} nominal using {CPI_ASSUMPTION:.1%} CPI")
    volatility.metric("Volatility ceiling", "15%")
    liquidity.metric("Liquidity floor", "90% within five business days")
    st.dataframe(
        [{"Sleeve": sleeve, "Proxy": TICKERS[sleeve], "Historical annual return": f"{estimates[sleeve]['expected_return']:.2%}", "Historical annual volatility": f"{estimates[sleeve]['volatility']:.2%}"}
         for sleeve in SLEEVES],
        column_config={"Sleeve": st.column_config.TextColumn("Sleeve", width="large")},
        hide_index=True,
        width="stretch",
    )
    st.caption("Historical arithmetic averages from the frozen five-year proxy file are reproducible inputs, not forecasts. BIZD is a public BDC proxy for private credit and is conservatively treated as the less-liquid sleeve; it does not reproduce private-credit fund terms.")

    equal = equal_weight_baseline(estimates, correlations)
    benchmark = benchmark_baseline(estimates, correlations)
    recommended = recommended_portfolio(estimates, correlations)
    st.subheader("Required comparison")
    summary = st.columns(3)
    for column, label, portfolio in ((summary[0], "Equal weight", equal), (summary[1], "70/20/10 benchmark", benchmark), (summary[2], "Recommended", recommended)):
        with column:
            st.metric(label, "NO FEASIBLE MIX" if portfolio is None else portfolio["verdict"].upper())
            if portfolio is not None:
                st.caption(f"Return {portfolio['expected_return']:.2%} | Volatility {portfolio['volatility']:.2%}")

    equal_tab, benchmark_tab, recommended_tab = st.tabs(["Equal-weight details", "Benchmark details", "Recommended details"])
    with equal_tab:
        display_portfolio("Equal-weight baseline", equal)
    with benchmark_tab:
        display_portfolio("70/20/10 benchmark", benchmark)
    with recommended_tab:
        display_portfolio("Constrained recommendation", recommended)


if __name__ == "__main__":
    main()
