import os
import glob

def clean_temp():

    files=glob.glob("temp/*.mp3")

    for f in files:

        os.remove(f)