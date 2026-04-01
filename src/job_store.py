jobs = {}

def create_job(job_id):

    jobs[job_id] = {

        "status":"processing",

        "result":None

    }


def finish_job(job_id,data):

    jobs[job_id]["status"]="done"

    jobs[job_id]["result"]=data


def fail_job(job_id):

    jobs[job_id]["status"]="failed"


def get_job(job_id):

    return jobs.get(job_id)
