from .tables import process_sql_updates


def zms2sql(models, zms_context, verbose=False):
    for model in models:
        print(f"zms2sql: Transfer {model.__name__}")
        zmsindex_result = zms_context.zcatalog_index(model.get_zms_catalog_query())
        process_sql_updates(zmsindex_result, model, verbose)
