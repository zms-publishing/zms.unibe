# $ rq worker default --url "$REDIS_URL"
# https://python-rq.org/docs/workers/
# https://python-rq.org/docs/scheduling/

import logging

LOGGER = logging.getLogger(__name__)

SCHEDULED_TASKS = {
    'weekly': (
        'update-zmsobjects',
        'update-datatables',
        'update-formulator',
        'update-contacts',
        'update-layouts',
    ),
    'officehours': (
        'fetch-agendas',
        'fetch-statusmessages',
        'update-zmssites',
        'update-teasers',
        'update-agendas',
        'update-newsevents',
    ),
    'afterwork': (
        'update-servicelinks',
        'update-medianews',
        'update-uniaktuell',
        'update-newsboxes',
        'update-newsevents',
    ),
}


def register(task: str, *args, **kwargs):
    match task:
        case "intensive_data_process":
            from .demo import intensive_data_process
            return intensive_data_process(*args, **kwargs)
        case _ if task in SCHEDULED_TASKS:
            from ..utils.zms2sql.cli import run_command

            failures = []
            for command in SCHEDULED_TASKS[task]:
                try:
                    run_command(command)
                except Exception as error:
                    LOGGER.exception("Scheduled command %s failed", command)
                    failures.append((command, error))
            if failures:
                failed_commands = ', '.join(command for command, _ in failures)
                raise RuntimeError(
                    f"Scheduled task {task} failed commands: {failed_commands}"
                ) from failures[0][1]
        case _:
            raise ValueError(f"Unknown task: {task}")
