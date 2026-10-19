from .UniaktuellArticle import UniaktuellArticle
from ...utils.zms2sql import zms2sql


def update_uniaktuell(zms_context):
    zms2sql([UniaktuellArticle], zms_context)
