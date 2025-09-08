from zms.unibe.utils.db import zms2sql
from .UniaktuellArticle import UniaktuellArticle


def update_uniaktuell(zms_context):
    zms2sql([UniaktuellArticle], zms_context)
