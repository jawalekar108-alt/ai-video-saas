from faster_whisper import WhisperModel

model = None

def load_model():

    global model

    if model is None:

        model = WhisperModel(
            "base",
            device="cpu",
            compute_type="int8"
        )

    return model


def transcribe_audio(file):

    try:

        model = load_model()

        segments, info = model.transcribe(file)

        text=""

        for segment in segments:

            text += segment.text + " "

        return text

    except Exception as e:

        print("Transcription failed:",e)

        return None
