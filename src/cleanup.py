import glob
import os

def cleanup():

    files=

    glob.glob("temp/*")

    for f in files:

        try:

            os.remove(f)

        except:

            pass
