import os

from openai import OpenAI

from config import OPENAI_API_KEY


client=

OpenAI(api_key=

OPENAI_API_KEY)


def transcribe_audio(file):

    if not os.path.exists(file):

        return None

    try:

        audio=open(file,"rb")

        transcript=

        client.audio.transcriptions.create(

        model=

        "gpt-4o-mini-transcribe",

        file=audio

        )

        return transcript.text

    except Exception as e:

        print("Transcription failed",e)

        return None
