from zms.unibe.utils.zms2sql import zms2sql
from .ZMSFormulator import ZMSFormulator


def update_formulator(zms_context):
    zms2sql([ZMSFormulator], zms_context)
