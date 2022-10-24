from sqlmodel import create_engine
import os

SQLDB_STORAGE = os.getenv('SQLDB_STORAGE', 'postgresql://127.0.0.1:5432/unibe_cmsapi')

try:
    with open('/run/secrets/sqldb.credentials') as file:  # via Docker Swarm secrets config
        credentials = file.read().strip()
except FileNotFoundError:
    credentials = 'postgres:mysecretpassword'

engine = create_engine(SQLDB_STORAGE.replace('://', f'://{credentials}@'),
                       # connect_args={"check_same_thread": False},  # for SQLite only
                       # echo=True
                       )
