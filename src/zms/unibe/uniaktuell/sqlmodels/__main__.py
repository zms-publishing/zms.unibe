from zms.unibe.utils.zms2sql.zms2sql import zms2sql
from .UniaktuellArticle import UniaktuellArticle


def update_uniaktuell(zms_context):
    zms2sql([UniaktuellArticle], zms_context)
