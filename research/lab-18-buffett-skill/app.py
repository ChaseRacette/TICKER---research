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
      .stApp, [data-testid="stAppViewContainer"] { background: #ffffff; color: #172033; }
      [data-testid="stHeader"] { background: rgba(255, 255, 255, 0.96); }
      [data-testid="stSidebar"] { background: #eef4f8; }
      h1, h2, h3 { color: #12344d !important; font-weight: 800 !important; }
      p, li, label, [data-testid="stCaptionContainer"] { color: #172033 !important; }
      [data-testid="stMetricLabel"] p { color: #334155 !important; font-weight: 700; }
      [data-testid="stMetricValue"] { color: #0f2f44 !important; font-weight: 800; }
      [data-testid="stMetric"] {
        background: #ffffff;
        border: 1px solid #bfd1df;
        border-left: 7px solid #0f6b8a;
        border-radius: 10px;
        padding: 14px;
        box-shadow: 0 2px 8px rgba(23, 63, 95, 0.08);
      }
      [data-testid="stDataFrame"] { border: 1px solid #8ba9bc; border-radius: 8px; }
      .explanation-box { background: #eef7fb; border-left: 6px solid #0f6b8a; color: #172033;
                         border-radius: 6px; padding: 14px 18px; margin: 10px 0 20px; }
    </style>
    """,
    unsafe_allow_html=True,
)
st.title("Buffett 10-K Skill | Business Quality, Not Price")
st.caption("Data from SEC EDGAR; built with AI help, a learning demonstration, not investment advice.")
st.markdown(
    """<div class="explanation-box"><b>What this page does:</b> It uses only the company's
    SEC 10-K facts to calculate revenue, profit, cash flow, ROE, and owner earnings. The code
    calculates the numbers; the memo interprets the business and never gives a price target.</div>""",
    unsafe_allow_html=True,
)

ticker = st.sidebar.text_input("Ticker", "COST").strip().upper()
st.sidebar.caption("Enter a U.S. company ticker, then load its five most recent 10-K fiscal years.")
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
    st.caption("Amounts are USD millions. Higher owner earnings means more cash remains after capital spending.")
    st.line_chart(chart_rows, x="FY end", y=["Owner earnings", "Net income"])

    st.subheader("Five-year 10-K facts")
    st.caption("Each figure is reported in USD millions. The right-most column records the exact XBRL tag used.")
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
    st.caption("PASS means the rule was satisfied in all five rows. NOT KNOWN means the 10-K data did not contain an input, so the program did not estimate it.")
    checks = buffett_checks(rows)
    check_columns = st.columns(3)
    for column, (name, result) in zip(check_columns, checks.items()):
        icon = "PASS" if result == "pass" else "FAIL" if result == "fail" else "NOT KNOWN"
        column.markdown(f"### {icon}")
        column.caption(name.replace("every year", "each year"))
    st.dataframe([{"Check": name, "Result": result} for name, result in checks.items()], hide_index=True)

    path = memo_path(loaded_ticker)
    st.subheader("Buffett memo")
    st.caption("This is a business-quality judgment based only on the printed facts above, not an investment recommendation.")
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
