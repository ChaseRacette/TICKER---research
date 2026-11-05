"""Streamlit Lab 19: three investor skills on identical SEC 10-K facts."""
from __future__ import annotations
import sys
from pathlib import Path
import streamlit as st
sys.path.insert(0, str(Path(__file__).parent))
from panel_skill import build_year_rows, display, investor_checks, memo_unprinted_numbers, verdict

REPORTS = Path(__file__).parent / "reports"
@st.cache_data(ttl=3600, show_spinner=False)
def load(ticker): return build_year_rows(ticker)
def memo(ticker, investor): return REPORTS / f"{ticker}_{investor.lower().replace(' ', '_')}_memo.md"
st.set_page_config(page_title="Lab 19 Legend Panel", layout="wide")
st.title("Legend Panel | Three investors, one 10-K record")
st.caption("SEC 10-K facts only • Educational business-quality screen, not investment advice")
ticker = st.sidebar.text_input("Ticker", "COST").strip().upper()
if st.sidebar.button("Load 10-K facts") or "data" not in st.session_state:
    try: st.session_state.data = (ticker, *load(ticker))
    except Exception as error: st.error(str(error))
if "data" in st.session_state:
    symbol, company, rows = st.session_state.data; checks = investor_checks(rows)
    st.subheader(f"{symbol} — {company}")
    st.caption("All three skills use the exact same five fiscal-year 10-K rows below. Missing inputs remain not found; checks become not known.")
    table = [{"FY end": r["fiscal_year_end"], "Net income ($m)": display(r["net_income"]), "Operating cash flow ($m)": display(r["operating_cash_flow"]), "Equity ($m)": display(r["equity"]), "ROE": f"{r['roe'] * 100:.1f}%" if r["roe"] is not None else "not found", "Owner earnings ($m)": display(r["owner_earnings"]), "Current assets ($m)": display(r["assets_current"]), "Current liabilities ($m)": display(r["liabilities_current"]), "Liabilities ($m)": display(r["liabilities"]), "Current ratio": display(r["current_ratio"], True), "Liabilities ÷ equity": display(r["liabilities_to_equity"], True)} for r in rows]
    st.dataframe(table, hide_index=True, width="stretch")

    st.subheader("Five-year operating trends")
    st.caption("USD millions. The charts use the same printed 10-K facts as the panel checks.")
    trends = [{
        "FY end": r["fiscal_year_end"],
        "Revenue": None if r["revenue"] is None else r["revenue"] / 1_000_000,
        "Net income": None if r["net_income"] is None else r["net_income"] / 1_000_000,
        "Operating cash flow": None if r["operating_cash_flow"] is None else r["operating_cash_flow"] / 1_000_000,
    } for r in rows]
    revenue_chart, cash_chart = st.columns(2)
    with revenue_chart:
        st.caption("Growth scale — revenue")
        st.line_chart(trends, x="FY end", y="Revenue", color="#5b8ff9")
    with cash_chart:
        st.caption("Earnings quality — cash flow versus income")
        st.line_chart(trends, x="FY end", y=["Operating cash flow", "Net income"], color=["#27ae60", "#f2994a"])

    st.subheader("Panel table")
    panel = [{"Investor": investor, "Check": name, "Result": result} for investor, cs in checks.items() for name, result in cs.items()]
    st.dataframe(panel, hide_index=True, width="stretch")

    st.subheader("At-a-glance scorecard")
    st.caption("Each investor uses different rules, so each card keeps that investor’s checks together. Green = pass, red = fail, amber = not known.")
    colors = {
        "pass": ("#d8f3dc", "#14532d", "✓"),
        "fail": ("#fde2e2", "#991b1b", "✕"),
        "not known": ("#fef3c7", "#92400e", "?"),
    }
    cards = st.columns(3)
    for column, (investor, criteria) in zip(cards, checks.items()):
        passed = list(criteria.values()).count("pass")
        with column:
            st.markdown(f"### {investor}")
            st.markdown(f"**{verdict(criteria).upper()}**")
            st.caption(f"{passed} of {len(criteria)} checks pass")
            for name, status in criteria.items():
                background, text, icon = colors[status]
                st.markdown(
                    f"<div style='background:{background}; color:{text}; border-radius:8px; "
                    f"padding:9px 10px; margin:7px 0; font-size:0.9rem;'><b>{icon} {status.upper()}</b><br>{name}</div>",
                    unsafe_allow_html=True,
                )
    st.subheader("Memos — every number must be printed above")
    columns = st.columns(3)
    flagged = []
    for col, (investor, cs) in zip(columns, checks.items()):
        with col:
            st.markdown(f"### {investor}")
            path = memo(symbol, investor)
            if path.exists():
                text = path.read_text(encoding="utf-8"); st.markdown(text)
                bad = memo_unprinted_numbers(text, rows)
                if bad: flagged.extend([f"{investor}: {x}" for x in bad])
            else: st.info(f"Save {path.name} after reviewing the printed facts.")
    if flagged: st.warning("Unprinted-number flag: " + "; ".join(flagged))
    else: st.success("Unprinted-number flag: clear across every saved memo.")
