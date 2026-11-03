"""Streamlit viewer for the Lab 18 SEC 10-K Buffett skill."""
from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st

SKILL_SCRIPTS = Path(__file__).parent / "buffett-10k-skill" / "scripts"
sys.path.insert(0, str(SKILL_SCRIPTS))
from edgar_buffett import (  # noqa: E402
    buffett_checks,
    build_year_rows,
    memo_unprinted_numbers,
)


REPORTS = Path(__file__).parent / "reports"


def display_value(value, percent=False):
    if value is None:
        return "not found" if not percent else "not known"
    return f"{value * 100:.1f}%" if percent else f"{value / 1_000_000:,.0f}"


@st.cache_data(ttl=3600, show_spinner=False)
def load_company(ticker: str):
    return build_year_rows(ticker)


def memo_path(ticker: str) -> Path:
    return REPORTS / f"{ticker.upper()}_buffett_memo.md"


st.set_page_config(page_title="Buffett 10-K Skill", layout="wide")
st.markdown(
    """
    <style>
      .stApp { background: #f7f3ea; }
      h1, h2, h3 { color: #173f5f; font-weight: 800 !important; }
      [data-testid="stMetric"] {
        background: #ffffff;
        border-left: 7px solid #d9822b;
        border-radius: 10px;
        padding: 14px;
        box-shadow: 0 2px 8px rgba(23, 63, 95, 0.12);
      }
      [data-testid="stDataFrame"] { border: 2px solid #173f5f; border-radius: 8px; }
    </style>
    """,
    unsafe_allow_html=True,
)
st.title("Buffett 10-K Skill | Business Quality, Not Price")
st.caption("Data from SEC EDGAR; built with AI help, a learning demonstration, not investment advice.")

ticker = st.sidebar.text_input("Ticker", "COST").strip().upper()
if st.sidebar.button("Load 10-K facts") or "lab18_data" not in st.session_state:
    try:
        st.session_state.lab18_data = (ticker, *load_company(ticker))
    except Exception as error:
        st.error(str(error))

if "lab18_data" in st.session_state:
    loaded_ticker, company, rows = st.session_state.lab18_data
    st.subheader(f"{loaded_ticker} — {company}")
    chart_rows = [{"FY end": row["fiscal_year_end"], "Owner earnings": row["owner_earnings"] / 1_000_000 if row["owner_earnings"] is not None else None,
                   "Net income": row["net_income"] / 1_000_000 if row["net_income"] is not None else None} for row in rows]
    latest = rows[-1] if rows else {}
    summary = st.columns(3)
    summary[0].metric("Latest owner earnings ($ millions)", display_value(latest.get("owner_earnings")))
    summary[1].metric("Latest ROE", display_value(latest.get("roe"), percent=True))
    summary[2].metric("Fiscal year end", latest.get("fiscal_year_end", "not found"))

    st.subheader("Earnings trend")
    st.line_chart(chart_rows, x="FY end", y=["Owner earnings", "Net income"])

    table = []
    for row in rows:
        table.append({
            "FY end": row["fiscal_year_end"], "Revenue": display_value(row["revenue"]),
            "Net income": display_value(row["net_income"]), "Operating cash flow": display_value(row["operating_cash_flow"]),
            "Capital spending": display_value(row["capital_spending"]), "Equity": display_value(row["equity"]),
            "ROE": display_value(row["roe"], percent=True), "Owner earnings": display_value(row["owner_earnings"]),
            "XBRL tags": "; ".join(f"{field}: {tag}" for field, tag in row["tags"].items()),
        })
    st.dataframe(table, width="stretch", hide_index=True)

    st.subheader("Buffett checks computed in code")
    checks = buffett_checks(rows)
    check_columns = st.columns(3)
    for column, (name, result) in zip(check_columns, checks.items()):
        icon = "PASS" if result == "pass" else "FAIL" if result == "fail" else "NOT KNOWN"
        column.markdown(f"### {icon}")
        column.caption(name)
    st.dataframe([{"Check": name, "Result": result} for name, result in checks.items()], hide_index=True)

    path = memo_path(loaded_ticker)
    st.subheader("Buffett memo")
    if path.exists():
        memo = path.read_text(encoding="utf-8")
        st.markdown(memo)
        unprinted = memo_unprinted_numbers(memo, rows)
        if unprinted:
            st.warning("Numbers in the memo not printed by the script: " + ", ".join(unprinted))
        else:
            st.success("Every number in this memo appears in the script output.")
    else:
        st.info(f"No saved memo yet. Save one as reports/{loaded_ticker}_buffett_memo.md after reviewing the script output.")
