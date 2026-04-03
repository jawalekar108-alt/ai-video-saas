import yt_dlp

from src.transcribe import transcribe_audio
from src.summarizer import summarize


def run_pipeline(url):

    try:

        ydl_opts={

            'format':'bestaudio/best',

            'outtmpl':'temp_audio.%(ext)s',

            'noplaylist':True

        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:

            ydl.download([url])

        transcript=transcribe_audio("temp_audio.m4a")

        if transcript is None:

            return {

                "status":"failed",

                "error":"Transcription failed"

            }

        summary=summarize(transcript)

        return {

            "status":"success",

            "transcript":transcript,

            "summary":summary

        }

    except Exception as e:

        return {

            "status":"failed",

            "error":str(e)

        }
