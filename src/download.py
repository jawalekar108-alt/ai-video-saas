from youtube_transcript_api import YouTubeTranscriptApi
import re

def get_video_id(url):

    regex=r"(?:v=|\/)([0-9A-Za-z_-]{11})"

    match=re.search(regex,url)

    if not match:

        raise Exception("Invalid URL")

    return match.group(1)


def get_youtube_transcript(url):

    video_id=get_video_id(url)

    try:

        transcript_list=YouTubeTranscriptApi.list_transcripts(video_id)

        try:

            transcript=transcript_list.find_transcript(['en'])

        except:

            transcript=transcript_list.find_generated_transcript(['en'])

        data=transcript.fetch()

        text=" ".join(

            x['text']

            for x in data

            if "[" not in x['text']

        )

        return text

    except:

        raise Exception("No captions available")