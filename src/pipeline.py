from src.transcript import get_transcript
from src.summarizer import summarize

def process_video(url):

    text = get_transcript(url)

    if text == "Transcript unavailable":

        return """
        Could not extract transcript.

        Try:
        • Videos with captions
        • Educational videos
        • Talks
        """

    return summarize(text)
