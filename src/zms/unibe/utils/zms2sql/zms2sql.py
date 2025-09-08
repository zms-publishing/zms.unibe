from .tables import process_sql_updates

def zms2sql(models, zms_context):
    for model in models:
        print(f'zms2sql: Sync {model.__name__}')
        zmsindex = zms_context.getZMSIndex()
        zcatalog = zmsindex.get_catalog()
        zmsindex_result = zcatalog(model.get_zms_catalog_query())
        process_sql_updates(zmsindex_result, model)