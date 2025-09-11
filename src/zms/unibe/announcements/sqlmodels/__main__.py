from zms.unibe.utils.zms2sql import zms2sql
from .MediaNews import MediaNews
from .NewsBox import NewsBox
from .NewsContainer import NewsContainer


def update_newsboxes(zms_context):
    zms2sql([NewsContainer, NewsBox], zms_context)


def update_mediareleases(zms_context):
    zms2sql([MediaNews], zms_context)
