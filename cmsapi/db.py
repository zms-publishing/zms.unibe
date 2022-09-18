from flask_zodb import ZODB
from sqlmodel import create_engine
import os

zodb = ZODB()

SQLDB_STORAGE = 'postgresql://' + os.getenv('SQLDB_STORAGE', 'postgres:mysecretpassword@127.0.0.1:5432/unibe_cmsapi')
# SQLDB_STORAGE = "sqlite:///../venv/unibe-cmsapi.db"

engine = create_engine(SQLDB_STORAGE,
                       # connect_args={"check_same_thread": False},  # for SQLite only
                       # echo=True
                       )
