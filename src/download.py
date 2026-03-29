from youtube_transcript_api import YouTubeTranscriptApi
import re


def extract_video_id(url):

    regex=r"(?:v=|\/)([0-9A-Za-z_-]{11})"

    match=re.search(regex,url)

    if match:
        return match.group(1)

    raise Exception("Invalid URL")



def get_youtube_transcript(url):

    video_id=extract_video_id(url)

    transcript_list=YouTubeTranscriptApi.list_transcripts(video_id)


    # Try English first
    try:

        transcript=transcript_list.find_transcript(['en'])

        data=transcript.fetch()

        return " ".join([x['text'] for x in data])

    except:
        pass


    # Try auto English
    try:

        transcript=transcript_list.find_generated_transcript(['en'])

        data=transcript.fetch()

        return " ".join([x['text'] for x in data])

    except:
        pass


    # Try ANY language
    try:

        for t in transcript_list:

            data=t.fetch()

            return " ".join([x['text'] for x in data])

    except:
        pass


    raise Exception("No captions available")
