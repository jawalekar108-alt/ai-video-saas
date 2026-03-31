import streamlit as st
import os

from dotenv import load_dotenv


from src.transcript import get_transcript
from src.analyzer import analyze
from src.chat import ask_video
from src.cache import load_cache, save_cache
from src.export import export_pdf
from src.cleanup import cleanup

load_dotenv()

# ---------------- PAGE ----------------

st.set_page_config(

    page_title="AI Video Intelligence",

    page_icon="🎬",

    layout="wide"

)

st.title("🎬 AI Video Intelligence SaaS")

st.write("Turn any YouTube video into smart study notes")


# ---------------- SESSION ----------------

def init_state():

    defaults={

        "transcript":"",
        "analysis":"",
        "loaded":False,
        "usage":0,
        "last_url":"",
        "pro":False,
        "processing":False

    }

    for k,v in defaults.items():

        if k not in st.session_state:

            st.session_state[k]=v


init_state()


# ---------------- INPUT ----------------

url=st.text_input(

    "Enter YouTube URL",

    key="url_input"

)

if url:

    if "youtube.com" in url or "youtu.be" in url:

        st.video(url)

    else:

        st.warning("Enter valid YouTube URL")


# ---------------- RESET ----------------

if url!=st.session_state.last_url:

    st.session_state.transcript=""

    st.session_state.analysis=""

    st.session_state.loaded=False

    st.session_state.last_url=url


# ---------------- SIDEBAR ----------------

with st.sidebar:

    st.title("💳 Plan")

    if st.session_state.pro:

        st.success("Pro Active")

    else:

        st.write("Free Plan")

        st.write("3 videos limit")

        st.write(

            f"{st.session_state.usage}/3 used"

        )

    st.divider()

    password=st.text_input(

        "Pro Access",

        type="password"

    )

    if password=="pro123":

        st.session_state.pro=True

        st.success("Pro unlocked")


# ---------------- ANALYZE ----------------

if st.button("🚀 Analyze Video"):

    if st.session_state.processing:

        st.stop()


    if not url:

        st.warning("Enter URL")

        st.stop()


    if not(

        "youtube.com" in url

        or

        "youtu.be" in url

    ):

        st.warning("Enter valid YouTube link")

        st.stop()


# FREE LIMIT

    if not st.session_state.pro:

        if st.session_state.usage>=3:

            st.warning("Free limit reached")

            st.stop()

        st.session_state.usage+=1


    st.session_state.processing=True


# ---------------- CACHE ----------------

    cache=load_cache(url)

    if cache:

        st.success("⚡ Loaded from cache")

        st.session_state.transcript=cache["transcript"]

        st.session_state.analysis=cache["analysis"]

        st.session_state.loaded=True

        st.session_state.processing=False


    else:

        try:

            cleanup()


# -------- GET TRANSCRIPT --------

            with st.spinner("Getting transcript..."):

                transcript=get_transcript(url)


# -------- VALIDATE --------

            if not transcript:

                st.warning("Transcript unavailable")

                uploaded=st.file_uploader(

                    "Upload transcript manually",

                    type=["txt"]

                )

                if uploaded:

                    transcript=uploaded.read().decode()

                else:

                    st.session_state.processing=False

                    st.stop()


# Prevent garbage analysis

            if len(transcript)<100:

                st.error("Transcript too short")

                st.session_state.processing=False

                st.stop()


# Prevent token overflow (IMPORTANT)

            transcript=transcript[:15000]


# -------- ANALYZE --------

            with st.spinner("Analyzing video..."):

                analysis=analyze(transcript)


# Validate AI output

            if not analysis:

                analysis="Analysis failed"


# -------- SAVE --------

            st.session_state.transcript=transcript

            st.session_state.analysis=analysis

            st.session_state.loaded=True


            save_cache(

                url,

                {

                    "transcript":transcript,

                    "analysis":analysis

                }

            )


            st.success("✅ Analysis complete")


        except Exception as e:

            st.error("Processing failed")

            st.info("Try another video with captions")


        st.session_state.processing=False


# ---------------- RESULTS ----------------

if st.session_state.loaded:

    tab1,tab2,tab3=st.tabs([

        "🧠 AI Analysis",

        "💬 Ask Video",

        "📜 Transcript"

    ])


# -------- TAB 1 --------

    with tab1:

        st.subheader("AI Analysis")

        st.markdown(

            st.session_state.analysis

        )


        col1,col2=st.columns(2)


        with col1:

            st.download_button(

                "⬇️ Download TXT",

                st.session_state.analysis,

                file_name="notes.txt"

            )


        with col2:

            pdf=export_pdf(

                "AI Video Notes",

                st.session_state.analysis

            )

            if pdf:

                st.download_button(

                    "📄 Download PDF",

                    data=pdf,

                    file_name="notes.pdf",

                    mime="application/pdf"

                )


# -------- TAB 2 --------

    with tab2:

        st.subheader("Ask Questions")

        question=st.text_input("Ask question")


        if st.button("Ask"):

            if not question:

                st.warning("Enter question")

            else:

                with st.spinner("Thinking..."):

                    answer=ask_video(

                        question,

                        st.session_state.transcript

                    )

                st.write(answer)


# -------- TAB 3 --------

    with tab3:

        st.subheader("Transcript")


        st.text_area(

            "Transcript",

            st.session_state.transcript,

            height=500

        )


        st.download_button(

            "⬇️ Download",

            st.session_state.transcript,

            file_name="transcript.txt"

        )
