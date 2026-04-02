import re
from youtube_transcript_api import YouTubeTranscriptApi
import yt_dlp

def extract_video_id(url):

    match = re.search(r"(v=|youtu.be/)([^&?/]+)", url)

    if not match:
        raise Exception("Invalid URL")

    return match.group(2)


def get_youtube_transcript(video_id):

    try:

        api = YouTubeTranscriptApi()

        transcript = api.fetch(video_id)

        text = " ".join([t.text for t in transcript])

        return text

    except:

        return None


def get_yt_dlp_captions(url):

    try:

        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'skip_download': True,
            'writesubtitles': True,
            'writeautomaticsub': True,
            'subtitlesformat': 'vtt',
            'js_runtimes': ['node']
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:

            info = ydl.extract_info(url, download=False)

            if 'subtitles' in info:

                for lang in info['subtitles']:

                    subs = info['subtitles'][lang]

                    if subs:

                        return "Captions available but extraction limited"

        return None

    except:

        return None


def get_transcript(url):

    video_id = extract_video_id(url)

    text = get_youtube_transcript(video_id)

    if text:
        return text

    text = get_yt_dlp_captions(url)

    if text:
        return text

    return "Transcript unavailable"
