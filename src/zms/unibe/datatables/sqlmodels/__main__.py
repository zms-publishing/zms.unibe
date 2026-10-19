from .ZMSBoris import ZMSBoris
from .ZMSDataTable import ZMSDataTable
from ...utils.zms2sql import zms2sql


def update_datatables(zms_context):
    zms2sql([ZMSDataTable], zms_context)

def update_boris(zms_context):
    zms2sql([ZMSBoris], zms_context)
