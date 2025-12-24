import streamlit as st
import numpy as np
import plotly.graph_objects as go

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------
st.set_page_config(page_title="A1C Insight Dashboard", layout="wide")

# ---------------------------------------------------
# HEADER
# ---------------------------------------------------
st.title("📊 A1C Insight & Trend Dashboard")
st.caption("Actual vs Projected A1C with Fiber, Protein & Fat Overlay")

# ---------------------------------------------------
# DATA (Prototype)
# ---------------------------------------------------
week_labels = [
    "11/23", "11/30", "12/07", "12/14",
    "12/21", "12/22", "12/23",
    "12/28", "01/04", "01/11", "01/18",
    "01/25", "02/01", "02/08", "02/15", "02/22", "03/01"
]

weeks = np.arange(len(week_labels))

actual_a1c = np.array([
    6.38, 6.33, 6.29, 6.25,
    6.26, 6.24, 6.25,
    6.21, 6.17, 6.12, 6.07,
    6.02, 5.98, 5.94, 5.90, 5.87, 5.84
])

projected_a1c = np.array([
    6.40, 6.25, 6.15, 6.05,
    5.98, 5.96, 5.95,
    5.92, 5.88, 5.85, 5.82,
    5.80, 5.80, 5.80, 5.80, 5.80, 5.80
])

best_case = projected_a1c - 0.08
worst_case = projected_a1c + 0.12

fiber_score = np.array([
    4.5, 5.2, 5.8, 6.6,
    5.9, 6.4, 6.0,
    6.7, 7.0, 7.2, 7.3,
    7.4, 7.5, 7.6, 7.7, 7.8, 7.9
])

protein_intake = np.array([
    65, 72, 78, 82,
    76, 92, 115,
    85, 88, 90, 92,
    94, 95, 96, 97, 98, 99
])

fat_intake = np.array([
    55, 58, 62, 68,
    70, 72, 75,
    74, 76, 78, 80,
    82, 84, 86, 88, 90, 92
])

current_week = 6  # 12/23

# ---------------------------------------------------
# INTERACTIVE PLOTLY CHART (Tooltips enabled)
# ---------------------------------------------------
fig = go.Figure()

fig.add_trace(go.Scatter(
    x=week_labels, y=actual_a1c,
    mode="lines+markers", name="Actual A1C",
    hovertemplate="Week: %{x}<br>Actual A1C: %{y:.2f}%<extra></extra>"
))

fig.add_trace(go.Scatter(
    x=week_labels, y=projected_a1c,
    mode="lines+markers", name="Projected A1C",
    line=dict(dash="dash"),
    hovertemplate="Week: %{x}<br>Projected A1C: %{y:.2f}%<extra></extra>"
))

fig.add_trace(go.Scatter(
    x=week_labels, y=fiber_score,
    mode="lines+markers", name="Fiber Score",
    line=dict(dash="dot"),
    hovertemplate="Week: %{x}<br>Fiber Score: %{y:.1f}/10<extra></extra>"
))

fig.add_trace(go.Scatter(
    x=week_labels, y=protein_intake,
    mode="lines+markers", name="Protein (g/day)",
    line=dict(dash="dashdot"),
    hovertemplate="Week: %{x}<br>Protein: %{y} g/day<extra></extra>"
))

fig.add_trace(go.Scatter(
    x=week_labels, y=fat_intake,
    mode="lines+markers", name="Fat (g/day)",
    hovertemplate="Week: %{x}<br>Fat: %{y} g/day<extra></extra>"
))

# Confidence band (filled)
fig.add_trace(go.Scatter(
    x=week_labels + week_labels[::-1],
    y=worst_case.tolist() + best_case[::-1].tolist(),
    fill="toself",
    name="Confidence Band",
    line=dict(width=0),
    hovertemplate="Week: %{x}<br>Band value: %{y:.2f}%<extra></extra>"
))

# Current week marker
fig.add_vline(
    x=week_labels[current_week],
    line_dash="dot",
    annotation_text=f"Current Week: {week_labels[current_week]}",
    annotation_position="top"
)

fig.update_layout(
    title="Actual vs Projected A1C with Fiber, Protein & Fat Overlay",
    hovermode="x unified",
    xaxis_title="Week",
    yaxis_title="A1C (%)",
    height=600,
    template="plotly_white",
)

st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------
# INSIGHTS
# ---------------------------------------------------
st.markdown("### 🧠 Current Insight")
st.success(
    "Trend shows resilience despite dietary variability. "
    "High protein + fiber moderated improvement rate effectively."
)
st.caption("Insights are trend-based only and not medical advice.")
