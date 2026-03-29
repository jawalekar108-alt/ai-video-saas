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

    # STEP 1 captions
    try:

        text=get_youtube_transcript(url)

        if text and len(text)>100:

            return clean_text(text)

    except Exception as e:

        print("Captions failed:",e)


    # STEP 2 audio attempt
    try:

        audio,video_id=download_audio(url)

        if audio:

            transcript=transcribe_audio(audio)

            try:
                os.remove(audio)
            except:
                pass

            if transcript:

                return clean_text(transcript)

    except Exception as e:

        print("Audio skipped:",e)


    # STEP 3 graceful fallback
    return None
