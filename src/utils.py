import shutil
import os

def cleanup():

    if os.path.exists("temp"):

        shutil.rmtree("temp")

    os.makedirs("temp",exist_ok=True)