from transcript import get_transcript
from summarizer import summarize

def process_video(url):

    text = get_transcript(url)

    summary = summarize(text)

    return summary
