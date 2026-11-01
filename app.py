"""
Project 10: Road Accident Trend Analysis (MoRTH India)
Main Streamlit Application & Executive Command Center
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

st.set_page_config(
    page_title="India Road Accident Trend Analysis | MoRTH",
    page_icon="🚦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    .metric-card {
        background-color: #FFFFFF;
        border-radius: 10px;
        padding: 20px;
        border-left: 5px solid #0D6EFD;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        margin-bottom: 15px;
    }
    .metric-card-danger {
        background-color: #FFFFFF;
        border-radius: 10px;
        padding: 20px;
        border-left: 5px solid #DC3545;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        margin-bottom: 15px;
    }
    .metric-card-warning {
        background-color: #FFFFFF;
        border-radius: 10px;
        padding: 20px;
        border-left: 5px solid #FFC107;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        margin-bottom: 15px;
    }
    .metric-value {
        font-size: 2.1rem;
        font-weight: 700;
        color: #1A1A1A;
        line-height: 1.2;
    }
    .metric-title {
        font-size: 0.95rem;
        color: #6C757D;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        font-weight: 600;
    }
    .metric-sub {
        font-size: 0.85rem;
        color: #28A745;
        margin-top: 5px;
        font-weight: 500;
    }
    .metric-sub-danger {
        font-size: 0.85rem;
        color: #DC3545;
        margin-top: 5px;
        font-weight: 500;
    }
    .footnote {
        font-size: 0.8rem;
        color: #6C757D;
        font-style: italic;
    }
</style>
""", unsafe_allow_html=True)

# Data Loading with Cache
@st.cache_data
def load_data():
    base_dir = os.path.dirname(__file__)
    data_dir = os.path.join(base_dir, "data", "cleaned")
    df_nat = pd.read_csv(os.path.join(data_dir, "national_series.csv"))
    df_leaders = pd.read_csv(os.path.join(data_dir, "state_leaders.csv"))
    df_sev = pd.read_csv(os.path.join(data_dir, "state_severity_2026.csv"))
    df_causes = pd.read_csv(os.path.join(data_dir, "recorded_causes_2025.csv"))
    return df_nat, df_leaders, df_sev, df_causes

try:
    df_nat, df_leaders, df_sev, df_causes = load_data()
except Exception as e:
    st.error(f"Error loading verified datasets: {e}. Run 'python -m src.pipeline' first.")
    st.stop()

# Header
st.title("🚦 India Road Accident Trend Analysis (2021–2025+)")
st.caption("Official Analytical Monitor — Ministry of Road Transport & Highways (MoRTH) Benchmarks | Lok Sabha Statutory Records")

# Overview Banner
st.info("""
**Mission & Context**: In 2025, India recorded **513,563 road accidents** and **183,382 fatalities**, reaching an unprecedented peak. 
This dashboard presents an auditable, transparent empirical assessment of national accident frequency, state severity disparities, 
root cause enforcement gaps, and evidence-based policy intervention modeling.
""")

# Key Performance Indicators (KPI Cards)
st.subheader("Executive Pulse (2025 National Overview)")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="metric-card-danger">
        <div class="metric-title">Total Accidents (2025)</div>
        <div class="metric-value">5,13,563</div>
        <div class="metric-sub-danger">▲ +5.3% YoY (vs 2024: 4,87,714)</div>
        <div class="footnote">1,407 accidents / day | 59 / hour</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="metric-card-danger">
        <div class="metric-title">Road Fatalities (2025)</div>
        <div class="metric-value">1,83,382</div>
        <div class="metric-sub-danger">▲ +3.5% YoY (vs 2024: 1,77,181)</div>
        <div class="footnote">502 deaths / day | 21 / hour</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="metric-card-warning">
        <div class="metric-title">Accident Severity Rate</div>
        <div class="metric-value">35.7</div>
        <div class="metric-sub">▼ -0.6 pts (Deaths per 100 crashes)</div>
        <div class="footnote">2021: 37.3 | 2024: 36.3</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-title">Injuries (Latest Published)</div>
        <div class="metric-value">4,71,441</div>
        <div class="footnote">Official 2024 final | 2025 pending MoRTH release</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Quick Visual Summary
col_left, col_right = st.columns([3, 2])

with col_left:
    st.markdown("### 📈 5-Year National Trajectory (2021–2025)")
    st.caption("Headline: Accidents surged +24.5% over 5 years, with fatalities climbing +19.1%.")
    
    fig_trend = go.Figure()
    fig_trend.add_trace(go.Scatter(
        x=df_nat["year"], 
        y=df_nat["accidents_lakh"], 
        name="Accidents (Lakh)",
        mode="lines+markers+text",
        text=[f"{v:.2f}L" for v in df_nat["accidents_lakh"]],
        textposition="top left",
        line=dict(color="#0D6EFD", width=3),
        marker=dict(size=8)
    ))
    fig_trend.add_trace(go.Scatter(
        x=df_nat["year"], 
        y=df_nat["fatalities_lakh"], 
        name="Fatalities (Lakh)",
        mode="lines+markers+text",
        text=[f"{v:.2f}L" for v in df_nat["fatalities_lakh"]],
        textposition="bottom right",
        line=dict(color="#DC3545", width=3),
        marker=dict(size=8)
    ))
    fig_trend.update_layout(
        template="plotly_white",
        yaxis_title="Volume in Lakh (100,000)",
        xaxis=dict(tickmode="linear", tick0=2021, dtick=1),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=40, r=40, t=20, b=40),
        height=380
    )
    st.plotly_chart(fig_trend, use_container_width=True)

with col_right:
    st.markdown("### 🗺️ State Leadership Disparities (2025)")
    st.caption("Headline: Tamil Nadu leads in crash count; Uttar Pradesh leads in absolute fatalities.")
    
    st.markdown("""
    - **Frequency Hotspot — Tamil Nadu**:
      - 2025 Crashes: **71,387** (+5.7% YoY)
      - Accounts for **13.9%** of all road accidents in India.
    - **Lethality Hotspot — Uttar Pradesh**:
      - 2025 Fatalities: **27,550** (+14.2% YoY)
      - Accounts for **15.0%** of all road deaths in India (up from 13.6% in 2024).
    """)
    
    # Donut share chart
    fig_donut = go.Figure(data=[go.Pie(
        labels=["Uttar Pradesh (Deaths)", "Rest of India (Deaths)"],
        values=[27550, 183382 - 27550],
        hole=.6,
        marker=dict(colors=["#DC3545", "#E9ECEF"])
    )])
    fig_donut.update_layout(
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=-0.1),
        margin=dict(l=20, r=20, t=20, b=20),
        height=240,
        annotations=[dict(text='15.0%<br>in UP', x=0.5, y=0.5, font_size=18, showarrow=False)]
    )
    st.plotly_chart(fig_donut, use_container_width=True)

st.markdown("---")

# Navigation guide
st.subheader("🧭 Explore Dedicated Analysis Modules")
colA, colB, colC, colD = st.columns(4)

with colA:
    st.markdown("#### 1. National Trends")
    st.write("Detailed 5-year series, severity divergence, daily/hourly rates, and YoY growth.")
    st.markdown("[Go to National Trends →](pages/1_📈_National_Trends)")

with colB:
    st.markdown("#### 2. State Analysis")
    st.write("Cross-state comparison, 2026 severity ranking, and geographical concentration.")
    st.markdown("[Go to State Analysis →](pages/2_🗺️_State_Analysis)")

with colC:
    st.markdown("#### 3. Cause Breakdown")
    st.write("Over-speeding, red light violations, mobile usage, and reporting gap analysis.")
    st.markdown("[Go to Cause Breakdown →](pages/3_⚠️_Cause_Breakdown)")

with colD:
    st.markdown("#### 4. Policy Simulator")
    st.write("Interactive what-if tool modeling lives saved through targeted interventions.")
    st.markdown("[Go to Policy Simulator →](pages/4_🎯_Policy_Simulator)")

# Sidebar Information
with st.sidebar:
    st.image("https://img.icons8.com/color/96/traffic-light.png", width=64)
    st.title("Project 10: MoRTH")
    st.markdown("**Road Accident Trend Analysis**")
    st.markdown("---")
    st.markdown("### 📋 Provenance & Standards")
    st.markdown("- **Authority**: MoRTH Lok Sabha Reply (30 Jul 2026)")
    st.markdown("- **Validation**: 100% Verified against statutory records")
    st.markdown("- **Missing Data Policy**: Explicitly labeled; zero fabrication")
    st.markdown("---")
    st.markdown("### 🛠️ Innovation Highlights")
    st.markdown("1. **Intervention What-If Simulator**")
    st.markdown("2. **Live Data Contract & Quality Auditor**")
