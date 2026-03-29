import yt_dlp
import re
from pathlib import Path

TEMP="temp"

Path(TEMP).mkdir(exist_ok=True)


def get_video_id(url):

    regex=r"(?:v=|\/)([0-9A-Za-z_-]{11})"

    match=re.search(regex,url)

    if match:
        return match.group(1)

    return "video"


def download_audio(url):

    video_id=get_video_id(url)

    output=f"{TEMP}/{video_id}.%(ext)s"


    ydl_opts={

        'format':'bestaudio/best',

        'outtmpl':output,

        'quiet':True,

        'noplaylist':True,

        'ignoreerrors':True,

        'retries':1,

        'nocheckcertificate':True,

        'geo_bypass':True,

        'extract_flat':False,

    }


    try:

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:

            info=ydl.extract_info(url,download=True)

            if not info:

                return None,None

            filename=ydl.prepare_filename(info)

            return filename,video_id

    except Exception as e:

        print("Audio download failed:",e)

        return None,None
