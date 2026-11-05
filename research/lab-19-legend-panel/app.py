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
    st.subheader("Panel table")
    panel = [{"Investor": investor, "Check": name, "Result": result} for investor, cs in checks.items() for name, result in cs.items()]
    st.dataframe(panel, hide_index=True, width="stretch")
    verdicts = st.columns(3)
    for col, (investor, cs) in zip(verdicts, checks.items()): col.metric(investor, verdict(cs).upper(), f"{list(cs.values()).count('pass')} of {len(cs)} checks pass")
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
