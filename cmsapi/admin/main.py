import time
import typer

from .db import connect_db
from .commands import init_tables, update_tables
from ..models.zmsobjects import ZMSSite, ZMSDataTable, ZMSFormulator
from ..models.teaserelement2022 import TeaserElement2022
from ..models.agendas import AgendaPortal, AgendaLibraryDE, AgendaLibraryEN
from ..models.mobileapp import MobileApp

# alias cmsadm='cd ~/Workspace/Projects/CMS-Integrations/unibe-cmsapi-v3/; venv/bin/python -m cmsapi.admin.main'


MODELS_AVAILABLE = {
    'ZMSSite': ZMSSite,
    'ZMSDataTable': ZMSDataTable,
    'ZMSFormulator': ZMSFormulator,
    'AgendaPortal': AgendaPortal,
    'AgendaLibraryDE': AgendaLibraryDE,
    'AgendaLibraryEN': AgendaLibraryEN,
    'TeaserElement2022': TeaserElement2022,
}


def main(command: str = typer.Argument(None, help='init | update'),
         feature: str = typer.Argument(None, help='NewsEvents'),
         metaobj: list[str] = typer.Option([], help=' | '.join(MODELS_AVAILABLE.keys()))):

    _all = False  # drop and create all tables
    models = [ZMSSite]  # refresh data of basic relation always - w/o init reflecting model change of ZMSSite
    for obj in metaobj:
        if obj == 'all':
            _all = True  # refresh data of all relations - w/ init reflecting model change of ZMSSite
            models = [x[1] for x in MODELS_AVAILABLE.items()]
            models.append(MobileApp)
        elif obj in MODELS_AVAILABLE:
            models.append(MODELS_AVAILABLE[obj])
        else:
            raise typer.Abort()

    if feature == 'NewsEvents':  # this Argument overrides any individually set Options via --metaobj
        # Keep this order! TeaserElement2022 must exist before Agendas - see TODO: separate processing in newsevents
        models = (ZMSSite, TeaserElement2022, AgendaPortal, AgendaLibraryDE, AgendaLibraryEN)

    if feature == 'MobileApp':
        models = (MobileApp, )

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
