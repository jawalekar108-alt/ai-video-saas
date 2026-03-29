import os
import shutil


def cleanup():

    temp="temp"

    if os.path.exists(temp):

        shutil.rmtree(temp)

    os.makedirs(temp,exist_ok=True)
