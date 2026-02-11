import os

from devtools import debug
from sqlmodel import create_engine

ZODB_STORAGE = os.getenv('ZODB_STORAGE', 'zeo://127.0.0.1:8000?storage=main')
SQLDB_STORAGE = os.getenv('SQLDB_STORAGE', 'postgresql://127.0.0.1:5432/zms_fastapi')


def connect_sqldb(verbose=False):
    
    global SQLDB_STORAGE
    credentials = 'postgres:mysecretpassword'
    
    try:
        with open('/run/secrets/sqldb.credentials') as file:  # via Docker Swarm secrets config
            credentials = file.read().strip()
    except FileNotFoundError:
        pass  # use default credentials

    if '@' not in SQLDB_STORAGE:  # apply credentials only if not already present
        SQLDB_STORAGE = SQLDB_STORAGE.replace('://', f'://{credentials}@')

    sqlengine = create_engine(
        SQLDB_STORAGE,
        pool_pre_ping=True,
        # connect_args={"check_same_thread": False},  # for SQLite only
        # echo=True
    )
    
    if verbose:
        debug(sqlengine)
        
    return sqlengine
