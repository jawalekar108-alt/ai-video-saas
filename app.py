import streamlit as st
import requests
import time

API = "http://localhost:8000"

st.set_page_config(
    page_title="AI Video Intelligence",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 AI Video Intelligence")

url = st.text_input("Enter YouTube URL")

if st.button("Analyze Video"):

    if not url:

        st.warning("Enter URL")

    else:

        response = requests.get(

            f"{API}/process",

            params={"url": url}

        )

        data = response.json()

        job_id = data["job_id"]

        st.session_state["job_id"] = job_id


if "job_id" in st.session_state:

    job_id = st.session_state["job_id"]

    status_response = requests.get(

        f"{API}/status",

        params={"job_id": job_id}

    )

    status = status_response.json()


    if status["status"] == "processing":

        st.info("Processing video...")

        time.sleep(2)

        st.rerun()


    elif status["status"] == "done":

        st.success("Analysis complete")

        st.subheader("AI Notes")

        st.write(status["result"]["analysis"])


    elif status["status"] == "failed":

        st.error("Processing failed")
