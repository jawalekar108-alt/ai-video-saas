from groq import Groq
from config import GROQ_API_KEY
from src.split_audio import split_audio
from src.checkpoint import load_checkpoint,save_checkpoint
import time
import os

client=Groq(api_key=GROQ_API_KEY)

def transcribe_audio(file_path):

    chunks=split_audio(file_path)

    checkpoint=load_checkpoint()

    full_text=[]

    print("Total chunks:",len(chunks))

    # initial cooldown (prevents first block)
    time.sleep(8)

    for i,chunk in enumerate(chunks):

        if str(i) in checkpoint:

            print("Skipping completed:",i)

            full_text.append(checkpoint[str(i)])

            continue

        retry=0

        while retry<5:

            try:

                size=os.path.getsize(chunk)/1024/1024

                print("Chunk",i,"size:",round(size,2),"MB")

                if size>24:

                    print("Chunk too large skip")

                    break

                print("Processing chunk",i+1,"/",len(chunks))

                with open(chunk,"rb") as f:

                    res=client.audio.transcriptions.create(

                        file=f,

                        model="whisper-large-v3"

                    )

                text=res.text

                full_text.append(text)

                checkpoint[str(i)]=text

                save_checkpoint(checkpoint)

                # PRODUCTION RATE LIMITER
                wait=25

                print("Cooling:",wait,"sec")

                time.sleep(wait)

                break

            except Exception as e:

                retry+=1

                wait=retry*45

                print("Retry",retry)

                print("Waiting:",wait)

                time.sleep(wait)

                if retry==5:

                    print("Failed chunk skipping")

                    full_text.append("")

    return " ".join(full_text)