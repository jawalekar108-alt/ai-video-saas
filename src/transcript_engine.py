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


def captions(video_id):

    try:

        transcripts=

        YouTubeTranscriptApi.list_transcripts(

        video_id

        )

    except:

        return None


# manual english

    try:

        t=transcripts.find_transcript(['en'])

        data=t.fetch()

        return " ".join(

        [x['text'] for x in data]

        )

    except:

        pass


# auto english

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


# any language fallback

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


# LAYER 1 CAPTIONS

    text=captions(video_id)

    if text and len(text)>100:

        print("Using captions")

        return text


# LAYER 2 AUDIO

    try:

        print("Downloading audio")

        audio=

        download_audio(url)

        if audio:

            print("Transcribing audio")

            text=

            transcribe_audio(audio)

            if text:

                return text

    except Exception as e:

        print("Audio fallback failed",e)


    return None
