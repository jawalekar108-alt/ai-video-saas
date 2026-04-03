from src.pipeline import run_pipeline

url="https://youtube.com/watch?v=dQw4w9WgXcQ"

result=run_pipeline(url)

print(result["summary"])
