import time

import typer
import ZODB, zodburi
from sqlmodel import create_engine
from devtools import debug

from .commands import init_tables, update_tables
from ..models.zmsdefaults import ZMSSite, ZMSFolder, ZMSDocument, ZMSFormulator, ZMSDataTable
from ..models.newsevents import TeaserElement2022, Newsbox
from ..models.uniaktuell import UniaktuellArticle

# alias zmsadm='cd /Users/cm19b120/Workspace/Projects/CMS-Integrations/unibe-cmsapi-v3/; venv/bin/python -m cmsapi.cli.main'

ZODB_STORAGE = 'zeo://127.0.0.1:8000?storage=main'
SQLDB_STORAGE = "postgresql://postgres:mysecretpassword@localhost:5432/unibe_cmsapi"
# SQLDB_STORAGE = "sqlite:///../venv/unibe-cmsapi.db"

MODELS_AVAILABLE = {
    'ZMSSite': ZMSSite,
    # 'ZMSFolder': ZMSFolder,
    # 'ZMSDocument': ZMSDocument,
    'ZMSDataTable': ZMSDataTable,
    'ZMSFormulator': ZMSFormulator,
    'TeaserElement2022': TeaserElement2022,
    # 'Newsbox': Newsbox,
    'UniaktuellArticle': UniaktuellArticle,
}


def main(command: str = typer.Argument(None),
         metaobj: list[str] = typer.Option(...)):

    models = []
    for obj in metaobj:
        if obj == 'all':
            models = [x[1] for x in MODELS_AVAILABLE.items()]
        elif obj in MODELS_AVAILABLE:
            models.append(MODELS_AVAILABLE[obj])

    t0 = time.time()

    if command == 'init':
        init_tables(models, *connect_db())
    elif command == 'update':
        update_tables(models, *connect_db())
    else:
        raise typer.Abort()

    t1 = time.time()
    ts = t1-t0
    debug(ts/60 > 1 and f'{ts/60} min' or f'{ts} sec')


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


if __name__ == "__main__":
    typer.run(main)
