import os

import glob


def cleanup():

    files=

    glob.glob(

    "temp/*"

    )

    for f in files:

        try:

            os.remove(f)

        except:

            pass
