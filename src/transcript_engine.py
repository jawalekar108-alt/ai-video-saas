import re
import os
import yt_dlp
from youtube_transcript_api import YouTubeTranscriptApi
from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def extract_video_id(url):
    match = re.search(r"(?:v=|youtu\.be/)([^&]+)", url)
    return match.group(1) if match else None


def get_captions(video_id):
    try:
        data = YouTubeTranscriptApi.get_transcript(video_id)
        return " ".join([x["text"] for x in data])
    except:
        return None


def download_audio(url):
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": "audio.%(ext)s",
        "quiet": True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info)


def transcribe(file):
    with open(file, "rb") as f:
        res = client.audio.transcriptions.create(
            file=f,
            model="whisper-large-v3"
        )
    return res.text


def get_transcript(url):
    video_id = extract_video_id(url)
    if not video_id:
        return None

    # ✅ captions first
    captions = get_captions(video_id)
    if captions:
        return captions

    # 🤖 fallback
    audio = download_audio(url)
    if not audio:
        return None

    text = transcribe(audio)

    try:
        os.remove(audio)
    except:
        pass

    return text
