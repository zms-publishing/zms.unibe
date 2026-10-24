from .MediaNews import MediaNews
from .NewsBox import NewsBox
from .NewsContainer import NewsContainer
from ...utils.zms2sql import zms2sql


def update_newsboxes(zms_context):
    zms2sql([NewsContainer, NewsBox], zms_context)


def update_medianews(zms_context):
    zms2sql([MediaNews], zms_context)
