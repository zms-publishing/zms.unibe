from zms.unibe.utils.db import connect_zodb
from zms.unibe.utils.zms2sql.tables import process_sql_updates
from .CodeBlock import CodeBlock
from .ZMSDocument import ZMSDocument
from .ZMSFile import ZMSFile
from .ZMSFolder import ZMSFolder
from .ZMSGraphic import ZMSGraphic
from .ZMSSite import ZMSSite
from .ZMSTable import ZMSTable
from .ZMSTextarea import ZMSTextarea


def update_zmssites():
    print("update_zmssite")

    count_objs = {}

    zmsindex = connect_zodb()
    zmsindex_result = zmsindex({'meta_id': 'ZMS'})
    
    for site in zmsindex_result:
        count_objs[site] = len(zmsindex({'path': site.getPath()}))
        
    process_sql_updates(zmsindex_result, ZMSSite, count_objs)
    
def update_zmsobjects():
    print("update_zmsobjects")
    
    zmsindex = connect_zodb()

    models = [CodeBlock, ZMSDocument, ZMSFile, ZMSFolder, ZMSGraphic, ZMSTable, ZMSTextarea]
    for model in models:
        zmsindex_result = zmsindex({'meta_id': model.get_zms_metaid()})
        process_sql_updates(zmsindex_result, model)
    
    
if __name__ == "__main__":
    update_zmssites()
    update_zmsobjects()
