import re

from youtube_transcript_api import YouTubeTranscriptApi


def extract_video_id(url):

    patterns=[

        r"v=([0-9A-Za-z_-]{11})",

        r"youtu\.be\/([0-9A-Za-z_-]{11})"

    ]

    for p in patterns:

        match=re.search(p,url)

        if match:
            return match.group(1)

    return None



def clean(text):

    text=text.replace("\n"," ")

    while "  " in text:

        text=text.replace("  "," ")

    return text.strip()



def get_transcript(url):

    video_id=extract_video_id(url)

    if not video_id:
        return None

    try:

        data=YouTubeTranscriptApi.get_transcript(video_id)

        text=" ".join([x['text'] for x in data])

        return clean(text)

    except Exception as e:

        print("Transcript error:",e)

        return None
