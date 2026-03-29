import yt_dlp
import os
import re

TEMP="temp"

os.makedirs(TEMP,exist_ok=True)

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

        'format':'bestaudio',

        'outtmpl':output,

        'quiet':True,

        'noplaylist':True,

        'nocheckcertificate':True,

        'ignoreerrors':False,

        'retries':10,

        'fragment_retries':10,

        'extractor_args':{

            'youtube':{

                'player_client':['web']

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

            filename=ydl.prepare_filename(info)

            filename=os.path.splitext(filename)[0]+".mp3"

        return filename,video_id

    except Exception as e:

        print("Download error:",e)

        raise Exception("Download failed")
