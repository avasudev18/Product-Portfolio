import streamlit as st
import numpy as np
import plotly.graph_objects as go

# ─────────────────────────────────────────
# Page config (must run first)
# ─────────────────────────────────────────
st.set_page_config(page_title="A1C Insight Dashboard", layout="wide")

st.title("A1C Insight & Trend Dashboard")
st.caption("Actual vs Projected A1C with Fiber, Protein & Fat Overlay")

# ─────────────────────────────────────────
# Data definitions (sample portfolio prototype)
# ─────────────────────────────────────────
weeks = np.arange(17)

week_labels = [
    "11/23", "11/30", "12/07", "12/14",
    "12/21", "12/22", "12/23",
    "12/28", "01/04", "01/11", "01/18",
    "01/25", "02/01", "02/08", "02/15",
    "02/22", "03/01"
]

actual_a1c = np.array([
    6.38, 6.33, 6.29, 6.25,
    6.26, 6.24, 6.25,
    6.21, 6.17, 6.12, 6.07,
    6.02, 5.98, 5.94, 5.90,
    5.87, 5.84
])

projected_a1c = np.array([
    6.40, 6.25, 6.15, 6.05,
    5.98, 5.96, 5.95,
    5.92, 5.88, 5.85, 5.82,
    5.80, 5.80, 5.80, 5.80,
    5.80, 5.80
])

fiber_score = np.array([
    4.5, 5.2, 5.8, 6.6,
    5.9, 6.4, 6.0,
    6.7, 7.0, 7.2, 7.3,
    7.4, 7.5, 7.6, 7.7,
    7.8, 7.9
])

protein_intake = np.array([
    65, 72, 78, 82,
    76, 92, 115,
    85, 88, 90, 92,
    94, 95, 96, 97,
    98, 99
])

fat_intake = np.array([
    55, 58, 62, 68,
    70, 72, 75,
    74, 76, 78, 80,
    82, 84, 86, 88,
    90, 92
])

best_case = projected_a1c - 0.08
worst_case = projected_a1c + 0.12
current_week = 6

# ─────────────────────────────────────────
# Interactive plot with tooltips
# ─────────────────────────────────────────
fig = go.Figure()

x = weeks  # numeric axis

fig.add_trace(go.Scatter(
    x=x, y=actual_a1c,
    mode="lines+markers",
    name="Actual A1C",
    hovertemplate="A1C: %{y:.2f}% (Week %{x})<extra></extra>"
))

fig.add_trace(go.Scatter(
    x=x, y=projected_a1c,
    mode="lines",
    name="Projected A1C",
    line=dict(dash="dash"),
    hovertemplate="Projected: %{y:.2f}%<extra></extra>"
))

# Confidence band
fig.add_trace(go.Scatter(
    x=np.concatenate([x, x[::-1]]),
    y=np.concatenate([worst_case, best_case[::-1]]),
    fill="toself",
    name="Confidence Band",
    line=dict(width=0),
    hovertemplate="Band limit: %{y:.2f}%<extra></extra>"
))

# Overlays
fig.add_trace(go.Scatter(
    x=x, y=fiber_score,
    name="Fiber Score",
    yaxis="y2",
    hovertemplate="Fiber: %{y:.1f}/10<extra></extra>"
))

fig.add_trace(go.Scatter(
    x=x, y=protein_intake,
    name="Protein (g/day)",
    yaxis="y3",
    hovertemplate="Protein: %{y} g/day<extra></extra>"
))

fig.add_trace(go.Scatter(
    x=x, y=fat_intake,
    name="Fat (g/day)",
    yaxis="y4",
    hovertemplate="Fat: %{y} g/day<extra></extra>"
))

# Current week indicator
fig.add_vline(
    x=current_week,
    line_dash="dot",
    annotation_text=f"Current Week (Week {current_week})",
    annotation_position="top"
)

# Layout
fig.update_layout(
    hovermode="x unified",
    xaxis=dict(title="Week", tickvals=weeks, ticktext=week_labels),
    yaxis=dict(title="A1C (%)"),
    yaxis2=dict(title="Fiber Score", overlaying="y", side="right"),
    yaxis3=dict(title="Protein (g/day)", overlaying="y", side="right", position=0.94),
    yaxis4=dict(title="Fat (g/day)", overlaying="y", side="right", position=1.0),
    height=600,
    margin=dict(r=120)
)

st.plotly_chart(fig, width="stretch")

# ─────────────────────────────────────────
# Insight panel (non-medical guidance only)
# ─────────────────────────────────────────
st.markdown("### Current Insight")
st.success(
    "Trend shows resilience despite dietary variability. "
    "High protein + fiber moderated improvement rate effectively. "
    "Interactive tooltips enabled using Plotly for portfolio demo."
)
st.caption("Insights are trend-based only and not medical advice.")
