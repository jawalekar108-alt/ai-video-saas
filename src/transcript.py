from src.download import get_youtube_transcript
from src.download_audio import download_audio
from src.transcribe import transcribe_audio
import os


def get_transcript(url):

    try:

        text=get_youtube_transcript(url)

        if text and len(text)>100:

            return text

    except Exception as e:

        print("Caption failed:",e)


    try:

        audio,video_id=download_audio(url)

        if audio:

            transcript=transcribe_audio(audio)

            # cleanup temp file
            try:
                os.remove(audio)
            except:
                pass

            if transcript and len(transcript)>100:

                return transcript

    except Exception as e:

        print("Audio failed:",e)


    raise Exception(

        "This video cannot be processed.\n"
        "Possible reasons:\n"
        "- DRM protection\n"
        "- Bot protection\n"
        "- No captions\n"
        "- Private video"

    )
