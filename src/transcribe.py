import whisper
import os

model=None

def load_model():

    global model

    if model is None:

        model=whisper.load_model("base")

    return model


def transcribe_audio(file):

    if not os.path.exists(file):

        return None

    try:

        model=load_model()

        result=model.transcribe(

        file,

        fp16=False

        )

        return result["text"]

    except Exception as e:

        print("Whisper failed:",e)

        return None
