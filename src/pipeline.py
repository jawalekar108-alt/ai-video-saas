from src.transcript_engine import get_transcript
from src.analyzer import analyze


def run_pipeline(url):
    try:
        transcript = get_transcript(url)

        if not transcript:
            return {
                "status": "failed",
                "error": "No transcript available"
            }

        summary = analyze(transcript)

        return {
            "status": "done",
            "transcript": transcript,
            "summary": summary
        }

    except Exception as e:
        return {
            "status": "failed",
            "error": str(e)
        }
