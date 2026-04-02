import re
import os
import yt_dlp
from youtube_transcript_api import YouTubeTranscriptApi
from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def extract_video_id(url):

    match = re.search(r"(?:v=|youtu\.be/)([^&?/]+)", url)

    return match.group(1) if match else None


# FAST METHOD (preferred)
def get_captions(video_id):

    try:

        api = YouTubeTranscriptApi()

        transcript = api.fetch(video_id)

        text = " ".join([t.text for t in transcript])

        if len(text) > 50:
            return text

    except:
        pass

    return None


# FALLBACK METHOD
def download_audio(url):

    try:

        ydl_opts = {

            "format": "bestaudio/best",

            "outtmpl": "audio.%(ext)s",

            "quiet": True,

            "no_warnings": True,

            "js_runtimes": ["node"]

        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:

            info = ydl.extract_info(url, download=True)

            return ydl.prepare_filename(info)

    except:

        return None


# AI TRANSCRIPTION FALLBACK
def transcribe(file):

    try:

        with open(file,"rb") as f:

            res = client.audio.transcriptions.create(

                file=f,

                model="whisper-large-v3",

                response_format="text"

            )

        return res

    except:

        return None


# MAIN PIPELINE
def get_transcript(url):

    video_id = extract_video_id(url)

    if not video_id:
        return "Invalid YouTube URL"


    # STEP 1 (FAST)
    captions = get_captions(video_id)

    if captions:
        return captions


    # STEP 2 (FALLBACK)
    audio = download_audio(url)

    if not audio:
        return "Transcript unavailable"


    text = transcribe(audio)


    # CLEANUP
    try:
        os.remove(audio)
    except:
        pass


    if not text:
        return "Transcript unavailable"


    return text
