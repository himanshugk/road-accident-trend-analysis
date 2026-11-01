import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

st.set_page_config(page_title="National Trends (2021–2025) | MoRTH", page_icon="📈", layout="wide")

@st.cache_data
def load_data():
    base_dir = os.path.dirname(os.path.dirname(__file__))
    df_nat = pd.read_csv(os.path.join(base_dir, "data", "cleaned", "national_series.csv"))
    return df_nat

df_nat = load_data()

st.title("📈 National Road Accident Trends (2021–2025)")
st.caption("Comprehensive analysis of volume escalation, fatalities, severity rates, and run-rates across India.")

# Interactive Filters
st.sidebar.header("Filter & Metric Selection")
selected_years = st.sidebar.slider("Select Year Range", min_value=2021, max_value=2025, value=(2021, 2025))
metric_choice = st.sidebar.radio("Primary Metric Display", ["Accidents vs Fatalities", "Severity Rate (Deaths / 100 Crashes)", "Run-Rates (Daily & Hourly)"])

df_filtered = df_nat[(df_nat["year"] >= selected_years[0]) & (df_nat["year"] <= selected_years[1])]

# Section 1: Macro Comparison
if metric_choice == "Accidents vs Fatalities":
    st.subheader("1. Accident & Fatality Growth Trajectory")
    st.caption("Headline: Accidents rose by 24.5% while fatalities increased by 19.1% from 2021 to 2025.")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=df_filtered["year"],
            y=df_filtered["accidents"],
            name="Accidents",
            marker_color="#0D6EFD",
            text=[f"{v:,}" for v in df_filtered["accidents"]],
            textposition="auto"
        ))
        fig.add_trace(go.Bar(
            x=df_filtered["year"],
            y=df_filtered["fatalities"],
            name="Fatalities",
            marker_color="#DC3545",
            text=[f"{v:,}" for v in df_filtered["fatalities"]],
            textposition="auto"
        ))
        fig.update_layout(
            barmode="group",
            template="plotly_white",
            yaxis_title="Total Count",
            xaxis=dict(tickmode="linear", dtick=1),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        st.markdown("#### 💡 Analytical Takeaways")
        st.write("""
        - **Post-Pandemic Rebound**: 2022 marked the steepest year-on-year increase (+11.9% accidents, +9.4% deaths) following the resumption of mobility.
        - **Persistent Rise**: While growth slowed in 2023–2024, 2025 saw a renewed spike of **+5.3%** in crashes and **+3.5%** in deaths.
        - **2025 Milestones**: Crosses 5.13 lakh crashes and 1.83 lakh fatalities for the first time in recorded history.
        """)

elif metric_choice == "Severity Rate (Deaths / 100 Crashes)":
    st.subheader("2. Accident Severity Analysis")
    st.caption("Headline: National severity has gently softened from 37.3 (2021) to 35.7 (2025), yet remains globally high.")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        fig_sev = go.Figure()
        fig_sev.add_trace(go.Scatter(
            x=df_filtered["year"],
            y=df_filtered["severity"],
            mode="lines+markers+text",
            text=[f"{v:.1f}" for v in df_filtered["severity"]],
            textposition="top center",
            line=dict(color="#FD7E14", width=3),
            marker=dict(size=10, color="#FD7E14")
        ))
        fig_sev.update_layout(
            template="plotly_white",
            yaxis=dict(title="Severity (Deaths per 100 Accidents)", range=[30, 42]),
            xaxis=dict(tickmode="linear", dtick=1)
        )
        st.plotly_chart(fig_sev, use_container_width=True)
    with col2:
        st.markdown("#### 💡 Understanding Severity")
        st.write("""
        - **What it means**: Accident Severity = `(Fatalities / Total Accidents) * 100`.
        - **Interpretation**: Out of every 100 recorded road collisions in India, approximately 36 people lose their lives.
        - **Contrast**: In most OECD nations, severity rates range between 2 and 6 deaths per 100 reported crashes.
        """)

else:
    st.subheader("3. Daily and Hourly Run-Rate Benchmarks")
    st.caption("Headline: In 2025, every hour witnessed 59 road crashes and 21 lives lost.")
    
    colA, colB = st.columns(2)
    with colA:
        fig_daily = px.bar(
            df_filtered, 
            x="year", 
            y=["accidents_per_day", "deaths_per_day"],
            barmode="group",
            title="Daily Average Run-Rate (Accidents vs Deaths)",
            color_discrete_sequence=["#0D6EFD", "#DC3545"],
            labels={"value": "Count per Day", "variable": "Rate Type"}
        )
        fig_daily.update_layout(template="plotly_white")
        st.plotly_chart(fig_daily, use_container_width=True)
    with colB:
        st.markdown("#### ⏱️ Real-Time Equivalents (2025)")
        st.markdown("""
        - **Every 61 seconds**: 1 road accident occurs somewhere in India.
        - **Every 2.8 minutes**: 1 person dies in a road collision.
        - **Every 24 hours**: 1,407 accidents and 502 fatalities.
        """)

st.markdown("---")
st.subheader("Data Summary Table (Traceable to MoRTH Submissions)")
st.dataframe(
    df_filtered[["year", "accidents", "fatalities", "injuries", "severity", "yoy_accidents_pct", "yoy_fatalities_pct", "source", "derivation_note"]],
    use_container_width=True
)
st.caption("Note: 2025 injuries figure is pending formal MoRTH publication and is deliberately not imputed.")
