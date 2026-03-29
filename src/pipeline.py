from src.download import get_youtube_transcript
from src.download_audio import download_audio
from src.transcribe import transcribe_audio

def get_transcript(url):

    try:

        text=get_youtube_transcript(url)

        if text and len(text)>100:

            return text

    except:

        pass

    try:

        audio,video_id=download_audio(url)

        if audio:

            transcript=transcribe_audio(audio)

            if transcript:

                return transcript

    except:

        pass

    raise Exception("Could not extract transcript (video may be protected)")
