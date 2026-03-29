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

        'format':'bestaudio/best',

        'outtmpl':output,

        'quiet':True,

        'noplaylist':True,

        'retries':10,

        'fragment_retries':10,

        'socket_timeout':30,

        'nocheckcertificate':True,

        'ignoreerrors':True,

        'allow_unplayable_formats':False,


        # COOKIE FIX (MOST IMPORTANT)
        'cookiefile':'cookies.txt',


        # Browser simulation
        'http_headers':{

            'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',

            'Accept-Language':
            'en-US,en;q=0.9'

        },


        # safest client currently
        'extractor_args':{

            'youtube':{

                'player_client':[

                    'web_creator',
                    'web'

                ]
            }
        },


        'postprocessors':[{

            'key':'FFmpegExtractAudio',

            'preferredcodec':'mp3',

            'preferredquality':'128'

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


    except Exception as e:

        print("Download failed:",e)

        return None,None
