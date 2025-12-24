import streamlit as st
import numpy as np
import plotly.graph_objects as go

# Data labels already defined above in your file
fig = go.Figure()

# Actual A1C
fig.add_trace(go.Scatter(
    x=week_labels,
    y=actual_a1c,
    mode="lines+markers",
    name="Actual A1C",
    hovertemplate="A1C: %{y:.2f}%<extra></extra>"
))

# Projected A1C
fig.add_trace(go.Scatter(
    x=week_labels,
    y=projected_a1c,
    mode="lines+markers",
    name="Projected A1C",
    line=dict(dash="dash"),
    hovertemplate="Projected: %{y:.2f}%<extra></extra>"
))

# Fiber Score
fig.add_trace(go.Scatter(
    x=week_labels,
    y=fiber_score,
    mode="lines+markers",
    name="Fiber Score",
    line=dict(dash="dot"),
    hovertemplate="Fiber: %{y:.1f}/10<extra></extra>"
))

# Protein Intake
fig.add_trace(go.Scatter(
    x=week_labels,
    y=protein_intake,
    mode="lines+markers",
    name="Protein (g/day)",
    line=dict(dash="dashdot"),
    hovertemplate="Protein: %{y} g/day<extra></extra>"
))

# Fat Intake
fig.add_trace(go.Scatter(
    x=week_labels,
    y=fat_intake,
    mode="lines+markers",
    name="Fat (g/day)",
    hovertemplate="Fat: %{y} g/day<extra></extra>"
))

# Confidence Band
fig.add_trace(go.Scatter(
    x=week_labels + week_labels[::-1],
    y=worst_case.tolist() + best_case[::-1].tolist(),
    fill="toself",
    name="Confidence Band",
    line=dict(width=0),
    hovertemplate="Best/Worst Range<br>Best: %{y:.2f}%<extra></extra>"
))

# Current Week Marker
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
    height=550,
    template="plotly_white"
)

st.plotly_chart(fig, use_container_width=True)
