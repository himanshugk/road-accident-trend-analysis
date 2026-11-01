import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

st.set_page_config(page_title="Cause Breakdown | MoRTH", page_icon="⚠️", layout="wide")

@st.cache_data
def load_data():
    base_dir = os.path.dirname(os.path.dirname(__file__))
    df_causes = pd.read_csv(os.path.join(base_dir, "data", "cleaned", "recorded_causes_2025.csv"))
    return df_causes

df_causes = load_data()

st.title("⚠️ Contributing Causes & Enforcement Gaps (2025)")
st.caption("Empirical breakdown of recorded traffic rule violations and systemic documentation gaps in FIRs.")

st.info("""
**Data Integrity Alert**: Official MoRTH statistics reflect minimum recorded violations at the time of police First Information Report (FIR) filing. 
Most road accidents occur without a codified violation tag.
""")

col1, col2 = st.columns([3, 2])

with col1:
    st.subheader("1. Recorded Causes vs Unspecified / Other Crashes")
    st.caption("Headline: Over 83% of accidents lack a specific recorded violation in preliminary reports.")
    
    fig_pie = go.Figure(data=[go.Pie(
        labels=df_causes["cause"],
        values=df_causes["accidents_count"],
        hole=.45,
        marker=dict(colors=["#DC3545", "#FD7E14", "#FFC107", "#20C997", "#E9ECEF"])
    )])
    fig_pie.update_layout(
        template="plotly_white",
        legend=dict(orientation="h", yanchor="bottom", y=-0.2),
        height=380
    )
    st.plotly_chart(fig_pie, use_container_width=True)

with col2:
    st.subheader("2. Zoom into Recorded Violations (86,625 Total)")
    st.caption("Headline: Over-speeding represents 94.8% of all specifically tagged traffic violations.")
    
    df_violations = df_causes[df_causes["cause"] != "No traffic violation recorded / Unspecified / Other"].copy()
    
    fig_bar = px.bar(
        df_violations,
        x="accidents_count",
        y="cause",
        orientation="h",
        text="accidents_count",
        color="cause",
        color_discrete_sequence=["#DC3545", "#FD7E14", "#FFC107", "#20C997"]
    )
    fig_bar.update_layout(
        template="plotly_white",
        showlegend=False,
        xaxis_title="Recorded Accident Count",
        yaxis_title="",
        height=380
    )
    st.plotly_chart(fig_bar, use_container_width=True)

st.markdown("---")
st.subheader("Violation Breakdown Table & Statutory Citations")
st.dataframe(df_causes, use_container_width=True)

st.markdown("""
### 🔍 Analytical Implications
1. **The Over-Speeding Crisis**: With 82,124 confirmed accidents attributed directly to excessive speed, high vehicle velocities remain the single deadliest risk factor on National and State Highways.
2. **Under-Reporting of In-Cabin Distraction**: Mobile phone usage accounts for only 136 recorded crashes (0.03%). Transport research indicates this is heavily under-documented due to evidentiary difficulties during on-scene investigation.
3. **Institutional Recommendation**: Upgrading from paper FIRs to integrated e-DAR (Electronic Detailed Accident Report) systems is vital to eliminate the 83.1% 'unspecified' documentation deficit.
""")
