import os
from groq import Groq
from config import GROQ_API_KEY

client = Groq(api_key=GROQ_API_KEY)

def transcribe_audio(file):

    if not os.path.exists(file):

        raise Exception("Audio file missing")

    try:

        with open(file,"rb") as audio:

            res = client.audio.transcriptions.create(

                file=audio,

                model="whisper-large-v3"

            )

        return res.text

    except Exception as e:

        print("Transcription error:",e)

        raise Exception("Transcription failed")
