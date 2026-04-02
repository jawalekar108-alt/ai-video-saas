from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
import re

def extract_video_id(url):

    match = re.search(r"(v=|youtu.be/)([^&?/]+)", url)

    if not match:
        raise Exception("Invalid URL")

    return match.group(2)


def get_transcript(url):

    video_id = extract_video_id(url)

    try:

        api = YouTubeTranscriptApi()

        transcript = api.fetch(video_id)

        text = " ".join([t.text for t in transcript])

        return text

    except:

        return "Transcript unavailable for this video"
