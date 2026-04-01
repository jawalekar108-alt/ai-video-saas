import streamlit as st

import threading

import uuid

import time

from src.transcript_engine import get_transcript

from src.analyzer import analyze


jobs={}


def process(job_id,url):

    jobs[job_id]["stage"]="Getting transcript"

    transcript=get_transcript(url)

    if not transcript:

        jobs[job_id]["status"]="failed"

        return

    jobs[job_id]["stage"]="Analyzing"

    notes=analyze(transcript)

    jobs[job_id]={

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

        jobs[job_id]={

            "status":"processing",

            "stage":"Starting"

        }

        thread=threading.Thread(

            target=process,

            args=(job_id,url)

        )

        thread.start()

        st.session_state.job_id=job_id



if "job_id" in st.session_state:

    job_id=st.session_state.job_id

    job=jobs[job_id]


    if job["status"]=="processing":

        st.info(job["stage"])

        time.sleep(2)

        st.rerun()


    elif job["status"]=="done":

        st.success("Done")

        st.subheader("AI Notes")

        st.write(job["analysis"])


        with st.expander("Transcript"):

            st.write(job["transcript"])


    elif job["status"]=="failed":

        st.error("Failed to process video")
