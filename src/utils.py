import re

def get_video_id(url):

    patterns = [

        r"v=([^&]+)",

        r"youtu.be/([^?]+)",

        r"shorts/([^?]+)"

    ]

    for p in patterns:

        match=re.search(p,url)

        if match:

            return match.group(1)

    return None
