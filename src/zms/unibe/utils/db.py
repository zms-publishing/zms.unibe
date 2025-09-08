import os

from devtools import debug
from sqlmodel import create_engine
from .zms2sql.tables import process_sql_updates

ZODB_STORAGE = os.getenv('ZODB_STORAGE', 'zeo://127.0.0.1:8000?storage=main')
SQLDB_STORAGE = os.getenv('SQLDB_STORAGE', 'postgresql://127.0.0.1:5432/zms_fastapi')


def connect_sqldb(verbose=False):
    
    credentials = 'postgres:mysecretpassword'
    
    try:
        with open('/run/secrets/sqldb.credentials') as file:  # via Docker Swarm secrets config
            credentials = file.read().strip()
    except FileNotFoundError:
        pass  # use default credentials
    
    sqlengine = create_engine(
        SQLDB_STORAGE.replace('://', f'://{credentials}@'),
        pool_pre_ping=True,
        # connect_args={"check_same_thread": False},  # for SQLite only
        # echo=True
    )
    
    if verbose:
        debug(sqlengine)
        
    return sqlengine


def zms2sql(models, zms_context):
    for model in models:
        print(f'zms2sql: Transfer {model.__name__}')
        zmsindex_result = zms_context.zcatalog_index(model.get_zms_catalog_query())
        process_sql_updates(zmsindex_result, model)
