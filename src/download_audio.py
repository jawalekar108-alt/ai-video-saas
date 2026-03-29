import yt_dlp
import os
import re
import subprocess
from pathlib import Path

TEMP="temp"

Path(TEMP).mkdir(exist_ok=True)


# keep yt-dlp updated (important for youtube changes)
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


    ydl_opts={

        # safer audio selection
        
        'format':'bestaudio[protocol=https]/bestaudio/best',

        'outtmpl':output,

        'quiet':True,

        'noplaylist':True,

        'nocheckcertificate':True,

        'ignoreerrors':True,

        'retries':10,

        'fragment_retries':10,

        'socket_timeout':30,

        # avoid DRM formats
        'allow_unplayable_formats':False,

        'http_headers':{
        'User-Agent':'Mozilla/5.0'
    },
        
        # huge reliability improvement
        'extractor_args':{

            'youtube':{

                'player_client':
                ['web']
            }
        },

        # sometimes fixes cloud networking bugs
        'source_address':'0.0.0.0',

        # convert to mp3
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


    except yt_dlp.utils.DownloadError:

        return fallback_download(url)

    except Exception:

        return fallback_download(url)



def fallback_download(url):

    video_id=get_video_id(url)

    output=f"{TEMP}/{video_id}.%(ext)s"


    fallback_opts={

        'format':'best',

        'outtmpl':output,

        'quiet':True,

        'noplaylist':True,

        'extractor_args':{

            'youtube':{

                'player_client':['android']

            }
        },

        'postprocessors':[{

            'key':'FFmpegExtractAudio',

            'preferredcodec':'mp3',

            'preferredquality':'128'

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
