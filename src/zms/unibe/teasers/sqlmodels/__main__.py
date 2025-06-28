from zms.unibe.utils.zms2sql.tables import process_sql_updates
from zms.unibe.utils.db import connect_zodb

from .TeaserContainer2022 import TeaserContainer2022
from .TeaserElement2022 import TeaserElement2022


def update_teasers():
    print("update teasers")

    zmsindex = connect_zodb()

    zmsindex_result = zmsindex({'meta_id': TeaserContainer2022.get_zms_metaid()})
    process_sql_updates(zmsindex_result, TeaserContainer2022)
    
    zmsindex_result = zmsindex({'meta_id': TeaserElement2022.get_zms_metaid()})
    process_sql_updates(zmsindex_result, TeaserElement2022)


if __name__ == '__main__':
    update_teasers()
