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
# LOAD ENV FIRST
# -------------------------------
load_dotenv()  # ✅ Load .env before using getenv()

# -------------------------------
# CONFIG
# -------------------------------
APP_TITLE = "📊 A1C Insight & Trend Dashboard (GPT-Powered)"
MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
SHEET_CSV_URL = os.getenv("SHEET_CSV_URL", "")

if not OPENAI_API_KEY:
    st.error("Missing OPENAI_API_KEY. Please add it to your .env file.")
    st.stop()

if not SHEET_CSV_URL:
    st.error("Missing SHEET_CSV_URL. Please add your Google Sheet CSV export URL in .env.")
    st.stop()

client = OpenAI(api_key=OPENAI_API_KEY)

# -------------------------------
# SYSTEM PROMPT
# -------------------------------
SYSTEM_PROMPT = """
You are an A1C Insight & Trend Analyzer for a user-friendly health dashboard.
Provide lifestyle pattern insights in a clear, supportive, and non-medical way.

⚠ Disclaimer: “These insights are based on trends and self-reported data and are not medical advice.”
Keep the tone simple, helpful, and encouraging.
"""

# -------------------------------
# DASHBOARD PLOTTING
# -------------------------------
def plot_dashboard(df: pd.DataFrame, current_pos: int):
    base = 6.4  # starting reference A1C
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
    ax1.fill_between(days, best, worst, alpha=0.25, label="Confidence Band")
    ax1.axvline(x=current_pos, linestyle=":", linewidth=2, label="Current Day")
    ax1.scatter(current_pos, actual[current_pos], s=160)

    ax1.set_xlabel("Day Index")
    ax1.set_ylabel("A1C (%)")
    ax1.grid(True)

    ax2 = ax1.twinx()
    ax2.plot(days, df["fiber"], linestyle="-.", marker="s", linewidth=2, label="Fiber Score")
    ax2.set_ylabel("Fiber (0–10)")

    ax3 = ax1.twinx()
    ax3.spines.right.set_position(("outward", 60))
    ax3.plot(days, df["protein"], linestyle=":", marker="^", linewidth=2, label="Protein (g)")
    ax3.set_ylabel("Protein (g)")

    ax4 = ax1.twinx()
    ax4.spines.right.set_position(("outward", 120))
    ax4.plot(days, df["fat"], linestyle="--", marker="D", linewidth=2, label="Fat (g)")
    ax4.set_ylabel("Fat (g)")

    # Combine legends
    lines, labels = [], []
    for ax in [ax1, ax2, ax3, ax4]:
        l, lab = ax.get_legend_handles_labels()
        lines += l
        labels += lab

    ax1.legend(lines, labels, loc="upper right")
    plt.title("A1C Trend with Fiber/Protein/Fat Correlation")
    plt.tight_layout()
    return fig

# -------------------------------
# GOOGLE SHEET READER
# -------------------------------
@st.cache_data(ttl=60)
def read_diet_logs_from_sheet(csv_url: str) -> pd.DataFrame:
    df = pd.read_csv(csv_url)
    df.columns = [c.strip().lower() for c in df.columns]
    if "date" not in df.columns or "entry_text" not in df.columns:
        raise ValueError("Sheet must contain columns: date, entry_text")
    df["date"] = pd.to_datetime(df["date"]).dt.date.astype(str)
    df["entry_text"] = df["entry_text"].fillna("").astype(str)
    return df.sort_values("date")

def get_entry_text_for_date(diet_df: pd.DataFrame, entry_date: str) -> str:
    match = diet_df[diet_df["date"] == entry_date]
    if match.empty:
        return ""
    return "\n\n".join(match["entry_text"].tolist()).strip()

# -------------------------------
# GPT REPORT GENERATION
# -------------------------------
def call_gpt_for_log(entry_text: str, entry_date: str) -> dict:
    user_prompt = f"""
Date: {entry_date}

User Log (plain text):
{entry_text}

Return only JSON with:
- carbs_min, carbs_max (g)
- fiber (0–10)
- protein (g)
- fat (g)
- rating (Compliant / Borderline / High Risk)
- trend summary (1 line)
- recommendations (3–7 short points)
- disclaimer
"""

    resp = client.responses.create(
        model=MODEL,
        input=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        store=False
    )
    return json.loads(resp.output_text.strip())

# -------------------------------
# STREAMLIT UI
# -------------------------------
st.set_page_config(page_title="A1C Tracker", layout="wide")
st.title(APP_TITLE)

try:
    diet_df = read_diet_logs_from_sheet(SHEET_CSV_URL)
except Exception as e:
    st.error(f"Failed to read diet logs from sheet: {e}")
    st.stop()

colA, colB = st.columns([1, 1])

with colA:
    st.subheader("📝 Today’s Log (from Google Sheet)")
    today_date = st.date_input("Date", value=date.today()).isoformat()
    today_iso = date.fromisoformat(today_date).isoformat()

    sheet_text = get_entry_text_for_date(diet_df, today_iso)
    entry_text = st.text_area("Diet/activity text", value=sheet_text, height=220)

    if st.button("Generate GPT Report"):
        if not entry_text.strip():
            st.warning("No log text found for this date.")
        else:
            with st.spinner("Generating GPT trend insights…"):
                report = call_gpt_for_log(entry_text, today_iso)

            # Store in session history
            rep = {
                "date": report["date"],
                "carbs_min": report["carbs_min"],
                "carbs_max": report["carbs_max"],
                "fiber": report["fiber"],
                "protein": report["protein"],
                "fat": report["fat"],
                "rating": report["rating"],
                "a1c_trend_summary": report["trend summary"],
                "recommendations": report["recommendations"],
                "disclaimer": report["disclaimer"]
            }

            if "report_history" not in st.session_state:
                st.session_state["report_history"] = []

            # Upsert into session history
            history = [x for x in st.session_state["report_history"] if x["date"] != rep["date"]]
            history.append(rep)
            history.sort(key=lambda x: x["date"])
            st.session_state["report_history"] = history
            st.success("Report generated & session dashboard updated.")

with colB:
    st.subheader("📌 Latest GPT Report")
    history = st.session_state.get("report_history", [])
    if history:
        latest = history[-1]
        st.markdown(f"**Date:** {latest['date']}")
        st.markdown(f"**Rating:** {latest['rating']}")
        st.markdown(f"**Carbs:** {latest['carbs_min']}–{latest['carbs_max']} g")
        st.markdown(f"**Fiber Score:** {latest['fiber']:.1f} / 10")
        st.markdown(f"**Protein:** {latest['protein']:.0f} g  |  **Fat:** {latest['fat']:.0f} g")
        st.markdown(f"**Summary:** {latest['a1c_trend_summary']}")
        st.write("**Recommendations:**", latest["recommendations"])
        st.caption(latest["disclaimer"])
    else:
        st.info("No reports generated yet this session.")

st.divider()
st.subheader("📈 Live Dashboard (Session History)")

history = st.session_state.get("report_history", [])
if history:
    df = pd.DataFrame(history).sort_values("date").reset_index(drop=True)
    fig = plot_dashboard(df, current_pos=len(df)-1)
    st.pyplot(fig)

    with st.expander("🔎 Raw session history"):
        st.dataframe(df[["date","rating","carbs_min","carbs_max","fiber","protein","fat"]], use_container_width=True)
else:
    st.info("Dashboard will appear after first GPT report.")
