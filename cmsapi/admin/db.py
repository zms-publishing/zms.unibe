import ZODB, zodburi
import os
from sqlmodel import create_engine
from devtools import debug

ZODB_STORAGE = 'zeo://127.0.0.1:8000?storage=main'
SQLDB_STORAGE = os.getenv('SQLDB_STORAGE', 'postgresql://127.0.0.1:5432/unibe_cmsapi')

try:
    with open('/run/secrets/sqldb.credentials') as file:  # via Docker Swarm secrets config
        credentials = file.read().strip()
except FileNotFoundError:
    credentials = 'postgres:mysecretpassword'


def connect_db():

    factory, dbargs = zodburi.resolve_uri(ZODB_STORAGE)
    connection = ZODB.connection(factory(), **dbargs)
    root = connection.root()
    zmsindex = root['Application']['unibe']['zcatalog_index']

    sqlengine = create_engine(SQLDB_STORAGE.replace('://', f'://{credentials}@'),
                              # connect_args={"check_same_thread": False},  # for SQLite only
                              # echo=True
                              )

    debug(ZODB_STORAGE, dbargs)
    debug(sqlengine)
    debug(zmsindex)

    return zmsindex, sqlengine
