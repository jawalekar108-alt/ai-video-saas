import streamlit as st

from src.transcript import get_transcript
from src.analyzer import analyze
from src.chat import ask_video
from src.cache import load_cache, save_cache
from src.export import export_pdf


# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="AI Video Intelligence",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 AI Video Intelligence SaaS")
st.write("Turn any YouTube video into smart study notes")


# ---------------- SESSION STATE ----------------

def init_state():

    defaults = {

        "transcript": "",
        "analysis": "",
        "loaded": False,
        "usage": 0,
        "last_url": "",
        "pro": False,
        "processing": False

    }

    for key,value in defaults.items():

        if key not in st.session_state:

            st.session_state[key] = value


init_state()


# ---------------- INPUT ----------------

url = st.text_input(
    "Enter YouTube URL",
    key="url_input"
)

if url:

    if "youtube.com" in url or "youtu.be" in url:

        st.video(url)

    else:

        st.warning("Enter valid YouTube URL")


# ---------------- RESET WHEN URL CHANGES ----------------

if url != st.session_state.last_url:

    st.session_state.transcript = ""

    st.session_state.analysis = ""

    st.session_state.loaded = False

    st.session_state.last_url = url


# ---------------- SIDEBAR ----------------

with st.sidebar:

    st.title("💳 Plan")

    if st.session_state.pro:

        st.success("Pro Plan Active")

    else:

        st.write("Free Plan")

        st.write("3 videos limit")

        st.write(
            f"{st.session_state.usage}/3 used"
        )

    st.divider()

    password = st.text_input(
        "Pro Access",
        type="password"
    )

    if password == "pro123":

        st.session_state.pro = True

        st.success("Pro unlocked")


# ---------------- ANALYZE BUTTON ----------------

if st.button("🚀 Analyze Video"):

    if st.session_state.processing:

        st.stop()

    if not url:

        st.warning("Enter URL")

        st.stop()

    if not (
        "youtube.com" in url
        or
        "youtu.be" in url
    ):

        st.warning("Enter valid YouTube link")

        st.stop()


    # FREE LIMIT

    if not st.session_state.pro:

        if st.session_state.usage >= 3:

            st.warning(
                "Free limit reached. Upgrade to Pro."
            )

            st.stop()

        st.session_state.usage += 1


    st.session_state.processing = True


    # CACHE CHECK

    cache = load_cache(url)

    if cache:

        st.success("⚡ Loaded from cache")

        st.session_state.transcript = cache["transcript"]

        st.session_state.analysis = cache["analysis"]

        st.session_state.loaded = True

        st.session_state.processing = False


    else:

        try:

            with st.spinner("Getting transcript..."):

                transcript = get_transcript(url)


            if not transcript:

                raise Exception(
                    "Could not extract transcript"
                )


            if len(transcript) < 50:

                raise Exception(
                    "Transcript too short"
                )


            with st.spinner("Analyzing video..."):

                analysis = analyze(transcript)


            st.session_state.transcript = transcript

            st.session_state.analysis = analysis

            st.session_state.loaded = True


            save_cache(

                url,

                {

                    "transcript": transcript,

                    "analysis": analysis

                }

            )


            st.success("✅ Analysis complete")


        except Exception as e:

            st.error(str(e))

            st.info(
                "Try another video with captions enabled."
            )

        st.session_state.processing = False


# ---------------- RESULTS ----------------

if st.session_state.loaded:

    tab1,tab2,tab3 = st.tabs([

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


        col1,col2 = st.columns(2)


# TXT DOWNLOAD

        with col1:

            st.download_button(

                "⬇️ Download Notes (TXT)",

                st.session_state.analysis,

                file_name="video_notes.txt"

            )


# PDF DOWNLOAD

        with col2:

            if st.session_state.analysis:

                pdf = export_pdf(

                    "AI Video Notes",

                    st.session_state.analysis

                )


                if pdf:

                    st.download_button(

                        "📄 Download Premium PDF",

                        data=pdf,

                        file_name="video_notes.pdf",

                        mime="application/pdf"

                    )

                else:

                    st.error(
                        "PDF generation failed"
                    )


# -------- TAB 2 --------

    with tab2:

        st.subheader(
            "Ask Questions About Video"
        )

        question = st.text_input(
            "Ask question"
        )


        if st.button("Ask"):

            if not question:

                st.warning(
                    "Enter question"
                )

            else:

                with st.spinner(
                    "Thinking..."
                ):

                    answer = ask_video(

                        question,

                        st.session_state.transcript

                    )

                st.write(answer)


# -------- TAB 3 --------

    with tab3:

        st.subheader("Full Transcript")


        st.text_area(

            "Transcript",

            st.session_state.transcript,

            height=500

        )


        st.download_button(

            "⬇️ Download Transcript",

            st.session_state.transcript,

            file_name="transcript.txt"

        )
