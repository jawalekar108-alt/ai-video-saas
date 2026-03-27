from pydub import AudioSegment
import os

def split_audio(file_path, chunk_length_ms=300000):

    audio = AudioSegment.from_file(file_path)

    os.makedirs("temp", exist_ok=True)

    chunks=[]

    for i,start in enumerate(range(0,len(audio),chunk_length_ms)):

        chunk=audio[start:start+chunk_length_ms]

        path=f"temp/chunk_{i}.mp3"

        chunk.export(

            path,

            format="mp3",

            bitrate="64k"

        )

        chunks.append(path)

    return chunks