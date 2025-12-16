import os
import time
import json
import requests
import streamlit as st

# ----------------------------
# CONFIG
# ----------------------------
API_BASE = "https://pm-interview-prep-workflow-with-smart-decis-238b266e.crewai.com"
# DEFAULT_TOKEN = "PUT_YOUR_TOKEN_HERE"  # better: use st.secrets or env var
DEFAULT_TOKEN = "2c5347f69d50"  # better: use st.secrets or env var
st.set_page_config(page_title="PM Interview Prep Workflow Runner", layout="wide")

def get_token() -> str:
    # Priority: Streamlit secrets -> env var -> fallback constant
    return (
        st.secrets.get("CREWAI_BEARER_TOKEN", None)
        or os.getenv("CREWAI_BEARER_TOKEN", None)
        or DEFAULT_TOKEN
    )

def auth_headers(token: str) -> dict:
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

def safe_json(resp: requests.Response):
    try:
        return resp.json()
    except Exception:
        return {"_raw_text": resp.text, "_status_code": resp.status_code}

def call_get_inputs(token: str) -> dict:
    url = f"{API_BASE}/inputs"
    r = requests.get(url, headers=auth_headers(token), timeout=30)
    return safe_json(r)

def call_kickoff(token: str, payload: dict) -> dict:
    url = f"{API_BASE}/kickoff"
    r = requests.post(url, headers=auth_headers(token), data=json.dumps(payload), timeout=60)
    return safe_json(r)

def call_status(token: str, task_id: str) -> dict:
    url = f"{API_BASE}/status/{task_id}"
    r = requests.get(url, headers=auth_headers(token), timeout=90)
    return safe_json(r)

def read_uploaded_file(uploaded_file) -> str:
    """
    Minimal, dependency-light approach:
    - txt: decode
    - pdf/docx: we pass bytes as base64-like safe string? (Not ideal)
    BEST practice: extract text with libraries. Here we do a simple fallback.
    """
    name = uploaded_file.name.lower()
    data = uploaded_file.read()

    if name.endswith(".txt"):
        try:
            return data.decode("utf-8", errors="ignore")
        except Exception:
            return data.decode(errors="ignore")

    # For PDF/DOCX: if your API expects raw text, you should extract text locally.
    # Without extra libs, we send a short note and ask user to paste text instead.
    return (
        f"[Uploaded file: {uploaded_file.name} ({len(data)} bytes).]\n"
        "NOTE: This app is not extracting text from PDF/DOCX by default. "
        "If your workflow requires resume text, paste resume text into the box below "
        "or add PDF/DOCX text extraction."
    )

# ----------------------------
# UI
# ----------------------------
st.title("PM Interview Prep Workflow (API Runner)")

with st.sidebar:
    st.header("API Settings")
    token = st.text_input("Bearer Token", value=get_token(), type="password")
    st.caption("Tip: store as Streamlit secret `CREWAI_BEARER_TOKEN` or env var.")

colA, colB = st.columns([1, 1], gap="large")

with colA:
    st.subheader("Inputs")

    # Required API fields (as per your screenshot)
    candidate_name = st.text_input(
        "candidate_name *",
        placeholder="Anilkumar Vasudevakurup"
    )

    job_title = st.text_input(
        "job_title *",
        placeholder="Customer Success Manager"
    )

    company_name = st.text_input(
        "company_name *",
        placeholder="NiCE"
    )

    st.divider()

    # Optional supporting inputs (resume + job description)
    resume_file = st.file_uploader(
        "Upload Resume (TXT/PDF/DOCX)",
        type=["txt", "pdf", "docx"]
    )

    pasted_resume = st.text_area(
        "Or paste resume text",
        height=220,
        placeholder="Paste resume text here..."
    )

    job_desc = st.text_area(
        "Job Description",
        height=280,
        placeholder="Paste the job description here..."
    )

    st.divider()

    show_inputs_schema = st.button("Fetch required inputs schema (GET /inputs)")



with colB:
    st.subheader("Run + Results")
    status_box = st.empty()
    raw_box = st.empty()

    start_btn = st.button("Start workflow (POST /kickoff)", type="primary")
    poll_seconds = st.slider("Polling interval (seconds)", 1, 10, 2)
    
    st.write("start_btn =", start_btn)
# ----------------------------
# Actions
# ----------------------------
if show_inputs_schema:
    try:
        schema = call_get_inputs(token)
        st.info("Response from GET /inputs")
        st.json(schema)
    except requests.RequestException as e:
        st.error(f"Network error calling /inputs: {e}")

def build_payload() -> dict:
    resume_text = ""
    if pasted_resume.strip():
        resume_text = pasted_resume.strip()
    elif resume_file is not None:
        resume_text = read_uploaded_file(resume_file).strip()

    # Adjust keys below to match your crew's expected input names from GET /inputs.
    return {
        "inputs": {
            "candidate_name": candidate_name.strip(),
            "job_title": job_title.strip(),
            "company_name": company_name.strip()
        }
    }

if start_btn:
    if not token or token == "PUT_YOUR_TOKEN_HERE":
        st.error("Please provide a valid Bearer Token (sidebar).")
        st.stop()

    if not company.strip() or not job_desc.strip():
        st.error("Please fill Company Name and Job Description.")
        st.stop()

    payload = build_payload()

    # Basic guard: avoid sending empty resume if user provided neither file nor paste
    if not payload["inputs"]["resume"]:
        st.warning("No resume text provided. Upload or paste resume text for best results.")

    status_box.info("Starting workflow...")
    raw_box.empty()

    try:
        kickoff_resp = call_kickoff(token, payload)
        raw_box.caption("Kickoff response")
        raw_box.json(kickoff_resp)

        # Common patterns: {"task_id": "..."} or {"id": "..."} etc.
        task_id = (
            kickoff_resp.get("task_id")
            or kickoff_resp.get("id")
            or kickoff_resp.get("taskId")
            or kickoff_resp.get("data", {}).get("task_id")
        )

        if not task_id:
            st.error("Could not find task_id in kickoff response. Check the response JSON above.")
            st.stop()

        status_box.success(f"Workflow started. task_id = {task_id}")

        # Poll status
        with st.spinner("Polling status..."):
            while True:
                s = call_status(token, task_id)
                status_box.write("Latest status:")
                status_box.json(s)

                # Try to detect completion
                state = (s.get("status") or s.get("state") or "").lower()
                done_flags = {"completed", "complete", "done", "succeeded", "success", "failed", "error", "cancelled", "canceled"}

                if state in done_flags:
                    break

                # Some APIs return a boolean
                if s.get("done") is True or s.get("completed") is True:
                    break

                time.sleep(poll_seconds)

        st.divider()
        st.subheader("Final Output")

        # Try common output fields
        final_output = (
            s.get("result")
            or s.get("output")
            or s.get("final_output")
            or s.get("data", {}).get("result")
            or s.get("data", {}).get("output")
        )

        if isinstance(final_output, (dict, list)):
            st.json(final_output)
        elif isinstance(final_output, str) and final_output.strip():
            st.write(final_output)
        else:
            st.info("No obvious final output field found. Showing full final status JSON:")
            st.json(s)

    except requests.RequestException as e:
        st.error(f"Network error: {e}")
    except Exception as e:
        st.error(f"Unexpected error: {e}")
5
