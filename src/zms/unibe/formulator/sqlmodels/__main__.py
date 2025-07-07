from zms.unibe.utils.db import connect_zodb
from zms.unibe.utils.zms2sql.tables import process_sql_updates
from .ZMSFormulator import ZMSFormulator


def update_formulator():
    print("update_formulator")

    zmsindex = connect_zodb()

    zmsindex_result = zmsindex({'meta_id': ZMSFormulator.get_zms_metaid()})
    process_sql_updates(zmsindex_result, ZMSFormulator)
    