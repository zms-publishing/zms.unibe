from .ZMSFormulator import ZMSFormulator
from ...utils.zms2sql import zms2sql


def update_formulator(zms_context):
    zms2sql([ZMSFormulator], zms_context)
