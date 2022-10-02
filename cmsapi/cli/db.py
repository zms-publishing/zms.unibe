import ZODB, zodburi
from sqlmodel import create_engine
from devtools import debug

ZODB_STORAGE = 'zeo://127.0.0.1:8000?storage=main'
SQLDB_STORAGE = "postgresql://postgres:mysecretpassword@localhost:5432/unibe_cmsapi"
# SQLDB_STORAGE = "sqlite:///../venv/unibe-cmsapi.db"


def connect_db():

    factory, dbargs = zodburi.resolve_uri(ZODB_STORAGE)
    connection = ZODB.connection(factory(), **dbargs)
    root = connection.root()
    zmsindex = root['Application']['unibe']['zcatalog_index']

    sqlengine = create_engine(
        SQLDB_STORAGE,
        # for SQLite only
        # connect_args={"check_same_thread": False},
        # echo=True
    )

    debug(ZODB_STORAGE, dbargs)
    debug(sqlengine)
    debug(zmsindex)

    return zmsindex, sqlengine
