import streamlit as st
import threading
import uuid
import time

from src.transcript_engine import get_transcript
from src.analyzer import analyze


# ---------------- SAFE GLOBAL STORE ----------------
jobs_store = {}


# ---------------- INIT SESSION ----------------
if "jobs" not in st.session_state:
    st.session_state.jobs = {}

if "job_id" not in st.session_state:
    st.session_state.job_id = None


# ---------------- BACKGROUND PROCESS ----------------
def process(job_id, url):
    try:
        jobs_store[job_id]["stage"] = "Getting transcript"

        transcript = get_transcript(url)

        if not transcript:
            jobs_store[job_id] = {
                "status": "failed",
                "stage": "Transcript Error",
                "error": "Transcript not found or disabled for this video"
            }
            return

        jobs_store[job_id]["stage"] = "Analyzing"

        notes = analyze(transcript)

        jobs_store[job_id] = {
            "status": "done",
            "analysis": notes,
            "transcript": transcript,
            "stage": "Complete"
        }

    except Exception as e:
        jobs_store[job_id] = {
            "status": "failed",
            "stage": "Error",
            "error": str(e)
        }


# ---------------- UI ----------------
st.set_page_config(
    page_title="AI Video Intelligence",
    page_icon="🎬"
)

st.title("🎬 AI Video Intelligence")

url = st.text_input("Paste YouTube URL")


# 🎬 SINGLE VIDEO PREVIEW (FIXED)
if url:
    try:
        st.video(url)
    except:
        st.warning("Invalid YouTube URL")


# ---------------- START JOB ----------------
if st.button("Analyze"):
    if not url:
        st.warning("Enter URL")
    else:
        job_id = str(uuid.uuid4())

        job_data = {
            "status": "processing",
            "stage": "Starting"
        }

        st.session_state.jobs[job_id] = job_data
        jobs_store[job_id] = job_data

        threading.Thread(
            target=process,
            args=(job_id, url),
            daemon=True
        ).start()

        st.session_state.job_id = job_id


# ---------------- JOB STATUS ----------------
if st.session_state.job_id:
    job_id = st.session_state.job_id

    if job_id not in jobs_store:
        st.error("Job lost. Retry.")
        st.stop()

    job = jobs_store[job_id]

    if job["status"] == "processing":
        st.info(f"⏳ {job['stage']}...")
        time.sleep(2)
        st.rerun()

    elif job["status"] == "done":
        st.success("✅ Analysis complete")

        st.subheader("🧠 AI Notes")
        st.write(job["analysis"])

        with st.expander("📜 Transcript"):
            st.write(job["transcript"])

    elif job["status"] == "failed":
        st.error("❌ Processing failed")
        if "error" in job:
            st.code(job["error"])
