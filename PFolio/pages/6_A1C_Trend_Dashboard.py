import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# ---------------------------------------------------
# PAGE CONFIG (lightweight, runs first)
# ---------------------------------------------------
st.set_page_config(
    page_title="A1C Insight Dashboard",
    layout="wide"
)

# ---------------------------------------------------
# DASHBOARD HEADER
# ---------------------------------------------------
st.title("📊 A1C Insight & Trend Dashboard")
st.caption("Actual vs Projected A1C with Fiber, Protein & Fat Overlay")
st.caption("Protein/Fiber patterns based on your portfolio prototype")

# ---------------------------------------------------
# SAMPLE DATA (replace later with dynamic input)
# ---------------------------------------------------
weeks = np.arange(17)  # 0 → 16 (17 weeks)

week_labels = [
    "11/23", "11/30", "12/07", "12/14",
    "12/21", "12/22", "12/23",
    "12/28", "01/04", "01/11", "01/18",
    "01/25", "02/01", "02/08", "02/15", "02/22", "03/01"
]

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

current_week = 6  # Week of 12/23 prototype index

# ---------------------------------------------------
# PLOT RENDERING
# ---------------------------------------------------
fig, ax1 = plt.subplots(figsize=(16, 6))

# --- A1C Lines ---
ax1.plot(weeks, actual_a1c, marker="o", linewidth=2.2, label="Actual A1C")
ax1.plot(weeks, projected_a1c, linestyle="--", linewidth=2.2, label="Projected A1C")
ax1.fill_between(weeks, best_case, worst_case, alpha=0.18, label="Confidence Band")

# --- Current Week Marker ---
ax1.axvline(x=current_week, linestyle=":", linewidth=1.8)
ax1.scatter(current_week, actual_a1c[current_week], s=140)

# --- Axis Formatting ---
ax1.set_xlabel("Week", fontsize=13)
ax1.set_ylabel("A1C (%)", fontsize=13)
ax1.set_xticks(weeks)
ax1.set_xticklabels(week_labels, fontsize=12)
ax1.grid(True)

# --- Overlay Axes ---
ax2 = ax1.twinx()
ax2.plot(weeks, fiber_score, linestyle="-.", marker="s", linewidth=1.8, label="Fiber Score")

ax3 = ax1.twinx()
ax3.spines["right"].set_position(("outward", 50))
ax3.plot(weeks, protein_intake, linestyle=":", marker="^", linewidth=1.8, label="Protein (g/day)")

ax4 = ax1.twinx()
ax4.spines["right"].set_position(("outward", 100))
ax4.plot(weeks, fat_intake, linestyle="--", marker="D", linewidth=1.8, label="Fat (g/day)")

ax2.set_ylabel("Fiber Score", fontsize=12)
ax3.set_ylabel("Protein (g/day)", fontsize=12)
ax4.set_ylabel("Fat (g/day)", fontsize=12)

# --- Unified Legend (efficient handle collection) ---
handles, labels = [], []
for axis in [ax1, ax2, ax3, ax4]:
    h, l = axis.get_legend_handles_labels()
    handles.extend(h)
    labels.extend(l)

fig.suptitle("Actual vs Projected A1C with Fiber, Protein & Fat Overlay", fontsize=18)

ax1.legend(handles, labels, loc="upper right", fontsize=11, frameon=True)

st.pyplot(fig)

# ---------------------------------------------------
# INSIGHT PANEL (Streamlit-optimized, no heavy ops)
# ---------------------------------------------------
st.markdown("### Current Insight")
st.success(
    "Trend shows resilience despite dietary variability. "
    "High protein + fiber moderated improvement rate effectively."
)
st.caption("Insights are trend-based only and not medical advice.")
