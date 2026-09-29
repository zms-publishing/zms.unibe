from fastapi import APIRouter, HTTPException
from rq.job import Job
from uuid import UUID

from zms.unibe.fastapi.meta import Tags
from zms.unibe.utils .dependencies import QueueConnDependency, QueueJobsDependency
from zms.unibe.tasks.demo_task import intensive_data_process

router = APIRouter(prefix="/queue", tags=[Tags.redis])


@router.post(
    path="/job", 
    summary="Create a job in Redis Queue (RQ)"
)
def create_job(jobs: QueueJobsDependency, name: str, seconds: int = 5):
    
    job = jobs.enqueue(intensive_data_process, name, seconds)

    return {
        "uuid": job.id,
        "status": "enqueued"
    }


@router.get(
    path="/job/{uuid}",
    summary="Get the status of a job in Redis Queue (RQ)"
)
def get_job_status(queue: QueueConnDependency, uuid: UUID):
    
    try:
        job = Job.fetch(str(uuid), connection=queue)
    except Exception:
        raise HTTPException(status_code=404, detail="Job ID not found")

    return {
        "uuid": job.id,
        "status": job.get_status(),  # queued, started, finished, failed
        "result": job.result         # returns None until the job completes
    }
