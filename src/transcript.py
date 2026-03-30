from youtube_transcript_api import YouTubeTranscriptApi
import re


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

        transcripts=YouTubeTranscriptApi.list_transcripts(video_id)


        # English captions
        try:

            t=transcripts.find_transcript(['en'])

            data=t.fetch()

            text=" ".join([x['text'] for x in data])

            return clean(text)

        except:
            pass


        # Auto captions
        try:

            t=transcripts.find_generated_transcript(['en'])

            data=t.fetch()

            text=" ".join([x['text'] for x in data])

            return clean(text)

        except:
            pass


        # Any language
        for t in transcripts:

            data=t.fetch()

            text=" ".join([x['text'] for x in data])

            return clean(text)


    except Exception as e:

        print("Transcript error:",e)


    return None



# from src.download import get_youtube_transcript


# def clean_text(text):

#     text=text.replace("\n"," ")

#     while "  " in text:
#         text=text.replace("  "," ")

#     return text.strip()



# def get_transcript(url):

#     try:

#         text=get_youtube_transcript(url)

#         if text and len(text)>100:

#             print("Using captions")

#             return clean_text(text)

#     except Exception as e:

#         print("Captions failed:",e)


#     # NEVER attempt audio in cloud SaaS

#     return """Transcript unavailable.

# This video blocks transcript extraction.

# Try:
# • Videos with captions enabled
# • Educational videos
# • Podcasts
# • Lectures

# This happens because some videos disable AI access.
# """
 
