import os
import json
import hashlib

CACHE="cache"

os.makedirs(CACHE,exist_ok=True)

def key(url):

    return hashlib.md5(url.encode()).hexdigest()


def load_cache(url):

    path=f"{CACHE}/{key(url)}.json"

    if os.path.exists(path):

        try:

            with open(path,"r",encoding="utf-8") as f:

                return json.load(f)

        except:

            return None

    return None


def save_cache(url,data):

    path=f"{CACHE}/{key(url)}.json"

    try:

        with open(path,"w",encoding="utf-8") as f:

            json.dump(data,f,indent=2)

    except:

        print("Cache save failed")