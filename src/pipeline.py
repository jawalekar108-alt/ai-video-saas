from src.download import get_youtube_transcript
from src.download_audio import download_audio
from src.transcribe import transcribe_audio

def get_transcript(url):

    try:

        print("Trying captions")

        text=get_youtube_transcript(url)

        if text and len(text)>100:

            return text

    except Exception as e:

        print("Caption failed:",e)

    print("Using AI transcription")

    audio,video_id=download_audio(url)

    transcript=transcribe_audio(audio)

    if not transcript or len(transcript)<100:

        raise Exception("Transcription failed")

    return transcript