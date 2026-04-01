import re

from youtube_transcript_api import YouTubeTranscriptApi

from src.audio import download_audio

from src.transcribe import transcribe_audio


def extract_video_id(url):

    patterns=[

    r"v=([0-9A-Za-z_-]{11})",

    r"youtu\.be\/([0-9A-Za-z_-]{11})"

    ]

    for p in patterns:

        m=re.search(p,url)

        if m:

            return m.group(1)

    return None


def get_captions(video_id):

    try:

        transcripts=

        YouTubeTranscriptApi.list_transcripts(

        video_id

        )

    except:

        return None


    try:

        t=

        transcripts.find_transcript(

        ['en']

        )

        data=t.fetch()

        return " ".join(

        [x['text'] for x in data]

        )

    except:

        pass


    try:

        t=

        transcripts.find_generated_transcript(

        ['en']

        )

        data=t.fetch()

        return " ".join(

        [x['text'] for x in data]

        )

    except:

        pass


    try:

        for t in transcripts:

            data=t.fetch()

            return " ".join(

            [x['text'] for x in data]

            )

    except:

        pass


    return None


def get_transcript(url):

    video_id=

    extract_video_id(url)

    if not video_id:

        return None


# LAYER 1

    text=

    get_captions(video_id)

    if text and len(text)>100:

        print("Captions used")

        return text


# LAYER 2

    print("No captions → using Whisper")

    audio=

    download_audio(url)

    if audio:

        text=

        transcribe_audio(audio)

        if text:

            return text


# FINAL FAIL SAFE

    return None
