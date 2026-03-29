import yt_dlp
import os
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

    'format':'bestaudio[ext=m4a]/bestaudio/best',

    'quiet':True,

    'noplaylist':True,

    'retries':5,

    'nocheckcertificate':True,

    'ignoreerrors':True,

    'geo_bypass':True,

    'outtmpl':output,

    'extractor_args':{

        'youtube':{

            'player_client':['web'],

            'skip':['dash','hls']

        }

    },

    'http_headers':{

        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',

        'Accept-Language':'en-US,en'

    },

    'postprocessors':[{

        'key':'FFmpegExtractAudio',

        'preferredcodec':'mp3'

    }]

}

    try:

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:

            info=ydl.extract_info(url,download=True)

            if not info:
                return None,None

            filename=ydl.prepare_filename(info)

            filename=os.path.splitext(filename)[0]+".mp3"

            return filename,video_id

    except:

        return None,None
