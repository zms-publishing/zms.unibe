# $ rq worker default --with-scheduler
# https://python-rq.org/docs/workers/
# https://python-rq.org/docs/scheduling/


def register(task: str, *args, **kwargs):
    
    match task:
        case "intensive_data_process":
            from zms.unibe.tasks.demo import intensive_data_process
            return intensive_data_process(*args, **kwargs)
        case _:
            raise ValueError(f"Unknown task: {task}")
