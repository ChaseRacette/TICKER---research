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

from portfolio import (  # noqa: E402
    CORRELATIONS,
    OBJECTIVE_RETURN,
    RESERVE_ELIGIBLE,
    SLEEVES,
    estimate_from_prices,
    lowest_risk_mix,
)


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


def display_result(container, title, result, asset_names):
    """Display one search result or the honest infeasible-result message."""
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


def main():
    st.set_page_config(page_title="Portfolio Stability Decision", layout="wide")
    st.title("Portfolio Stability Decision")
    st.caption("Built with AI help, a learning demonstration, not investment advice.")

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

    current_result = lowest_risk_mix(
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

    current_column, loaded_column = st.columns(2)
    display_result(current_column, "Lowest-risk mix for current inputs", current_result, list(edited_sleeves))
    display_result(loaded_column, "Answer for inputs as loaded", loaded_result, list(loaded_sleeves))

    change = largest_weight_change(current_result, loaded_result, list(edited_sleeves))
    if change is None:
        st.info("Largest weight change is unavailable because at least one search has no feasible mix.")
    else:
        asset, percentage_points = change
        st.metric("Largest weight change", f"{percentage_points:.2f} points", asset)


if __name__ == "__main__":
    main()
