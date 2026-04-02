import streamlit as st
from pipeline import process_video

st.set_page_config(page_title="AI Video Summarizer")

st.title("AI YouTube Video Summarizer")

url = st.text_input("Enter YouTube URL")

if url:

    st.video(url)

    if st.button("Generate Summary"):

        with st.spinner("Processing..."):

            summary = process_video(url)

            st.subheader("Summary")

            st.write(summary)
