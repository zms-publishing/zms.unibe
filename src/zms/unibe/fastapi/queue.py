from fastapi import APIRouter, HTTPException
from uuid import UUID
from datetime import datetime, timedelta

from zms.unibe.utils.helpers import local_timezone
from zms.unibe.fastapi.meta import Tags
from zms.unibe.utils.dependencies import QueueDependency
from zms.unibe.tasks.task_config import register

router = APIRouter(prefix="/queue", tags=[Tags.redis])


@router.post(
    path="/job",
    summary="Create a job in Redis Queue (RQ)"
)
def create_job(
        queue: QueueDependency,
        task: str = 'intensive_data_process',
        in_seconds: int = 0,
        at_datetime: datetime | None = None,
        at_front: bool = False,
        params: dict | None = {'job_name': 'Demo', 'job_duration': 5},
):
    # https://github.com/rq/rq#scheduling-jobs
    _in = timedelta(seconds=in_seconds)
    _at = local_timezone(at_datetime)
    now = local_timezone()
    
    if in_seconds > 0:
        job = queue.enqueue_in(
            _in,
            register,
            task,
            **params if params else {},
            at_front=at_front,
        )
        dt = local_timezone(now + _in)
    elif at_datetime:
        if _at <= now:
            raise HTTPException(
                status_code=400,
                detail="Execution time must be in the future."
            )
        job = queue.enqueue_at(
            _at,
            register,
            task,
            **params if params else {},
            at_front=at_front,
        )
        dt = _at
    else:
        job = queue.enqueue(
            register, 
            task,
            **params if params else {},
            at_front=at_front,
        )
        dt = now

    return {
        "job_id": job.id,
        "status": job.get_status(),
        "scheduled_for": dt.isoformat()
    }


@router.get(
    path="/job/{uuid}",
    summary="Get the status of a job in Redis Queue (RQ)"
)
def get_job_status(
        queue: QueueDependency,
        uuid: UUID
):
    job = queue.fetch_job(str(uuid))
    
    if job:
        return {
            "job_id": job.id,
            "status": job.get_status(),
            "enqueued_at_front": job.enqueue_at_front,
            "enqueued_at": job.enqueued_at,
            "started_at": job.started_at,
            "ended_at": job.ended_at,
            "result": job.return_value(),
        }
    
    raise HTTPException(
        status_code=404,
        detail="Job ID not found."
    )


@router.delete(
    path="/job/{uuid}",
    summary="Cancel a scheduled or running job in Redis Queue (RQ)",
)
def cancel_job(
        jobs: QueueDependency,
        uuid: UUID,
):
    job = jobs.fetch_job(str(uuid))

    if job:
        try:
            job.cancel()
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=str(e)
            )

        return {
            "message": f"Job {uuid} has been cancelled."
        }

    raise HTTPException(
        status_code=404,
        detail="Job ID not found."
    )
