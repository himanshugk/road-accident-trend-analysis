import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

st.set_page_config(page_title="State Analysis | MoRTH", page_icon="🗺️", layout="wide")

@st.cache_data
def load_data():
    base_dir = os.path.dirname(os.path.dirname(__file__))
    df_leaders = pd.read_csv(os.path.join(base_dir, "data", "cleaned", "state_leaders.csv"))
    df_sev = pd.read_csv(os.path.join(base_dir, "data", "cleaned", "state_severity_2026.csv"))
    return df_leaders, df_sev

df_leaders, df_sev = load_data()

st.title("🗺️ State-Level Road Accident & Severity Analysis")
st.caption("Empirical breakdown of known 2025 state leaders and statutory 2026 state severity rankings.")

# Note on data availability
st.warning("""
**Data Availability Boundary**: In accordance with statutory disclosures by MoRTH, a complete 36-state 2025 table has not yet been released. 
To preserve analytical integrity, this dashboard displays verified benchmark states and statutory 2026 severity indices, avoiding synthetic data.
""")

col1, col2 = st.columns(2)

with col1:
    st.subheader("1. Known State Leaders (2025 Benchmarks)")
    st.caption("Headline: Tamil Nadu has the highest accident volume; Uttar Pradesh suffers the most road deaths.")
    
    st.dataframe(df_leaders, use_container_width=True)
    
    fig_lead = go.Figure()
    fig_lead.add_trace(go.Bar(
        x=["Tamil Nadu (Accidents)", "Uttar Pradesh (Fatalities)"],
        y=[71387, 27550],
        marker_color=["#0D6EFD", "#DC3545"],
        text=["71,387 crashes<br>(13.9% of India)", "27,550 deaths<br>(15.0% of India)"],
        textposition="auto"
    ))
    fig_lead.update_layout(template="plotly_white", yaxis_title="Count in 2025", height=320)
    st.plotly_chart(fig_lead, use_container_width=True)

with col2:
    st.subheader("2. State Severity Index (1 Jan – 27 Jul 2026)")
    st.caption("Headline: Uttar Pradesh records severe lethality at 55.4 deaths per 100 crashes vs 34.1 national average.")
    
    # Filter out omitted states for the chart
    df_plot = df_sev[df_sev["severity_rate"].notna()].sort_values("severity_rate", ascending=True)
    
    colors = ["#DC3545" if s == "Uttar Pradesh" else ("#0D6EFD" if s == "National Average (India)" else "#6C757D") for s in df_plot["state"]]
    
    fig_sev = go.Figure(go.Bar(
        x=df_plot["severity_rate"],
        y=df_plot["state"],
        orientation='h',
        marker_color=colors,
        text=[f"{v:.1f}" for v in df_plot["severity_rate"]],
        textposition="outside"
    ))
    fig_sev.add_vline(x=34.1, line_dash="dash", line_color="#0D6EFD", annotation_text="National Avg (34.1)", annotation_position="top right")
    fig_sev.update_layout(
        template="plotly_white",
        xaxis=dict(title="Severity (Deaths per 100 Accidents)", range=[0, 65]),
        height=380,
        margin=dict(l=120, r=40, t=20, b=40)
    )
    st.plotly_chart(fig_sev, use_container_width=True)

st.markdown("---")
st.subheader("Statutory 2026 Severity Table & Status Ledger")
st.dataframe(df_sev, use_container_width=True)
st.caption("Data source: MoRTH Lok Sabha reply (30 Jul 2026). Kerala and Bihar were omitted in parliamentary records due to one missing parameter.")
