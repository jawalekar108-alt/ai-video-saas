from youtube_transcript_api import YouTubeTranscriptApi

from youtube_transcript_api._errors import *

from src.utils import get_video_id


def get_transcript(url):

    try:

        video_id=get_video_id(url)

        if not video_id:

            return None

        transcript=YouTubeTranscriptApi.get_transcript(

            video_id,

            languages=['en','hi']

        )

        text=" ".join(

            [t["text"] for t in transcript]

        )

        return text


    except TranscriptsDisabled:

        return "No captions available"


    except NoTranscriptFound:

        return "Transcript not found"


    except Exception:

        return None
