import pytz
import time
from datetime import datetime
from Products.zms import standard

def local_timezone(dt=None):
    if dt is None:
        dt = datetime.now()
    if isinstance(dt, time.struct_time):
        dt = standard.format_datetime_iso(dt)
    if isinstance(dt, str):
        dt = datetime.fromisoformat(dt)
    return dt.astimezone(pytz.timezone('Europe/Zurich'))
