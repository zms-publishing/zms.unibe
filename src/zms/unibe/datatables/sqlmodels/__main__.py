from zms.unibe.utils.zms2sql import zms2sql
from .ZMSBoris import ZMSBoris
from .ZMSDataTable import ZMSDataTable


def update_datatables(zms_context):
    zms2sql([ZMSDataTable], zms_context)

def update_boris(zms_context):
    zms2sql([ZMSBoris], zms_context)
