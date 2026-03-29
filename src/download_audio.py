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

        'format':'worstaudio/worst',

        'quiet':True,

        'noplaylist':True,

        'outtmpl':output,

        'retries':3,

        'ignoreerrors':True,

        # safer client
        'extractor_args':{

            'youtube':{

                'player_client':['web']

            }
        },

        # browser disguise
        'http_headers':{

            'User-Agent':'Mozilla/5.0'

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
