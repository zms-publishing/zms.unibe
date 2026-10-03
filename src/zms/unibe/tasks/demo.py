# zms.unibe.tasks.demo

def intensive_data_process(job_name: str = 'job_name', job_duration: int = 10) -> str:
    """Simulates a heavy, time-consuming background job."""
    import time

    from rq import get_current_job
    job = get_current_job()
    if job:
        job.meta['progress'] = "Progress info..."
        job.meta['foobar'] = "more..."
        job.save_meta()  # show dict in the RQ dashboard detail view

    print(f"Starting job: {job_name}")
    time.sleep(job_duration)
    print(f"Finished job: {job_name}")
    return f"Result: {job_name} completed successfully after {job_duration}s!"
