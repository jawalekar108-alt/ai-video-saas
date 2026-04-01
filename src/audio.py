import yt_dlp

from pathlib import Path

TEMP="temp"

Path(TEMP).mkdir(exist_ok=True)

def download_audio(url):

    try:

        ydl_opts={

        'format':'bestaudio',

        'outtmpl':'temp/audio.%(ext)s',

        'quiet':True,

        'noplaylist':True,

        'retries':3

        }

        with yt_dlp.YoutubeDL(

        ydl_opts

        ) as ydl:

            info=

            ydl.extract_info(

            url,

            download=True

            )

            return ydl.prepare_filename(info)

    except Exception as e:

        print("Audio fail:",e)

        return None
