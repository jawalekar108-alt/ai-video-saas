import yt_dlp

import os

from pathlib import Path


TEMP="temp"

Path(TEMP).mkdir(

exist_ok=True

)


def download_audio(url):

    try:

        output=

        f"{TEMP}/audio.%(ext)s"

        ydl_opts={

        'format':'bestaudio/best',

        'outtmpl':output,

        'quiet':True,

        'noplaylist':True

        }

        with yt_dlp.YoutubeDL(

        ydl_opts

        ) as ydl:

            info=

            ydl.extract_info(

            url,

            download=True

            )

            filename=

            ydl.prepare_filename(info)

            return filename

    except Exception as e:

        print("Download failed",e)

        return None
