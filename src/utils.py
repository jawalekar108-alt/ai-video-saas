import os
import shutil


def cleanup_temp():

    if os.path.exists("temp"):

        shutil.rmtree("temp")

    os.makedirs("temp",exist_ok=True)
