import os
import json
from datetime import date
import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from dotenv import load_dotenv
import google.generativeai as genai

# -------------------------------
# LOAD CONFIG
# -------------------------------
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
SHEET_CSV_URL = os.getenv("SHEET_CSV_URL", "")

if not GEMINI_API_KEY:
    st.error("Missing GEMINI_API_KEY in .env")
    st.stop()

if not SHEET_CSV_URL:
    st.error("Missing SHEET_CSV_URL in .env")
    st.stop()

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)
gemini_model = genai.GenerativeModel("gemini-1.5-flash")

APP_TITLE = "📊 A1C Insight & Trend Dashboard (Gemini AI)"
st.set_page_config(page_title="A1C Tracker", layout="wide")
st.title(APP_TITLE)

# -------------------------------
# READ GOOGLE SHEET
# -------------------------------
@st.cache_data(ttl=60)
def read_diet_logs_from_sheet(csv_url: str) -> pd.DataFrame:
    try:
        df = pd.read_csv(csv_url)
    except Exception:
        st.error("Failed to read Google Sheet CSV. Make sure the sheet is published as CSV export.")
        return pd.DataFrame()

    df.columns = [c.strip().lower() for c in df.columns]
    if "date" not in df.columns or "entry_text" not in df.columns:
        st.error("Sheet must contain columns: date, entry_text")
        st.stop()

    df["date"] = pd.to_datetime(df["date"]).dt.date.astype(str)
    df["entry_text"] = df["entry_text"].fillna("").astype(str)
    return df.sort_values("date")

diet_df = read_diet_logs_from_sheet(SHEET_CSV_URL)

def get_entry_text_for_date(diet_df: pd.DataFrame, entry_date: str) -> str:
    match = diet_df[diet_df["date"] == entry_date]
    if match.empty:
        return ""
    return "\n\n".join(match["entry_text"].tolist()).strip()

# -------------------------------
# GEMINI ANALYSIS CALL
# -------------------------------
def call_gemini_for_log(entry_text: str, entry_date: str):
    prompt = f"""
You are an A1C Trend Insight Engine.
Give results in simple, clear, supportive, non-medical language.

User Diet & Activity Log:
{entry_text}

Date:
{entry_date}

Return JSON with:
{{
  "date": "{entry_date}",
  "carbs_min": number,
  "carbs_max": number,
  "fiber": number (0-10),
  "protein": number,
  "fat": number,
  "rating": "Compliant" | "Borderline" | "High Risk",
  "trend_summary": string,
  "recommendations": [3-7 short points],
  "disclaimer": string
}}
"""
    try:
        response = gemini_model.generate_content(prompt)
        text = response.text.strip()
        start = text.find("{")
        end = text.rfind("}") + 1
        return json.loads(text[start:end])
    except Exception as e:
        st.error(f"Gemini analysis failed: {e}")
        return None

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

    fig, ax = plt.subplots(figsize=(16, 6))
    ax.plot(days, actual, marker="o", linewidth=2.5, label="Actual A1C (Proxy)")
    ax.plot(days, projected, linestyle="--", linewidth=2.5, label="Projected A1C")
    ax.fill_between(days, best, worst, alpha=0.25, label="Confidence Band")
    ax.axvline(x=current_pos, linestyle=":", linewidth=2)
    ax.scatter(current_pos, actual[current_pos], s=160)

    ax.set_xlabel("Day Index")
    ax.set_ylabel("A1C (%)")
    ax.grid(True)
    ax.legend(loc="upper right")
    plt.title("A1C Trend Correlation (Gemini AI)")
    plt.tight_layout()
    return fig

# -------------------------------
# UI SECTIONS
# -------------------------------
colA, colB = st.columns([1,1])

with colA:
    st.subheader("📝 Today’s Log")
    entry_date = st.date_input("Select Date", value=date.today()).isoformat()
    today_iso = entry_date

    sheet_text = get_entry_text_for_date(diet_df, today_iso)
    entry_text = st.text_area("Diet/activity text", value=sheet_text, height=220)

    if st.button("Generate Gemini Report"):
        if not entry_text.strip():
            st.warning("No log text found for this date in sheet.")
        else:
            with st.spinner("Generating Gemini insights…"):
                report = call_gemini_for_log(entry_text, today_iso)

            if report:
                if "report_history" not in st.session_state:
                    st.session_state["report_history"] = []
                history = [x for x in st.session_state["report_history"] if x["date"] != report["date"]]
                history.append(report)
                history.sort(key=lambda x: x["date"])
                st.session_state["report_history"] = history
                st.success("Gemini report generated!")

with colB:
    st.subheader("📌 Latest Report")
    history = st.session_state.get("report_history", [])
    if history:
        latest = history[-1]
        st.markdown(f"**Date:** {latest['date']}")
        st.markdown(f"**Rating:** {latest['rating']}")
        st.markdown(f"**Carbs:** {latest['carbs_min']}–{latest['carbs_max']} g")
        st.markdown(f"**Fiber Score:** {latest['fiber']:.1f} / 10")
        st.markdown(f"**Protein:** {latest['protein']} g  |  **Fat:** {latest['fat']} g")
        st.markdown(f"**Summary:** {latest['trend_summary']}")
        st.write("**Recommendations:**", latest["recommendations"])
        st.caption(latest["disclaimer"])
    else:
        st.info("No reports yet. Generate one!")

st.divider()
st.subheader("📈 Live Dashboard")

history = st.session_state.get("report_history", [])
if history:
    df = pd.DataFrame(history).reset_index(drop=True)
    fig = plot_dashboard(df, current_pos=len(df)-1)
    st.pyplot(fig)

    with st.expander("🔎 Raw session history"):
        st.dataframe(df[["date","rating","carbs_min","carbs_max","fiber","protein","fat"]], use_container_width=True)
else:
    st.info("Dashboard appears after first Gemini report.")
