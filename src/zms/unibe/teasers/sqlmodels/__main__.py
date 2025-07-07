from zms.unibe.utils.db import connect_zodb
from zms.unibe.utils.zms2sql.tables import process_sql_updates
from .TeaserContainer2022 import TeaserContainer2022
from .TeaserElement2022 import TeaserElement2022


def update_teasers():
    print("update teasers")

    zmsindex = connect_zodb()

    models = [TeaserContainer2022, TeaserElement2022]
    for model in models:
        zmsindex_result = zmsindex({'meta_id': model.get_zms_metaid()})
        process_sql_updates(zmsindex_result, model)


if __name__ == '__main__':
    update_teasers()
