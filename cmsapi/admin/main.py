import time
import typer

from .db import connect_db
from .commands import init_tables, update_tables
from ..models.zmsobjects import ZMSSite, ZMSDataTable, ZMSFormulator
from ..models.teaserelement2022 import TeaserElement2022
from ..models.newsbox import NewsBox
from ..models.agendas import AgendaPortal, AgendaLibraryDE, AgendaLibraryEN
from ..models.mobileapp import MobileApp
from ..models.newsevents import StatusMessage
from ..models.uniaktuell import UniaktuellArticle
from ..models.mediareleases import MediaRelease

# alias cmsadm='cd ~/PyCharm/CMSAPI/unibe-cmsapi-v3/; venv/bin/python -m cmsapi.admin.main'
# alias cmsadm='/app/bin/python -m cmsapi.admin.main'

MODELS_AVAILABLE = {
    'ZMSSite': ZMSSite,
    # 'ZMSDataTable': ZMSDataTable,
    # 'ZMSFormulator': ZMSFormulator,
    'TeaserElement2022': TeaserElement2022,
    'NewsBox': NewsBox,
    'AgendaPortal': AgendaPortal,
    'AgendaLibraryDE': AgendaLibraryDE,
    'AgendaLibraryEN': AgendaLibraryEN,
    'MobileApp': MobileApp,
    'StatusMessage': StatusMessage,
    'UniaktuellArticle': UniaktuellArticle,
    'MediaRelease': MediaRelease,
}


def main(command: str = typer.Argument(None, help='init | update'),
         feature: str = typer.Argument(None, help='NewsEvents | StatusMessages | MobileApp'),
         metaobj: list[str] = typer.Option([], help=' | '.join(MODELS_AVAILABLE.keys())+' | all')):

    _all = False  # drop and create all tables
    for obj in metaobj:
        if obj == 'all':
            _all = True
            models = [x[1] for x in MODELS_AVAILABLE.items()]
        elif obj in MODELS_AVAILABLE:
            models.append(MODELS_AVAILABLE[obj])
        else:
            raise typer.Abort()

    if feature == 'NewsEvents':  # this Argument overrides any individually set Options via --metaobj
        models = (ZMSSite, AgendaPortal, AgendaLibraryDE, AgendaLibraryEN, TeaserElement2022, NewsBox)

    if feature == 'Announcements':
        models = (ZMSSite, StatusMessage, UniaktuellArticle, MediaRelease)

    if feature == 'MobileApp':
        models = (ZMSSite, MobileApp, )

    t0 = time.time()

    if command == 'init':
        init_tables(models, *connect_db(), _all=_all)
    elif command == 'update':
        update_tables(models, *connect_db())
    else:
        raise typer.Abort()

    t1 = time.time()
    ts = t1-t0
    print('--------------------------------------------------------------------------')
    print('PROCESSING TIME', ts/60 > 1 and f': {ts/60} min' or f': {ts} sec')
    print('==========================================================================')


if __name__ == "__main__":
    typer.run(main)
