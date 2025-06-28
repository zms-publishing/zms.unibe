from zms.unibe.utils.zms2sql.tables import process_sql_updates
from zms.unibe.utils.db import connect_zodb

from .ZMSDataTable import ZMSDataTable
from .ZMSBoris import ZMSBoris


def update_datatables():
    print("update_datatables")

    zmsindex = connect_zodb()

    zmsindex_result = zmsindex({'meta_id': ZMSDataTable.get_zms_metaid()})
    process_sql_updates(zmsindex_result, ZMSDataTable)
    
    zmsindex_result = zmsindex({'meta_id': ZMSBoris.get_zms_metaid()})
    process_sql_updates(zmsindex_result, ZMSBoris)
    