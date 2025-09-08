from zms.unibe.utils.db import zms2sql
from .ZMSBoris import ZMSBoris
from .ZMSDataTable import ZMSDataTable


def update_datatables(zms_context):
    zms2sql([ZMSDataTable, ZMSBoris], zms_context)
