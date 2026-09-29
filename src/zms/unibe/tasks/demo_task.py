# demo_task.py

def intensive_data_process(job_name: str, duration: int):
    """Simulates a heavy, time-consuming background job."""
    import time

    print(f"Starting job: {job_name}")
    time.sleep(duration)
    print(f"Finished job: {job_name}")
    return f"Result: {job_name} completed successfully after {duration}s!"
