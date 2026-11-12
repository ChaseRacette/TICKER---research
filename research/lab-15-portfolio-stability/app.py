r"""Lab 15 Streamlit interface for the Lab 14 portfolio engine.

Run from the Course/Work Folder:
    .\.venv\Scripts\python.exe -E -m streamlit run MSFT\ticker-research\research\lab-15-portfolio-stability\app.py
"""

from copy import deepcopy
from io import StringIO
from pathlib import Path
import sys

import streamlit as st


# Import the Lab 14 engine rather than recreating its portfolio math here.
ENGINE_DIRECTORY = Path(__file__).resolve().parents[1] / "lab-14-portfolio"
if str(ENGINE_DIRECTORY) not in sys.path:
    sys.path.insert(0, str(ENGINE_DIRECTORY))
MANDATE_DIRECTORY = Path(__file__).resolve().parents[1] / "lab-13-mandate"
if str(MANDATE_DIRECTORY) not in sys.path:
    sys.path.insert(0, str(MANDATE_DIRECTORY))

from portfolio import (  # noqa: E402
    CORRELATIONS,
    OBJECTIVE_RETURN,
    RESERVE_ELIGIBLE,
    SLEEVES,
    benchmark_weights,
    covariance_matrix,
    equal_weight_weights,
    estimate_from_prices,
    expected_return,
    lowest_risk_mix,
    portfolio_volatility,
    reserve_eligible_weight,
)
from mandate import HOLDINGS, rule_results  # noqa: E402


def load_inputs(uploaded_prices, use_last_36_months):
    """Return current and as-loaded inputs from Meridian or an uploaded price CSV."""
    if uploaded_prices is None:
        sleeves = deepcopy(SLEEVES)
        correlations = deepcopy(CORRELATIONS)
        return sleeves, correlations, deepcopy(sleeves), deepcopy(correlations), "Meridian training inputs"

    csv_text = uploaded_prices.getvalue().decode("utf-8-sig")
    loaded_sleeves, loaded_correlations = estimate_from_prices(StringIO(csv_text))
    if use_last_36_months:
        current_sleeves, current_correlations = estimate_from_prices(
            StringIO(csv_text), last_36_months=True
        )
        label = "Your CSV estimates: last 36 monthly returns"
    else:
        current_sleeves, current_correlations = deepcopy(loaded_sleeves), deepcopy(loaded_correlations)
        label = "Your CSV estimates: all monthly returns"
    return current_sleeves, current_correlations, loaded_sleeves, loaded_correlations, label


def result_for_weights(weights, sleeves, correlations, reserve_eligible):
    """Calculate the three comparable portfolio metrics for any supplied weights."""
    covariances = covariance_matrix(sleeves, correlations)
    return {
        "weights": weights,
        "expected_return": expected_return(weights, sleeves),
        "volatility": portfolio_volatility(weights, covariances),
        "reserve_eligible_weight": reserve_eligible_weight(weights, reserve_eligible),
    }


def mandate_results(weights):
    """Apply Lab 13's checkable rules when all nonzero assets belong to its mandate universe."""
    unknown_assets = [asset for asset, weight in weights.items() if weight and asset not in HOLDINGS]
    if unknown_assets:
        return "not known", [("Mandate asset mapping", ", ".join(unknown_assets), "not known")]

    percent_weights = {holding: weights.get(holding, 0.0) * 100 for holding in HOLDINGS}
    checks = [(label, f"{measured:.1f}%", "pass" if passed else "fail")
              for label, measured, passed in rule_results(percent_weights)]
    return ("pass" if all(status == "pass" for _, _, status in checks) else "fail"), checks


def display_result(container, title, result, asset_names):
    """Display one comparable portfolio and the mandate verdict it earns."""
    with container:
        st.subheader(title)
        if result is None:
            st.warning("No mix meets the objective and reserve rule.")
            return
        st.dataframe(
            {
                "Asset": asset_names,
                "Weight": [f"{result['weights'][asset]:.2%}" for asset in asset_names],
            },
            hide_index=True,
            width="stretch",
        )
        first, second, third = st.columns(3)
        first.metric("Expected return", f"{result['expected_return']:.2%}")
        second.metric("Volatility", f"{result['volatility']:.2%}")
        third.metric("Reserve eligible", f"{result['reserve_eligible_weight']:.2%}")
        verdict, checks = mandate_results(result["weights"])
        if verdict == "pass":
            st.success("Mandate verdict: PASS")
        elif verdict == "fail":
            failed_rules = "; ".join(label for label, _, status in checks if status == "fail")
            st.error(f"Mandate verdict: FAIL — {failed_rules}")
        else:
            st.warning("Mandate verdict: NOT KNOWN — uploaded assets need mapping to the mandate.")
        st.dataframe(
            [{"Mandate rule": label, "Measured": measured, "Result": status} for label, measured, status in checks],
            hide_index=True,
            width="stretch",
        )


def largest_weight_change(current_result, loaded_result, asset_names):
    """Return the largest allocation difference, in percentage points, when both results exist."""
    if current_result is None or loaded_result is None:
        return None
    asset = max(
        asset_names,
        key=lambda name: abs(
            current_result["weights"][name] - loaded_result["weights"][name]
        ),
    )
    change = abs(current_result["weights"][asset] - loaded_result["weights"][asset])
    return asset, change * 100


def dff_signal():
    """Return the verified Lab 17 ALFRED DFF card without a live-data dependency.

    The reference vintage was checked in Lab 17. A DFF level of 3.50% or higher is a
    monitoring trigger for committee review; it never changes portfolio weights automatically.
    """
    dff_value = 3.88
    signal = "high-rate review" if dff_value >= 3.50 else "normal-rate context"
    card = {
        "Source": "https://fred.stlouisfed.org/series/DFF",
        "Series": "DFF — Federal Funds Effective Rate",
        "Units": "Percent, not seasonally adjusted",
        "Frequency": "Daily, 7-day",
        "Release": "H.15 Selected Interest Rates",
        "As known on": "2026-09-30",
        "Latest available observation": "2026-09-29",
        "Latest value": "3.88%",
        "Observed publication lag": "1 calendar day",
        "Same-date revisions": "0",
        "Later current observations excluded": "28",
        "Signal rule": "DFF at or above 3.50%",
        "Signal": signal,
    }
    return signal, dff_value, card


def adverse_return_stress(sleeves, correlations, objective_return, reserve_eligible, minimum_reserve_weight):
    """Stress the global-equity return estimate and rerun the same constrained search.

    The formal stress lowers the global-equity estimate to 6.0%. The process stops when no
    long-only mix can meet both the return objective and reserve rule; it must not substitute
    a portfolio that breaks the mandate just to produce an answer.
    """
    stressed_sleeves = deepcopy(sleeves)
    asset = "Global equity index fund"
    if asset not in stressed_sleeves:
        return None, None, None
    base_return = stressed_sleeves[asset]["expected_return"]
    stressed_return = min(base_return, 0.06)
    stressed_sleeves[asset]["expected_return"] = stressed_return
    result = lowest_risk_mix(
        stressed_sleeves,
        correlations,
        objective_return,
        reserve_eligible,
        minimum_reserve_weight,
    )
    return base_return, stressed_return, result


def main():
    st.set_page_config(page_title="Portfolio Stability Decision", layout="wide")
    st.title("Meridian Foundation Portfolio Decision")
    st.caption("AI use: ChatGPT/Codex assisted with code and documentation; the analyst owns the analysis and decision. Educational use only; not investment advice.")

    st.sidebar.header("Mandate and data")
    objective_return = st.sidebar.number_input(
        "Objective expected return (%)",
        value=OBJECTIVE_RETURN * 100,
        step=0.1,
        format="%.1f",
    ) / 100
    minimum_reserve_weight = st.sidebar.number_input(
        "Minimum reserve-eligible weight (%)",
        value=3.0,
        min_value=0.0,
        max_value=100.0,
        step=0.5,
        format="%.1f",
    ) / 100
    uploaded_prices = st.sidebar.file_uploader(
        "Upload prices.csv", type="csv", help="Date first, oldest first, then one column per ticker."
    )
    use_last_36_months = st.sidebar.toggle("Use only the last 36 monthly returns", value=False)

    try:
        (
            current_sleeves,
            current_correlations,
            loaded_sleeves,
            loaded_correlations,
            source_label,
        ) = load_inputs(uploaded_prices, use_last_36_months)
    except (UnicodeDecodeError, ValueError) as error:
        st.error(f"Could not estimate inputs from this CSV: {error}")
        return

    st.subheader(source_label)
    st.write("Expected returns are historical estimates, not forecasts. Edit an estimate below to test stability.")

    edited_sleeves = deepcopy(current_sleeves)
    reserve_eligible = set()
    for asset in current_sleeves:
        left, right = st.columns([3, 2])
        with left:
            edited_sleeves[asset]["expected_return"] = st.number_input(
                f"Expected return estimate — {asset} (%)",
                value=current_sleeves[asset]["expected_return"] * 100,
                step=0.1,
                format="%.2f",
                key=f"return-{asset}",
            ) / 100
        with right:
            if st.checkbox(
                f"{asset} is reserve eligible",
                value=asset in RESERVE_ELIGIBLE,
                key=f"reserve-{asset}",
            ):
                reserve_eligible.add(asset)

    constrained_result = lowest_risk_mix(
        edited_sleeves,
        current_correlations,
        objective_return,
        reserve_eligible,
        minimum_reserve_weight,
    )
    loaded_result = lowest_risk_mix(
        loaded_sleeves,
        loaded_correlations,
        objective_return,
        reserve_eligible,
        minimum_reserve_weight,
    )

    equal_result = result_for_weights(
        equal_weight_weights(edited_sleeves), edited_sleeves, current_correlations, reserve_eligible
    )
    benchmark_result = result_for_weights(
        benchmark_weights(edited_sleeves), edited_sleeves, current_correlations, reserve_eligible
    )

    st.subheader("Required portfolio comparison")
    st.caption("The constrained mix is the recommended candidate because it is the lowest-volatility mix that meets the entered return objective and reserve rule. Every portfolio is separately checked against the mandate.")
    equal_column, benchmark_column, constrained_column = st.columns(3)
    for column, label, result in (
        (equal_column, "Equal-weight", equal_result),
        (benchmark_column, "Benchmark", benchmark_result),
        (constrained_column, "Recommended", constrained_result),
    ):
        verdict, _ = mandate_results(result["weights"])
        column.metric(label, verdict.upper())
        column.caption(f"Return {result['expected_return']:.2%} | Volatility {result['volatility']:.2%}")

    equal_tab, benchmark_tab, constrained_tab = st.tabs(
        ["Equal-weight details", "Benchmark details", "Recommended portfolio details"]
    )
    equal_column, benchmark_column, constrained_column = equal_tab, benchmark_tab, constrained_tab
    display_result(equal_column, "Equal-weight baseline", equal_result, list(edited_sleeves))
    display_result(benchmark_column, "Benchmark baseline", benchmark_result, list(edited_sleeves))
    display_result(constrained_column, "Constrained portfolio — recommended", constrained_result, list(edited_sleeves))

    st.subheader("Point-in-time DFF signal and data card")
    st.caption(
        "DFF is an external rate-monitoring signal, not a fund price or automatic allocation override. "
        "The verified ALFRED vintage calls for committee review when DFF is at or above 3.50%; it does not change portfolio weights automatically."
    )
    signal, dff_value, data_card = dff_signal()
    signal_column, level_column, vintage_column = st.columns(3)
    signal_column.metric("DFF monitoring signal", signal.upper())
    level_column.metric("Latest DFF known then", f"{dff_value:.2f}%", "2026-09-29")
    vintage_column.metric("ALFRED vintage", "2026-09-30", "one-day observed lag")
    st.dataframe(
        [data_card],
        column_config={"Source": st.column_config.LinkColumn("Source", display_text=r".*/series/(.*)$")},
        hide_index=True,
        width="stretch",
    )

    st.subheader("Formal adverse-return stress run")
    st.caption(
        "Stress design: reduce the global equity expected-return estimate to 6.0%, then rerun the same "
        "long-only constrained search. The return objective and reserve requirement do not change."
    )
    base_return, stressed_return, stress_result = adverse_return_stress(
        edited_sleeves,
        current_correlations,
        objective_return,
        reserve_eligible,
        minimum_reserve_weight,
    )
    if base_return is None:
        st.warning("Stress result not known: the uploaded universe has no mapped global equity index fund.")
    else:
        base_column, stress_column, outcome_column = st.columns(3)
        base_column.metric("Base global-equity estimate", f"{base_return:.2%}")
        stress_column.metric("Stressed global-equity estimate", f"{stressed_return:.2%}")
        if stress_result is None:
            outcome_column.metric("Stress outcome", "STOP")
            st.error(
                "Stop condition met: no long-only portfolio can meet both the entered return objective and "
                "reserve rule after the stress. Do not recommend an allocation; return to the committee for "
                "a revised objective, assumptions, or mandate clarification."
            )
        else:
            outcome_column.metric("Stress outcome", "REVIEW")
            st.warning(
                "A feasible mix remains after the stress. Review its weights, return estimate, and mandate verdict "
                "before retaining the recommendation."
            )
            st.dataframe(
                {"Asset": list(edited_sleeves), "Stressed weight": [f"{stress_result['weights'][asset]:.2%}" for asset in edited_sleeves]},
                hide_index=True,
                width="stretch",
            )

    change = largest_weight_change(constrained_result, loaded_result, list(edited_sleeves))
    if change is None:
        st.info("Largest weight change is unavailable because at least one search has no feasible mix.")
    else:
        asset, percentage_points = change
        st.metric("Largest weight change", f"{percentage_points:.2f} points", asset)


if __name__ == "__main__":
    main()
