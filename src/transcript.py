from src.download import get_youtube_transcript
from src.download_audio import download_audio
from src.transcribe import transcribe_audio
import os


def clean_text(text):

    text=text.replace("\n"," ")

    while "  " in text:
        text=text.replace("  "," ")

    return text.strip()



def get_transcript(url):

    # STEP 1 — captions (PRIMARY METHOD)
    try:

        text=get_youtube_transcript(url)

        if text and len(text)>100:

            print("Using captions")

            return clean_text(text)

    except Exception as e:

        print("Captions failed:",e)



    # STEP 2 — audio (ONLY attempt once)
    try:

        audio,video_id=download_audio(url)

        if audio:

            print("Trying audio transcription")

            transcript=transcribe_audio(audio)

            try:
                os.remove(audio)
            except:
                pass

            if transcript and len(transcript)>100:

                return clean_text(transcript)

    except Exception as e:

        print("Audio blocked:",e)



    # STEP 3 — NEVER CRASH APP
    return """Transcript unavailable.

This video likely blocks AI extraction.

Try:
• Videos with captions
• Educational content
• Talks / podcasts

Or upload transcript manually.
"""
