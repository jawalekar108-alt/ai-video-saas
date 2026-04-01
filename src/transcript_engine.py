import re
import os
import yt_dlp
from youtube_transcript_api import YouTubeTranscriptApi

# OPTIONAL: use Groq or OpenAI
from groq import Groq
from openai import OpenAI


# ---------------- CONFIG ----------------
USE_GROQ = True   # set False to use OpenAI

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# ---------------- EXTRACT VIDEO ID ----------------
def extract_video_id(url):
    match = re.search(r"(?:v=|youtu\.be/)([^&]+)", url)
    return match.group(1) if match else None


# ---------------- STEP 1: TRY YOUTUBE CAPTIONS ----------------
def get_youtube_captions(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return " ".join([t["text"] for t in transcript])
    except:
        return None


# ---------------- STEP 2: DOWNLOAD AUDIO ----------------
def download_audio(url):
    try:
        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": "audio.%(ext)s",
            "quiet": True,
            "noplaylist": True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        return filename
    except Exception as e:
        print("Download error:", e)
        return None


# ---------------- STEP 3: TRANSCRIBE USING AI ----------------
def transcribe_audio(file_path):
    try:
        with open(file_path, "rb") as audio_file:

            if USE_GROQ:
                response = groq_client.audio.transcriptions.create(
                    file=audio_file,
                    model="whisper-large-v3"
                )
                return response.text

            else:
                response = openai_client.audio.transcriptions.create(
                    file=audio_file,
                    model="whisper-1"
                )
                return response.text

    except Exception as e:
        print("Transcription error:", e)
        return None


# ---------------- MAIN FUNCTION ----------------
def get_transcript(url):
    video_id = extract_video_id(url)

    if not video_id:
        return None

    # ✅ Step 1: captions
    captions = get_youtube_captions(video_id)
    if captions:
        print("Using YouTube captions")
        return captions

    print("No captions → using AI transcription")

    # ✅ Step 2: download audio
    audio_file = download_audio(url)
    if not audio_file:
        return None

    # ✅ Step 3: transcribe
    transcript = transcribe_audio(audio_file)

    # cleanup
    try:
        os.remove(audio_file)
    except:
        pass

    return transcript
