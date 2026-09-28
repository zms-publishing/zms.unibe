from fastapi import APIRouter, HTTPException
from rq.job import Job
from uuid import UUID

from zms.unibe.fastapi.meta import Tags

router = APIRouter(prefix="/rq", tags=[Tags.queue])


def intensive_data_process(task_name: str, duration: int):
    """Simulates a heavy, time-consuming background task."""
    import time
    
    print(f"Starting task: {task_name}")
    time.sleep(duration) 
    print(f"Finished task: {task_name}")
    return f"Result: {task_name} completed successfully after {duration}s!"


@router.post(
    path="/job", 
    summary="Create a job in Redis Queue (RQ)"
)
def create_job(name: str, seconds: int = 5):
    from app.main import RQ_JOBS
    
    job = RQ_JOBS.enqueue(intensive_data_process, name, seconds)

    return {
        "uuid": job.id,
        "status": "enqueued"
    }


@router.get(
    path="/job/{uuid}",
    summary="Get the status of a job in Redis Queue (RQ)"
)
def get_job_status(uuid: UUID):
    from app.main import REDIS_CONN
    
    try:
        job = Job.fetch(str(uuid), connection=REDIS_CONN)
    except Exception:
        raise HTTPException(status_code=404, detail="Job ID not found")

    return {
        "uuid": job.id,
        "status": job.get_status(),  # queued, started, finished, failed
        "result": job.result         # returns None until the job completes
    }
