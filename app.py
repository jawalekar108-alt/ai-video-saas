import streamlit as st

import requests

import time


API="http://localhost:8000"


st.title(

"AI Video Intelligence"

)

url=st.text_input(

"YouTube URL"

)

if st.button("Analyze"):

    res=requests.get(

    f"{API}/process",

    params={"url":url}

    )

    job_id=

    res.json()["job_id"]

    st.session_state.job_id=job_id


if "job_id" in st.session_state:

    job_id=

    st.session_state.job_id

    status=

    requests.get(

    f"{API}/status",

    params={"job_id":job_id}

    ).json()


    if status["status"]=="processing":

        st.info("Processing...")

        time.sleep(3)

        st.rerun()


    elif status["status"]=="done":

        st.success("Complete")

        st.write(

        status["result"]["analysis"]

        )


    elif status["status"]=="failed":

        st.error("Failed")
