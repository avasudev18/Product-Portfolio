import os
import json
from datetime import date
import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# -------------------------------
# CONFIG
# -------------------------------
APP_TITLE = "📊 A1C Insight & Trend Dashboard (GPT-Powered)"
DATA_PATH = "a1c_logs.json"

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
MODEL = os.getenv("OPENAI_MODEL", "gpt-5.2")

if not OPENAI_API_KEY:
    st.error("Missing OPENAI_API_KEY. Add it to a .env file or environment variable.")
    st.stop()

client = OpenAI(api_key=OPENAI_API_KEY)

# -------------------------------
# YOUR SYSTEM PROMPT (Enhanced Model)
# -------------------------------
SYSTEM_PROMPT = """
You are an A1C Insight and Trend Engine for a consumer-facing digital health application.
Analyze user-provided lifestyle, physiology, and activity data to generate personalized A1C trends,
insights, and projections in a non-diagnostic, non-prescriptive manner.

Core Principles:
- Do not provide medical diagnoses or treatment advice
- Use plain language suitable for non-clinical users
- Focus on patterns, trends, and correlations, not certainty
- Ensure outputs are interpretable, transparent, and explainable

User Profile Context (Fixed Inputs):
Sex: Male
Age: 58
Height: 5 feet 11 inches
Weight: 175 lbs
Exercise Frequency: 4 times per week
Exercise Types: Structured exercise, Pickleball, Tennis

Output Guidelines:
Return a concise summary plus a structured report.
Include confidence disclaimer: “These insights are based on trends and self-reported data and are not medical advice.”
"""

# -------------------------------
# JSON SCHEMA FOR STRUCTURED OUTPUT
# -------------------------------
REPORT_SCHEMA = {
    "name": "daily_a1c_report",
    "schema": {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "date": {"type": "string"},
            "a1c_trend_summary": {"type": "string"},
            "daily_total_carbs_g": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "min": {"type": "number"},
                    "max": {"type": "number"}
                },
                "required": ["min", "max"]
            },
            "fiber_score_0_10": {"type": "number"},
            "protein_g": {"type": "number"},
            "fat_g": {"type": "number"},
            "rating": {"type": "string", "enum": ["Compliant", "Borderline", "High Risk"]},
            "carb_spike_alerts": {
                "type": "array",
                "items": {"type": "string"}
            },
            "recommendations": {
                "type": "array",
                "items": {"type": "string"},
                "minItems": 3,
                "maxItems": 7
            },
            "notes": {"type": "string"},
            "disclaimer": {"type": "string"}
        },
        "required": [
            "date",
            "a1c_trend_summary",
            "daily_total_carbs_g",
            "fiber_score_0_10",
            "protein_g",
            "fat_g",
            "rating",
            "carb_spike_alerts",
            "recommendations",
            "disclaimer"
        ]
    }
}

# -------------------------------
# STORAGE HELPERS
# -------------------------------
def load_logs(path: str) -> list[dict]:
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_logs(path: str, logs: list[dict]) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(logs, f, indent=2)

def upsert_log(logs: list[dict], report: dict) -> list[dict]:
    # replace if date exists
    d = report["date"]
    out = [x for x in logs if x.get("date") != d]
    out.append(report)
    out.sort(key=lambda x: x["date"])
    return out

# -------------------------------
# GPT CALL (Responses API + Structured Outputs)
# -------------------------------
def generate_report(entry_text: str, entry_date: str) -> dict:
    user_prompt = f"""
Date: {entry_date}

User Log (plain text):
{entry_text}

Tasks:
1) Estimate carbs by meal (Breakfast/Lunch/Dinner/Snacks) and total.
2) Produce a trend-based A1C insight summary (non-diagnostic).
3) Estimate fiber score (0–10), protein grams, fat grams (rough estimates are OK).
4) Output ONLY JSON that matches the provided schema.
"""

    resp = client.responses.create(
        model=MODEL,
        input=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        # Structured outputs (JSON schema)
        text={
            "format": {
                "type": "json_schema",
                "json_schema": REPORT_SCHEMA
            }
        },
        # Optional: reduce retention if desired
        store=False
    )
    # Responses API returns output text; parse JSON
    txt = resp.output_text
    return json.loads(txt)

# -------------------------------
# DASHBOARD PLOTTING (A1C + Fiber + Protein + Fat)
# -------------------------------
def plot_dashboard(df: pd.DataFrame, current_idx: int):
    # Minimal proxy A1C line from carbs/fiber/protein/fat (simple & explainable)
    # (Replace later with your real proxy/fit. For now: a stable directional index.)
    # Base line anchored at 6.4 start
    base = 6.4
    days = np.arange(len(df))
    # heuristic: lower carbs + higher fiber + exercise improves slope
    carbs_mid = (df["carbs_min"] + df["carbs_max"]) / 2
    slope = -0.0025  # gentle downward/day
    adj = (
        (carbs_mid - 110) * 0.0006   # more carbs -> higher
        - (df["fiber"] - 6.0) * 0.010
        - (df["protein"] - 90) * 0.0003
        + (df["fat"] - 75) * 0.0002
    )
    actual = base + slope * days + np.cumsum(adj.fillna(0).values) * 0.02

    # Projected curve toward 5.8 by end date (simple curve)
    projected = np.linspace(base, 5.8, len(df))

    best = projected - 0.08
    worst = projected + 0.12

    fig, ax1 = plt.subplots(figsize=(16, 6))

    ax1.plot(days, actual, marker="o", linewidth=2.5, label="Actual A1C (Proxy)")
    ax1.plot(days, projected, linestyle="--", linewidth=2.5, label="Projected A1C")
    ax1.fill_between(days, best, worst, alpha=0.25, label="Confidence Band (Best–Worst)")
    ax1.axvline(x=current_idx, linestyle=":", linewidth=2, label="Current Day")
    ax1.scatter(current_idx, actual[current_idx], s=160)

    ax1.set_xlabel("Day Index")
    ax1.set_ylabel("A1C (%)")
    ax1.grid(True)

    ax2 = ax1.twinx()
    ax2.plot(days, df["fiber"], linestyle="-.", marker="s", linewidth=2, label="Fiber (0–10)")
    ax2.set_ylabel("Fiber (0–10)")

    ax3 = ax1.twinx()
    ax3.spines.right.set_position(("outward", 60))
    ax3.plot(days, df["protein"], linestyle=":", marker="^", linewidth=2, label="Protein (g)")
    ax3.set_ylabel("Protein (g)")

    ax4 = ax1.twinx()
    ax4.spines.right.set_position(("outward", 120))
    ax4.plot(days, df["fat"], linestyle="--", marker="D", linewidth=2, label="Fat (g)")
    ax4.set_ylabel("Fat (g)")

    lines, labels = [], []
    for ax in [ax1, ax2, ax3, ax4]:
        l, lab = ax.get_legend_handles_labels()
        lines += l
        labels += lab
    ax1.legend(lines, labels, loc="upper right")
    plt.title("Actual vs Projected A1C + Fiber + Protein + Fat (Live Tracker)")
    plt.tight_layout()
    return fig

# -------------------------------
# UI
# -------------------------------
st.set_page_config(page_title="A1C Tracker", layout="wide")
st.title(APP_TITLE)

logs = load_logs(DATA_PATH)

colA, colB = st.columns([1, 1])

with colA:
    st.subheader("📝 Log Today")
    entry_date = st.date_input("Date", value=date.today()).isoformat()
    entry_text = st.text_area(
        "Paste meals/activity (plain text)",
        height=220,
        placeholder="Example:\nBreakfast: ...\nLunch: ...\nExercise: ...\nSleep: ..."
    )

    if st.button("Generate GPT Report + Save"):
        if not entry_text.strip():
            st.warning("Please paste your log first.")
        else:
            with st.spinner("Generating report..."):
                report = generate_report(entry_text=entry_text, entry_date=entry_date)

            # Flatten for dashboard convenience
            report["carbs_min"] = report["daily_total_carbs_g"]["min"]
            report["carbs_max"] = report["daily_total_carbs_g"]["max"]
            report["fiber"] = report["fiber_score_0_10"]
            report["protein"] = report["protein_g"]
            report["fat"] = report["fat_g"]

            logs = upsert_log(logs, report)
            save_logs(DATA_PATH, logs)
            st.success("Saved. Dashboard updated.")

with colB:
    st.subheader("📌 Latest GPT Report")
    if logs:
        latest = sorted(logs, key=lambda x: x["date"])[-1]
        st.markdown(f"**Date:** {latest['date']}")
        st.markdown(f"**Rating:** {latest['rating']}")
        st.markdown(f"**Carbs:** {latest['daily_total_carbs_g']['min']}–{latest['daily_total_carbs_g']['max']} g")
        st.markdown(f"**Fiber score:** {latest['fiber_score_0_10']:.1f} / 10")
        st.markdown(f"**Protein:** {latest['protein_g']:.0f} g  |  **Fat:** {latest['fat_g']:.0f} g")
        st.markdown(f"**Summary:** {latest['a1c_trend_summary']}")

        if latest["carb_spike_alerts"]:
            st.markdown("**Carb Spike Alerts**")
            st.write(latest["carb_spike_alerts"])

        st.markdown("**Recommendations**")
        st.write(latest["recommendations"])

        st.caption(latest["disclaimer"])
    else:
        st.info("No logs yet. Add your first entry to generate a report.")

st.divider()
st.subheader("📈 Live Dashboard")

if logs:
    df = pd.DataFrame(logs).sort_values("date")
    df["carbs_min"] = df["carbs_min"].astype(float)
    df["carbs_max"] = df["carbs_max"].astype(float)

    # Current day marker = latest row index
    current_idx = df.index[df["date"] == df["date"].max()][0]
    current_pos = list(df.index).index(current_idx)

    fig = plot_dashboard(df.reset_index(drop=True), current_pos)
    st.pyplot(fig)

    with st.expander("🔎 View raw history"):
        st.dataframe(df[["date","rating","carbs_min","carbs_max","fiber","protein","fat"]], use_container_width=True)
else:
    st.info("Dashboard will appear after the first saved GPT report.")

