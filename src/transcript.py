from src.download import get_youtube_transcript
from src.download_audio import download_audio
from src.transcribe import transcribe_audio
import os


def get_transcript(url):

    # STEP 1 — captions (primary method)
    try:

        text=get_youtube_transcript(url)

        if text and len(text)>100:

            print("Using YouTube captions")

            return text

    except Exception as e:

        print("Captions unavailable:",e)


    # STEP 2 — try audio (best effort only)
    try:

        audio,video_id=download_audio(url)

        if audio:

            print("Using audio transcription")

            transcript=transcribe_audio(audio)

            try:
                os.remove(audio)
            except:
                pass

            if transcript and len(transcript)>100:

                return transcript

    except Exception as e:

        print("Audio blocked:",e)


    # STEP 3 — graceful failure (important UX)

    raise Exception(

        "Could not process this video.\n\n"
        "Try:\n"
        "• Videos with captions enabled\n"
        "• Educational videos\n"
        "• Public lectures\n"
        "• Avoid music videos\n"
        "• Avoid Shorts"

    )
