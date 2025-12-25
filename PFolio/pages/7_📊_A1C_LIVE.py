import os
import json
from datetime import date
import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from dotenv import load_dotenv
from openai import OpenAI

# -------------------------------
# ENV / CONFIG
# -------------------------------
load_dotenv()  # ✅ must come BEFORE getenv()

APP_TITLE = "📊 A1C Insight & Trend Dashboard (GPT-Powered)"
MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")  # keep configurable
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# Public Google Sheet -> CSV export URL
# Example format:
# https://docs.google.com/spreadsheets/d/<SPREADSHEET_ID>/gviz/tq?tqx=out:csv&sheet=DietLogs
SHEET_CSV_URL = os.getenv("https://docs.google.com/spreadsheets/d/e/2PACX-1vRcuj-g59c5JryG92ELeX-zk9vkaAhhWgoD0G9OtD_7EyEHTsZwvzWBAIzd6jubaw/pubhtml?gid=1563587956&single=true", "")

if not OPENAI_API_KEY:
    st.error("Missing OPENAI_API_KEY. Add it to .env or Streamlit secrets.")
    st.stop()

if not SHEET_CSV_URL:
    st.error("Missing SHEET_CSV_URL. Add it to .env or Streamlit secrets.")
    st.stop()

client = OpenAI(api_key=OPENAI_API_KEY)

# -------------------------------
# SYSTEM PROMPT
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
# STRUCTURED OUTPUT SCHEMA (Responses API)
# -------------------------------
REPORT_SCHEMA = {
    "name": "daily_a1c_report",
    "strict": True,  # ✅ important for strict structured outputs
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
            "carb_spike_alerts": {"type": "array", "items": {"type": "string"}},
            "recommendations": {"type": "array", "items": {"type": "string"}, "minItems": 3, "maxItems": 7},
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
# GOOGLE SHEET READERS
# -------------------------------
@st.cache_data(ttl=60)
def read_diet_logs_from_sheet(csv_url: str) -> pd.DataFrame:
    """
    Reads a public Google Sheet tab exported as CSV.
    Expect columns: date, entry_text
    """
    df = pd.read_csv(csv_url)
    df.columns = [c.strip().lower() for c in df.columns]

    if "date" not in df.columns or "entry_text" not in df.columns:
        raise ValueError("Sheet must contain columns: date, entry_text")

    # normalize date to ISO string
    df["date"] = pd.to_datetime(df["date"]).dt.date.astype(str)
    df["entry_text"] = df["entry_text"].fillna("").astype(str)
    return df.sort_values("date")

def get_entry_text_for_date(diet_df: pd.DataFrame, entry_date: str) -> str:
    match = diet_df[diet_df["date"] == entry_date]
    if match.empty:
        return ""
    # If multiple rows, join them
    return "\n\n".join(match["entry_text"].tolist()).strip()

# -------------------------------
# GPT REPORT GENERATOR
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
        text={
            "format": {
                "type": "json_schema",
                "json_schema": REPORT_SCHEMA
            }
        },
        store=False
    )

    # The SDK helper returns the final text response
    txt = resp.output_text.strip()
    return json.loads(txt)

# -------------------------------
# DASHBOARD PLOTTING
# -------------------------------
def plot_dashboard(df: pd.DataFrame, current_pos: int):
    base = 6.4
    days = np.arange(len(df))

    carbs_mid = (df["carbs_min"] + df["carbs_max"]) / 2
    slope = -0.0025

    adj = (
        (carbs_mid - 110) * 0.0006
        - (df["fiber"] - 6.0) * 0.010
        - (df["protein"] - 90) * 0.0003
        + (df["fat"] - 75) * 0.0002
    )
    actual = base + slope * days + np.cumsum(adj.fillna(0).values) * 0.02

    projected = np.linspace(base, 5.8, len(df))
    best = projected - 0.08
    worst = projected + 0.12

    fig, ax1 = plt.subplots(figsize=(16, 6))
    ax1.plot(days, actual, marker="o", linewidth=2.5, label="Actual A1C (Proxy)")
    ax1.plot(days, projected, linestyle="--", linewidth=2.5, label="Projected A1C")
    ax1.fill_between(days, best, worst, alpha=0.25, label="Confidence Band (Best–Worst)")
    ax1.axvline(x=current_pos, linestyle=":", linewidth=2, label="Current Day")
    ax1.scatter(current_pos, actual[current_pos], s=160)

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

try:
    diet_df = read_diet_logs_from_sheet(SHEET_CSV_URL)
except Exception as e:
    st.error(f"Failed to read Google Sheet CSV. Error: {e}")
    st.stop()

colA, colB = st.columns([1, 1])

with colA:
    st.subheader("📝 Log (from Google Sheet)")
    entry_date = st.date_input("Date", value=date.today()).isoformat()

    sheet_text = get_entry_text_for_date(diet_df, entry_date)
    entry_text = st.text_area(
        "Diet/activity text (auto-loaded from sheet; editable)",
        value=sheet_text,
        height=220,
        placeholder="If blank, add the row in Google Sheet (date, entry_text)."
    )

    if st.button("Generate GPT Report (no local DB)"):
        if not entry_text.strip():
            st.warning("No entry found for this date in the sheet, and the text box is empty.")
        else:
            with st.spinner("Generating report..."):
                report = generate_report(entry_text=entry_text, entry_date=entry_date)

            # Flatten for dashboard
            report_flat = dict(report)
            report_flat["carbs_min"] = report["daily_total_carbs_g"]["min"]
            report_flat["carbs_max"] = report["daily_total_carbs_g"]["max"]
            report_flat["fiber"] = report["fiber_score_0_10"]
            report_flat["protein"] = report["protein_g"]
            report_flat["fat"] = report["fat_g"]

            st.session_state["latest_report"] = report_flat
            st.success("Report generated (not saved locally).")

with colB:
    st.subheader("📌 Latest GPT Report")

    latest = st.session_state.get("latest_report")
    if latest:
        st.markdown(f"**Date:** {latest['date']}")
        st.markdown(f"**Rating:** {latest['rating']}")
        st.markdown(f"**Carbs:** {latest['daily_total_carbs_g']['min']}–{latest['daily_total_carbs_g']['max']} g")
        st.markdown(f"**Fiber score:** {latest['fiber_score_0_10']:.1f} / 10")
        st.markdown(f"**Protein:** {latest['protein_g']:.0f} g  |  **Fat:** {latest['fat_g']:.0f} g")
        st.markdown(f"**Summary:** {latest['a1c_trend_summary']}")

        if latest.get("carb_spike_alerts"):
            st.markdown("**Carb Spike Alerts**")
            st.write(latest["carb_spike_alerts"])

        st.markdown("**Recommendations**")
        st.write(latest["recommendations"])
        st.caption(latest["disclaimer"])
    else:
        st.info("Generate a report to see it here.")

st.divider()
st.subheader("📈 Live Dashboard")

# Build dashboard from generated reports in-session only
# (If you want persistent dashboard history, store reports back into a Google Sheet tab — see Option B below.)
if "report_history" not in st.session_state:
    st.session_state["report_history"] = []

if st.session_state.get("latest_report"):
    # upsert into in-session history
    rep = st.session_state["latest_report"]
    hist = [r for r in st.session_state["report_history"] if r["date"] != rep["date"]]
    hist.append(rep)
    hist.sort(key=lambda x: x["date"])
    st.session_state["report_history"] = hist

history = st.session_state["report_history"]
if history:
    df = pd.DataFrame(history).sort_values("date").reset_index(drop=True)
    df["carbs_min"] = df["carbs_min"].astype(float)
    df["carbs_max"] = df["carbs_max"].astype(float)

    current_pos = df.index[df["date"] == df["date"].max()][0]
    fig = plot_dashboard(df, int(current_pos))
    st.pyplot(fig)

    with st.expander("🔎 View raw history (this session)"):
        st.dataframe(df[["date","rating","carbs_min","carbs_max","fiber","protein","fat"]], use_container_width=True)
else:
    st.info("Dashboard appears after you generate at least one GPT report.")
