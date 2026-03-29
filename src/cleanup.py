import os
import shutil


def cleanup():

    temp_dir="temp"

    try:

        if os.path.exists(temp_dir):

            shutil.rmtree(temp_dir)

        os.makedirs(temp_dir,exist_ok=True)

    except Exception as e:

        print("Cleanup warning:",e)
