import json
import os

CHECKPOINT="temp/checkpoint.json"

def load_checkpoint():

    if os.path.exists(CHECKPOINT):

        with open(CHECKPOINT,"r") as f:

            return json.load(f)

    return {}

def save_checkpoint(data):

    os.makedirs("temp",exist_ok=True)

    with open(CHECKPOINT,"w") as f:

        json.dump(data,f)

def clear_checkpoint():

    if os.path.exists(CHECKPOINT):

        os.remove(CHECKPOINT)