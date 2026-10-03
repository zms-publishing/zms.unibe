# $ rq cron cron_config.py
# https://python-rq.org/docs/cron/
# https://python-rq.org/docs/jobs/

from rq.cron import register
from zms.unibe.tasks.demo import intensive_data_process


register(
    intensive_data_process,
    queue_name='maintenance',
    interval=1800  # 30 minutes in seconds
)

register(
    intensive_data_process,
    queue_name='reports',
    args=('daily_metrics',),
    #kwargs={'format': 'json', 'recipients': ['bob@example.com']},
    interval=21600  # 6 hours in seconds
)

register(
    intensive_data_process,
    queue_name='cron',
    name="hourly_status",
    cron="1/5 * * * *"  # every 5 minutes from :01 through :59
)
