import streamlit as st
import uuid
import time

from src.pipeline import run_pipeline
from src.export import export_pdf

# ---------------- SESSION ----------------
if "job" not in st.session_state:
    st.session_state.job = None

st.set_page_config(page_title="AI Video Intelligence", page_icon="🎬")

st.title("🎬 AI Video Intelligence")

url = st.text_input("Paste YouTube URL")

# 🎬 Preview
if url:
    try:
        st.video(url)
    except:
        st.warning("Invalid URL")

# ---------------- RUN ----------------
if st.button("Analyze"):
    if not url:
        st.warning("Enter URL")
    else:
        with st.spinner("Processing video..."):
            result = run_pipeline(url)
            st.session_state.job = result

# ---------------- RESULT ----------------
job = st.session_state.job

if job:
    if job["status"] == "failed":
        st.error("❌ Failed")
        st.code(job.get("error", "Unknown error"))

    else:
        st.success("✅ Done")

        st.subheader("🧠 Summary")
        st.write(job["summary"])

        with st.expander("📜 Transcript"):
            st.write(job["transcript"])

        # 📄 PDF EXPORT
        pdf = export_pdf(job["summary"], job["transcript"])

        st.download_button(
            "📄 Download PDF",
            pdf,
            file_name="analysis.pdf",
            mime="application/pdf"
        )
