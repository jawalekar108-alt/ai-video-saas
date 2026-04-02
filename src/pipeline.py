from src.transcript import get_transcript
from src.summarizer import summarize

def process_video(url):

    text = get_transcript(url)

    if text == "Transcript unavailable for this video":

        return "No transcript available. Try another video."

    return summarize(text)
