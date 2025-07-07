from zms.unibe.utils.db import connect_zodb
from zms.unibe.utils.zms2sql.tables import process_sql_updates
from .ContentPane import ContentPane
from .ContentTabs import ContentTabs
from .TwoCols import TwoCols
from .UniBEEvent import UniBEEvent
from .UniBEFactsheet import UniBEFactsheet
from .WeiterbildungStudiengang import WeiterbildungStudiengang


def update_layouts():
    print("update_layouts")
    
    zmsindex = connect_zodb()
    
    models = [ContentPane, ContentTabs, TwoCols, UniBEEvent, UniBEFactsheet, WeiterbildungStudiengang]
    for model in models:
        zmsindex_result = zmsindex({'meta_id': model.get_zms_metaid()})
        process_sql_updates(zmsindex_result, model)
    