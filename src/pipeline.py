from src.download import get_youtube_transcript
from src.download_audio import download_audio
from src.transcribe import transcribe_audio

def get_transcript(url):

    # Try captions first
    try:

        text=get_youtube_transcript(url)

        if text and len(text)>100:

            return text

    except Exception as e:

        print("Caption failed:",e)

    # Try audio download
    try:

        audio,video_id=download_audio(url)

        if audio:

            transcript=transcribe_audio(audio)

            if transcript and len(transcript)>100:

                return transcript

    except Exception as e:

        print("Audio failed:",e)

    # Final fallback
    raise Exception(
        "This video cannot be processed.\n"
        "Possible reasons:\n"
        "- DRM protection\n"
        "- Bot protection\n"
        "- No captions available\n"
        "- Private video"
    )
