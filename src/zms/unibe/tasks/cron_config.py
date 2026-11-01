# $ rq cron zms.unibe.tasks.cron_config --url "$REDIS_URL"
# https://python-rq.org/docs/cron/
# https://python-rq.org/docs/jobs/
# Set TZ to the timezone previously used by system cron.

from rq.cron import register as register_cron

from zms.unibe.tasks.task_config import register as run_task

register_cron(
    run_task,
    queue_name='default',
    args=('afterwork',),
    name='afterwork',
    cron='5 18 * * 1-5',
    job_timeout=3600,
)

register_cron(
    run_task,
    queue_name='default',
    args=('officehours',),
    name='officehours',
    cron='50 7-17/2 * * 1-5',
    job_timeout=3600,
)

register_cron(
    run_task,
    queue_name='default',
    args=('weekly',),
    name='weekly',
    cron='5 8 * * 6',
    job_timeout=10800,
)
