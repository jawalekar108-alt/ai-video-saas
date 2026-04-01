import uuid

from src.transcript_engine import get_transcript

from src.analyzer import analyze

from src.job_store import create_job

from src.job_store import finish_job

from src.job_store import fail_job


def process_video(url):

    job_id = str(uuid.uuid4())

    create_job(job_id)

    try:

        transcript = get_transcript(url)

        if not transcript:

            fail_job(job_id)

            return job_id


        notes = analyze(transcript)

        finish_job(

            job_id,

            {

                "transcript": transcript,

                "analysis": notes

            }

        )

    except Exception:

        fail_job(job_id)

    return job_id
