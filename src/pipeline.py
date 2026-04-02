from src.transcript_engine import get_transcript
from src.gemini_client import gemini_summary
from src.groq_client import groq_summary

def process_video(url):

    text = get_transcript(url)

    if not text:

        return "Could not extract transcript from this video."

    if len(text) < 200:

        return "Transcript too short."

    try:

        return gemini_summary(text)

    except:

        return groq_summary(text)
