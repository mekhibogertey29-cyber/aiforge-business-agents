#!/usr/bin/env python3
"""
Live dashboard – click any agent section to see its task, status, full output and revenue.
"""
import streamlit as st
import json
from pathlib import Path
from datetime import datetime
import pandas as pd
import plotly.express as px
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from config import OUTPUT_DIR, DATA_DIR, BUSINESS_NAME, AGENT_ORDER

st.set_page_config(
    page_title=f"{BUSINESS_NAME} Command Center",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------- Helpers ----------
def load_json(name):
    p = OUTPUT_DIR / name
    if p.exists():
        try:
            return json.loads(p.read_text())
        except:
            return None
    return None

def load_text(name):
    p = OUTPUT_DIR / name
    return p.read_text() if p.exists() else None

def get_status(agent_name):
    p = DATA_DIR / f"{agent_name}_status.json"
    if p.exists():
        return json.loads(p.read_text())
    return {"state": "never_run", "current_task": "—", "last_update": "—"}

def status_color(state):
    return {
        "done": "🟢",
        "working": "🟡",
        "idle": "⚪",
        "error": "🔴",
        "never_run": "⚫"
    }.get(state, "⚪")

# ---------- Sidebar ----------
st.sidebar.title(f"⚡ {BUSINESS_NAME}")
st.sidebar.markdown("**Isolated Multi-Agent Desk**")
st.sidebar.markdown("---")
st.sidebar.markdown("### Agents (click to inspect)")

selected = st.sidebar.radio(
    "Select section",
    ["Overview"] + AGENT_ORDER,
    format_func=lambda x: x if x == "Overview" else f"{status_color(get_status(x)['state'])} {x}"
)

st.sidebar.markdown("---")
if st.sidebar.button("▶ Run Full Chain Now", type="primary"):
    with st.spinner("Running all agents in isolation..."):
        import subprocess
        result = subprocess.run(
            [sys.executable, str(Path(__file__).parent.parent / "orchestrator.py")],
            cwd=str(Path(__file__).parent.parent),
            capture_output=True, text=True
        )
        st.sidebar.code(result.stdout[-1500:] if result.stdout else result.stderr)
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.caption("Each agent owns exactly one job + one file. Zero overlapping writes.")

# ---------- Main Content ----------
if selected == "Overview":
    st.title(f"{BUSINESS_NAME} – Live Command Center")
    st.markdown("Watch every agent, their current task, and real revenue numbers.")

    # KPI row
    sales = load_json("sales.json")
    listing = load_json("listing.json")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("30-Day Revenue", f"${sales['last_30_days']['revenue'] if sales else 0:.2f}")
    with col2:
        st.metric("Units Sold (30d)", sales['last_30_days']['units'] if sales else 0)
    with col3:
        st.metric("Current Price", f"${listing['price'] if listing else 0:.2f}")
    with col4:
        st.metric("Listing Status", listing['status'] if listing else "None")

    # Agent status grid
    st.subheader("All Agents Status")
    cols = st.columns(4)
    for i, agent in enumerate(AGENT_ORDER):
        s = get_status(agent)
        with cols[i % 4]:
            st.markdown(f"**{status_color(s['state'])} {agent}**")
            st.caption(s.get("current_task", "—"))
            st.caption(f"Updated: {s.get('last_update', '—')[:19]}")

    # Revenue chart
    if sales and sales.get("history"):
        st.subheader("Revenue Over Time")
        df = pd.DataFrame(sales["history"])
        fig = px.bar(df, x="date", y="revenue", title="Daily Revenue", labels={"revenue": "USD"})
        st.plotly_chart(fig, use_container_width=True)

    # Quick product card
    if listing:
        st.subheader("Current Live Product")
        st.markdown(f"**{listing['title']}**")
        st.write(listing["description"][:300] + "...")
        st.write(f"**Price:** ${listing['price']} | Platforms: {', '.join(listing['platforms'])}")

else:
    # Individual agent deep view
    agent = selected
    status = get_status(agent)
    st.title(f"{status_color(status['state'])} {agent}")
    st.markdown(f"**Owned Job:** {status.get('owned_job', '—')}")
    st.markdown(f"**Current Task:** `{status.get('current_task', '—')}`")
    st.markdown(f"**Last Update:** {status.get('last_update', '—')}")

    st.markdown("---")

    # Show the exact output this agent owns
    output_map = {
        "01_ideator": ("ideas.json", "json"),
        "02_researcher": ("research.json", "json"),
        "03_designer": ("product_spec.json", "json"),
        "04_copywriter": ("copy.json", "json"),
        "05_lister": ("listing.json", "json"),
        "06_marketer": ("marketing.json", "json"),
        "07_sales_tracker": ("sales.json", "json"),
        "08_optimizer": ("optimizations.md", "text"),
    }

    fname, ftype = output_map.get(agent, (None, None))
    if fname:
        st.subheader(f"Private Output → `{fname}`")
        if ftype == "json":
            data = load_json(fname)
            if data:
                st.json(data)
            else:
                st.info("No output yet. Run the chain.")
        else:
            text = load_text(fname)
            if text:
                st.markdown(text)
            else:
                st.info("No output yet. Run the chain.")

    # Extra for sales agent
    if agent == "07_sales_tracker":
        sales = load_json("sales.json")
        if sales and sales.get("history"):
            st.subheader("Full Sales History")
            df = pd.DataFrame(sales["history"])
            st.dataframe(df, use_container_width=True)
            fig = px.line(df, x="date", y=["units", "revenue"], title="Units & Revenue")
            st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.caption("Isolation contract active • Each agent writes only its own file • Dashboard is read-only observer")