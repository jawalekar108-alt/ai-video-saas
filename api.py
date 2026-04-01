from fastapi import FastAPI

from worker import process_video

from src.job_store import get_job


app = FastAPI()


@app.get("/process")

def process(url: str):

    job_id = process_video(url)

    return {"job_id": job_id}


@app.get("/status")

def status(job_id: str):

    job = get_job(job_id)

    if not job:

        return {"status": "failed"}

    return job
