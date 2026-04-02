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

        if text and len(text) > 100:
            return text

    except Exception as e:

        print("Transcript API failed:",e)

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

            info=ydl.extract_info(url,download=True)

            file=ydl.prepare_filename(info)

            return file

    except Exception as e:

        print("yt-dlp failed:",e)

        return None


def transcribe(audio_file):

    try:

        with open(audio_file,"rb") as f:

            res=client.audio.transcriptions.create(

                file=f,

                model="whisper-large-v3-turbo"

            )

        return res.text

    except Exception as e:

        print("Whisper failed:",e)

        return None


def get_transcript(url):

    video_id=extract_video_id(url)

    if not video_id:

        return None


    # STEP 1 captions
    text=get_captions(video_id)

    if text:

        print("Using captions")

        return text


    # STEP 2 whisper fallback
    audio=download_audio(url)

    if not audio:

        return None


    text=transcribe(audio)


    try:
        os.remove(audio)
    except:
        pass


    return text
