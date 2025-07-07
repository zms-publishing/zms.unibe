from pathlib import Path

from zms.unibe.utils.db import connect_zodb
from zms.unibe.utils.zms2sql.tables import process_sql_updates
from .MediaNews import MediaNews
from .NewsBox import NewsBox
from .NewsContainer import NewsContainer


def update_newsboxes():
    print( "Updating newsboxes")

    zmsindex = connect_zodb()

    zmsindex_result = zmsindex({'meta_id': NewsContainer.get_zms_metaid()})
    process_sql_updates(zmsindex_result, NewsContainer)

    zmsindex_result = zmsindex({'path': '/unibe/portal/unibiblio/content', 'meta_id': 'newsbox'})
    for newscontainer in open(f'{Path(__file__).parent.absolute()}/newsbox_all_active_filtered.csv'):
        zmsindex_result += zmsindex({'path': f'{newscontainer.strip()}', 'meta_id': 'newsbox'})

    zmsindex_result = zmsindex({'meta_id': NewsBox.get_zms_metaid()})
    process_sql_updates(zmsindex_result, NewsBox)


def update_mediareleases():
    print( "update_mediareleases")    
    
    zmsindex = connect_zodb()
    zmsindex_result = zmsindex({'path': '/unibe/portal/media_relations/content',
                                'meta_id': 'media_news'})

    process_sql_updates(zmsindex_result, MediaNews)
    
    
if __name__ == "__main__":
    update_newsboxes()
    update_mediareleases()
