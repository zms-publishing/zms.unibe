from zms.unibe.utils.zms2sql.tables import process_sql_updates
from zms.unibe.utils.db import connect_zodb

from .UniaktuellArticle import UniaktuellArticle


def update_uniaktuell():
    print("update_uniaktuell")

    zmsindex = connect_zodb()
    zmsindex_result = zmsindex({'path': '/unibe/portal/uni_aktuell/content',
                                'meta_id': 'UniaktuellArticle'})

    process_sql_updates(zmsindex_result, UniaktuellArticle)


if __name__ == "__main__":
    update_uniaktuell()
