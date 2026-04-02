import re
import os
import yt_dlp
from youtube_transcript_api import YouTubeTranscriptApi
from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def extract_video_id(url):

    match = re.search(r"(?:v=|youtu\.be/)([^&?/]+)", url)

    if not match:
        return None

    return match.group(1)


def get_captions(video_id):

    try:

        api = YouTubeTranscriptApi()

        transcript = api.fetch(video_id)

        text = " ".join([t.text for t in transcript])

        if len(text) > 100:

            return text

    except:

        pass

    return None


def download_audio(url):

    try:

        ydl_opts = {

            "format":"bestaudio/best",

            "outtmpl":"audio.%(ext)s",

            "quiet":True,

            "no_warnings":True,

            "js_runtimes":["node"]

        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:

            info = ydl.extract_info(url,download=True)

            file = ydl.prepare_filename(info)

            return file

    except:

        return None


def transcribe(audio_file):

    try:

        with open(audio_file,"rb") as f:

            res = client.audio.transcriptions.create(

                file=f,

                model="whisper-large-v3-turbo"

            )

        return res.text

    except:

        return None


def get_transcript(url):

    video_id = extract_video_id(url)

    if not video_id:

        return None


    # FAST captions first
    text = get_captions(video_id)

    if text:

        return text


    # Whisper fallback
    audio = download_audio(url)

    if not audio:

        return None


    text = transcribe(audio)


    try:
        os.remove(audio)
    except:
        pass


    return text
