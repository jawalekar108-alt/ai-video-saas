import streamlit as st
from src.pipeline import process_video

st.title("AI YouTube Video Summarizer")

url = st.text_input("Enter YouTube URL")

if url:

    st.video(url)

    if st.button("Generate Summary"):

        with st.spinner("Generating summary..."):

            summary = process_video(url)

            st.subheader("Summary")
        
            st.write("Processing transcript...")
            st.write(summary)
