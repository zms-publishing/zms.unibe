from zms.unibe.utils.db import connect_zodb
from zms.unibe.utils.zms2sql.tables import process_sql_updates
from .ZMSBoris import ZMSBoris
from .ZMSDataTable import ZMSDataTable


def update_datatables():
    print("update_datatables")

    zmsindex = connect_zodb()

    models = [ZMSDataTable, ZMSBoris]
    for model in models:
        zmsindex_result = zmsindex({'meta_id': model.get_zms_metaid()})
        process_sql_updates(zmsindex_result, model)
    