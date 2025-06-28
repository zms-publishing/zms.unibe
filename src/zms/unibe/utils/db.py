import ZODB, zodburi
import os
from sqlmodel import create_engine
from devtools import debug

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


def connect_zodb(verbose=False):

    factory, dbargs = zodburi.resolve_uri(ZODB_STORAGE)
    connection = ZODB.connection(factory(), **dbargs)
    root = connection.root()
    zmsindex = root['Application']['unibe']['zcatalog_index']

    if verbose:
        debug(ZODB_STORAGE, dbargs)
        debug(zmsindex)

    return zmsindex
