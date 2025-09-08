from zms.unibe.utils.db import zms2sql
from .ContentPane import ContentPane
from .ContentTabs import ContentTabs
from .TwoCols import TwoCols
from .UniBEEvent import UniBEEvent
from .UniBEFactsheet import UniBEFactsheet
from .WeiterbildungStudiengang import WeiterbildungStudiengang


def update_layouts(zms_context):
    zms2sql([ContentPane, ContentTabs, TwoCols, UniBEEvent, UniBEFactsheet, WeiterbildungStudiengang], zms_context)
