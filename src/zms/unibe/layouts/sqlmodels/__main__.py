from zms.unibe.utils.zms2sql.tables import process_sql_updates
from zms.unibe.utils.db import connect_zodb

from .ContentPane import ContentPane
from .ContentTabs import ContentTabs
from .TwoCols import TwoCols
from .UniBEEvent import UniBEEvent
from .UniBEFactsheet import UniBEFactsheet
from .WeiterbildungStudiengang import WeiterbildungStudiengang


def update_layouts():
    print("update_layouts")
    
    zmsindex = connect_zodb()
    
    zmsindex_result = zmsindex({'meta_id': ContentPane.get_zms_metaid()})
    process_sql_updates(zmsindex_result, ContentPane)
    
    zmsindex_result = zmsindex({'meta_id': ContentTabs.get_zms_metaid()})
    process_sql_updates(zmsindex_result, ContentTabs)
    
    zmsindex_result = zmsindex({'meta_id': TwoCols.get_zms_metaid()})
    process_sql_updates(zmsindex_result, TwoCols)
    
    zmsindex_result = zmsindex({'meta_id': UniBEEvent.get_zms_metaid()})
    process_sql_updates(zmsindex_result, UniBEEvent)
    
    zmsindex_result = zmsindex({'meta_id': UniBEFactsheet.get_zms_metaid()})
    process_sql_updates(zmsindex_result, UniBEFactsheet)
    
    zmsindex_result = zmsindex({'meta_id': WeiterbildungStudiengang.get_zms_metaid()})
    process_sql_updates(zmsindex_result, WeiterbildungStudiengang)
    