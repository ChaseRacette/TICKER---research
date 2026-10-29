r"""Lab 17 — FRED and ALFRED point-in-time rates app.

Run from the Course/Work Folder:
    .\.venv\Scripts\python.exe -E -m streamlit run MSFT\ticker-research\research\lab-17-fred-asof\asof_app.py
"""

import csv
from datetime import date
from io import StringIO
import re
from urllib.parse import urlencode
from urllib.request import Request, urlopen

import streamlit as st


SERIES_NAMES = {
    "BAA": "Moody's Baa corporate bond yield",
    "FEDFUNDS": "Federal funds rate",
    "DGS10": "10-year Treasury yield",
    "MORTGAGE30US": "30-year mortgage rate",
}
FRED_CSV_URL = "https://fred.stlouisfed.org/graph/fredgraph.csv"
ALFRED_CSV_URL = "https://alfred.stlouisfed.org/graph/alfredgraph.csv"


def validate_series_id(series_id):
    """Reject malformed IDs before they become part of a download URL."""
    cleaned = series_id.strip().upper()
    if not cleaned:
        return ""
    if not re.fullmatch(r"[A-Z0-9_.-]+", cleaned):
        raise ValueError("Series IDs may contain only letters, numbers, underscores, periods, and hyphens.")
    return cleaned


def parse_fred_csv(csv_text, series_id):
    """Return date-to-value observations, ignoring FRED's '.' missing-value marker."""
    reader = csv.DictReader(StringIO(csv_text))
    if not reader.fieldnames or "observation_date" not in reader.fieldnames:
        raise ValueError(f"FRED did not return usable CSV data for {series_id}.")

    value_columns = [column for column in reader.fieldnames if column != "observation_date"]
    if len(value_columns) != 1:
        raise ValueError(f"FRED returned an unexpected CSV layout for {series_id}.")

    observations = {}
    value_column = value_columns[0]
    for row in reader:
        observation_date = row["observation_date"]
        value = row[value_column]
        if value in ("", ".", None):
            continue
        try:
            observations[date.fromisoformat(observation_date)] = float(value)
        except ValueError as error:
            raise ValueError(f"FRED returned an invalid observation for {series_id}.") from error
    if not observations:
        raise ValueError(f"FRED returned no numeric observations for {series_id}.")
    return observations


def download_csv(url, parameters):
    """Download one public FRED-style CSV without an API key."""
    request = Request(
        f"{url}?{urlencode(parameters)}",
        headers={"User-Agent": "Mozilla/5.0"},
    )
    with urlopen(request, timeout=30) as response:
        return response.read().decode("utf-8-sig")


@st.cache_data(show_spinner=False, ttl=3600)
def download_today_values(series_id):
    """Download a series as FRED displays it today."""
    csv_text = download_csv(FRED_CSV_URL, {"id": series_id})
    return parse_fred_csv(csv_text, series_id)


@st.cache_data(show_spinner=False, ttl=3600)
def download_vintage_values(series_id, vintage_date):
    """Download a series as ALFRED displayed it on a specified vintage date."""
    csv_text = download_csv(
        ALFRED_CSV_URL,
        {"id": series_id, "vintage_date": vintage_date},
    )
    return parse_fred_csv(csv_text, series_id)


def last_observation(observations):
    """Return the latest measurement date and value in a dictionary of observations."""
    latest_date = max(observations)
    return latest_date, observations[latest_date]


def format_observation_value(value):
    """Display integers without decimals and other observations to two decimal places."""
    if value.is_integer():
        return f"{value:,.0f}"
    return f"{value:,.2f}"


def comparison_row(series_id, vintage_values, today_values):
    """Calculate the point-in-time versus current-data counts for one series."""
    vintage_date, vintage_value = last_observation(vintage_values)
    today_date, today_value = last_observation(today_values)
    values_after_then = sum(
        observation_date > vintage_date for observation_date in today_values
    )
    revised_values = sum(
        observation_date in today_values and today_values[observation_date] != value
        for observation_date, value in vintage_values.items()
    )
    return {
        "Series ID": f"https://fred.stlouisfed.org/series/{series_id}",
        "Known then: last measured": vintage_date.isoformat(),
        "Known then: value": format_observation_value(vintage_value),
        "Today: last measured": today_date.isoformat(),
        "Today: value": format_observation_value(today_value),
        "Today's values after then": values_after_then,
        "Same-date values revised": revised_values,
    }


def render_chart(series_id, observations, start_date, vintage_values, as_known_on):
    """Render one today's-data line chart and state the latest value known on the vintage date."""
    chart_data = [
        {"Date": observation_date.isoformat(), "Value": value}
        for observation_date, value in sorted(observations.items())
        if observation_date >= start_date
    ]
    st.subheader(f"{series_id} — {SERIES_NAMES.get(series_id, 'Custom FRED series')}")
    if not chart_data:
        st.info(f"No current {series_id} observations are available on or after {start_date}.")
    else:
        st.vega_lite_chart(
            chart_data,
            {
                "mark": {"type": "line", "tooltip": True},
                "encoding": {
                    "x": {"field": "Date", "type": "temporal", "title": "Observation date"},
                    "y": {"field": "Value", "type": "quantitative", "title": "Value"},
                    "tooltip": [
                        {"field": "Date", "type": "temporal"},
                        {"field": "Value", "type": "quantitative"},
                    ],
                },
            },
            width="stretch",
        )
    known_date, known_value = last_observation(vintage_values)
    st.caption(
        f"Last observation known on {as_known_on}: {known_date.isoformat()} = "
        f"{format_observation_value(known_value)}"
    )


def render_combined_chart(series_observations, start_date):
    """Overlay each series after rebasing its first displayed observation to 100."""
    chart_data = []
    for series_id, observations in series_observations.items():
        displayed_observations = [
            (observation_date, value)
            for observation_date, value in sorted(observations.items())
            if observation_date >= start_date
        ]
        if not displayed_observations or displayed_observations[0][1] == 0:
            continue
        base_value = displayed_observations[0][1]
        chart_data.extend(
            {
                "Date": observation_date.isoformat(),
                "Series": series_id,
                "Indexed value": value / base_value * 100,
            }
            for observation_date, value in displayed_observations
        )

    if len(series_observations) < 2 or not chart_data:
        return
    st.subheader("Combined comparison — rebased to 100")
    st.caption(
        "Each series begins at 100 on its first available observation on or after the start date. "
        "This makes relative co-movement visible; it is not a statistical correlation calculation."
    )
    st.vega_lite_chart(
        chart_data,
        {
            "mark": {"type": "line", "tooltip": True},
            "encoding": {
                "x": {"field": "Date", "type": "temporal", "title": "Observation date"},
                "y": {"field": "Indexed value", "type": "quantitative", "title": "Index (start = 100)"},
                "color": {"field": "Series", "type": "nominal", "title": "Series"},
                "tooltip": [
                    {"field": "Date", "type": "temporal"},
                    {"field": "Series", "type": "nominal"},
                    {"field": "Indexed value", "type": "quantitative", "format": ".2f"},
                ],
            },
        },
        width="stretch",
    )


def main():
    st.set_page_config(page_title="FRED Rates As-Of", layout="wide")
    st.title("FRED Rates As-Of")
    st.caption(
        "Data from FRED and ALFRED, Federal Reserve Bank of St. Louis, downloaded today; "
        "built with AI help, a learning demonstration, not investment advice."
    )

    st.sidebar.header("Series and dates")
    selected_series = st.sidebar.multiselect(
        "FRED series",
        options=list(SERIES_NAMES),
        default=list(SERIES_NAMES),
        format_func=lambda series_id: f"{series_id} — {SERIES_NAMES[series_id]}",
    )
    additional_series = st.sidebar.text_input("Add another FRED series ID", placeholder="Example: DFF")
    try:
        additional_series = validate_series_id(additional_series)
    except ValueError as error:
        st.sidebar.error(str(error))
        additional_series = ""
    if additional_series and additional_series not in selected_series:
        selected_series.append(additional_series)

    start_date = st.sidebar.date_input("Start date", value=date(2020, 1, 1))
    as_known_on = st.sidebar.date_input("As known on", value=date.today())

    if not selected_series:
        st.info("Select at least one FRED series to begin.")
        return

    table_rows = []
    current_observations = {}
    for series_id in selected_series:
        try:
            today_values = download_today_values(series_id)
            vintage_values = download_vintage_values(series_id, as_known_on.isoformat())
            render_chart(series_id, today_values, start_date, vintage_values, as_known_on)
            current_observations[series_id] = today_values
            table_rows.append(comparison_row(series_id, vintage_values, today_values))
        except Exception as error:  # Keep the other requested series usable after one bad ID.
            st.error(f"{series_id}: unable to download or read this FRED series ({error}).")

    render_combined_chart(current_observations, start_date)

    if table_rows:
        st.subheader("As-of comparison")
        st.dataframe(
            table_rows,
            hide_index=True,
            width="stretch",
            column_config={
                "Series ID": st.column_config.LinkColumn(
                    "Series ID",
                    display_text=r".*/series/(.*)$",
                ),
            },
        )


if __name__ == "__main__":
    main()
