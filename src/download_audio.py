import yt_dlp
import os
import re
import subprocess
from pathlib import Path

TEMP="temp"

Path(TEMP).mkdir(exist_ok=True)


# Keep yt-dlp fresh (YouTube changes constantly)
try:
    subprocess.run(
        ["pip","install","-U","yt-dlp"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
except:
    pass


def get_video_id(url):

    regex=r"(?:v=|\/)([0-9A-Za-z_-]{11})"

    match=re.search(regex,url)

    if match:
        return match.group(1)

    return "video"



def download_audio(url):

    video_id=get_video_id(url)

    output=f"{TEMP}/{video_id}.%(ext)s"


    # MAIN CONFIG (stable 2026)
    ydl_opts={

        'format':'bestaudio[protocol=https]/bestaudio/best',

        'outtmpl':output,

        'quiet':True,

        'noplaylist':True,

        'retries':10,

        'fragment_retries':10,

        'socket_timeout':30,

        'ignoreerrors':True,

        'nocheckcertificate':True,

        'allow_unplayable_formats':False,


        # IMPORTANT → looks like real browser
        'http_headers':{

            'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',

            'Accept-Language':
            'en-US,en;q=0.9'

        },


        # IMPORTANT → only stable clients
        'extractor_args':{

            'youtube':{

                'player_client':[

                    'web',
                    'mweb'

                ]
            }
        },


        'source_address':'0.0.0.0',


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

                return fallback_download(url)

            filename=ydl.prepare_filename(info)

            filename=os.path.splitext(filename)[0]+".mp3"

            return filename,video_id


    except Exception:

        return fallback_download(url)



# FALLBACK METHOD
def fallback_download(url):

    video_id=get_video_id(url)

    output=f"{TEMP}/{video_id}.%(ext)s"


    fallback_opts={

        'format':'worstaudio/worst',

        'outtmpl':output,

        'quiet':True,

        'noplaylist':True,

        'ignoreerrors':True,


        'http_headers':{

            'User-Agent':
            'Mozilla/5.0'

        },


        'extractor_args':{

            'youtube':{

                'player_client':['web']

            }
        },


        'postprocessors':[{

            'key':'FFmpegExtractAudio',

            'preferredcodec':'mp3',

            'preferredquality':'96'

        }]

    }


    try:

        with yt_dlp.YoutubeDL(fallback_opts) as ydl:

            info=ydl.extract_info(url,download=True)

            if not info:
                return None,None

            filename=ydl.prepare_filename(info)

            filename=os.path.splitext(filename)[0]+".mp3"

            return filename,video_id

    except:

        return None,None
