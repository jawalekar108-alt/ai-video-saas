import streamlit as st
import threading
import uuid
import time

from src.transcript_engine import get_transcript
from src.analyzer import analyze


if "jobs" not in st.session_state:

    st.session_state.jobs={}



def process(job_id,url):

    st.session_state.jobs[job_id]["stage"]="Getting transcript"

    transcript=get_transcript(url)

    if not transcript:

        st.session_state.jobs[job_id]["status"]="failed"

        return


    st.session_state.jobs[job_id]["stage"]="Analyzing"

    notes=analyze(transcript)


    st.session_state.jobs[job_id]={

        "status":"done",

        "analysis":notes,

        "transcript":transcript,

        "stage":"Complete"

    }



st.set_page_config(

page_title="AI Video Intelligence",

page_icon="🎬"

)

st.title("AI Video Intelligence")


url=st.text_input("YouTube URL")


if st.button("Analyze"):

    if not url:

        st.warning("Enter URL")

    else:

        job_id=str(uuid.uuid4())

        st.session_state.jobs[job_id]={

            "status":"processing",

            "stage":"Starting"

        }

        thread=threading.Thread(

            target=process,

            args=(job_id,url),

            daemon=True

        )

        thread.start()

        st.session_state.job_id=job_id



if "job_id" in st.session_state:

    job_id=st.session_state.job_id


    if job_id not in st.session_state.jobs:

        st.error("Job lost. Retry.")
        st.stop()


    job=st.session_state.jobs[job_id]


    if job["status"]=="processing":

        st.info(job["stage"])

        time.sleep(2)

        st.rerun()


    elif job["status"]=="done":

        st.success("Analysis complete")

        st.subheader("AI Notes")

        st.write(job["analysis"])


        with st.expander("Transcript"):

            st.write(job["transcript"])


    elif job["status"]=="failed":

        st.error("Processing failed")
