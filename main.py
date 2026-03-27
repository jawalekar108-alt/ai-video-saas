from src.download import download_audio
from src.splitter import split_audio
from src.transcribe import transcribe_chunks
from src.summarize import summarize_text, extract_highlights

url = input("Enter YouTube URL: ")

print("Downloading audio...")
audio = download_audio(url)

print("Splitting audio...")
chunks = split_audio(audio)

print("Transcribing...")
transcript, segments = transcribe_chunks(chunks)

print("Analyzing content...")
summary = summarize_text(transcript)

print("Extracting highlights...")
highlights = extract_highlights(segments)

print("\n====== FINAL SUMMARY ======\n")

print(summary)

print("\n====== KEY MOMENTS ======\n")

for h in highlights:

    print(h)