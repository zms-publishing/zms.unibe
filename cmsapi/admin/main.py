import time
import typer

from .db import connect_db
from .commands import init_tables, update_tables
from .newsevents import update_newsevents_table
from ..models.zmsobjects import *
from ..models.teaserelement2022 import TeaserContainer2022, TeaserElement2022, Hero2022, Hero
from ..models.newsbox import NewsBox, NewsContainer
from ..models.agendas import AgendaPortal, AgendaLibraryDE, AgendaLibraryEN
from ..models.servicelinks import ServiceLink
from ..models.newsevents import StatusMessage
from ..models.uniaktuell import UniaktuellArticle
from ..models.mediareleases import MediaRelease

# alias cmsadm='cd ~/PyCharm/CMSAPI/unibe-cmsapi-v3/; venv/bin/python -m cmsapi.admin.main'
# alias cmsadm='/app/bin/python -m cmsapi.admin.main'

MODELS_AVAILABLE = {
    'ZMSSite': ZMSSite,
    'ZMSBoris': ZMSBoris,
    'ZMSDataTable': ZMSDataTable,
    'ZMSFormulator': ZMSFormulator,
    #'ZMSFolder': ZMSFolder,
    #'ZMSGraphic': ZMSGraphic,
    #'ZMSDocument': ZMSDocument,
    #'ZMSFile': ZMSFile,
    #'ZMSTable': ZMSTable,
    'TeaserContainer2022': TeaserContainer2022,
    'TeaserElement2022': TeaserElement2022,
    'Hero2022': Hero2022,
    'Hero': Hero,
    'NewsContainer': NewsContainer,
    'NewsBox': NewsBox,
    'AgendaPortal': AgendaPortal,
    #'AgendaLibraryDE': AgendaLibraryDE,
    #'AgendaLibraryEN': AgendaLibraryEN,
    'ServiceLink': ServiceLink,
    'StatusMessage': StatusMessage,
    'UniaktuellArticle': UniaktuellArticle,
    'MediaRelease': MediaRelease,
    #'TwoCols': TwoCols,
    #'ContentTabs': ContentTabs,
    #'ContentPane': ContentPane,
    #'AlertBox': AlertBox,
    #'InfoBox': InfoBox,
    #'Person': Person,
    #'ContactBoxSection': ContactBoxSection,
    #'ContactBox': ContactBox,
    #'TeamSection': TeamSection,
    #'Team': Team,
    #'WeiterbildungStudiengang': WeiterbildungStudiengang,
    #'UniBEFactsheet': UniBEFactsheet,
    'UniBEEvent': UniBEEvent,
    'CodeBlock': CodeBlock,
}


def main(command: str = typer.Argument(None, help='init | update'),
         feature: str = typer.Argument(None, help='NewsEvents | NewsBoxes | Announcements | ServiceLinks'),
         metaobj: list[str] = typer.Option([], help=' | '.join(MODELS_AVAILABLE.keys())+' | all')):

    _all = False  # drop and create all tables
    models = []
    for obj in metaobj:
        if obj == 'all':
            _all = True
            models = [x[1] for x in MODELS_AVAILABLE.items()]
        elif obj in MODELS_AVAILABLE:
            models.append(MODELS_AVAILABLE[obj])
        else:
            raise typer.Abort()

    if feature == 'NewsEvents':  # this Argument overrides any individually set Options via --metaobj
                                 # AgendaPortal processes also AgendaLibraryDE and AgendaLibraryEN in _fetch_agenda_data
        models = (ZMSSite, AgendaPortal, TeaserContainer2022, TeaserElement2022, StatusMessage, )

    if feature == 'NewsBoxes':
        models = (NewsContainer, NewsBox, )

    if feature == 'Announcements':
        models = (UniaktuellArticle, MediaRelease, )

    if feature == 'ServiceLinks':
        models = (ServiceLink, )

    t0 = time.time()

    if command == 'init':
        init_tables(models, *connect_db(), _all=_all)
    elif command == 'update':
        update_tables(models, *connect_db())
    else:
        raise typer.Abort()

    update_newsevents_table(*connect_db())

    t1 = time.time()
    ts = t1-t0
    print('--------------------------------------------------------------------------')
    print('PROCESSING TIME', f'{ts:.3f} sec', f'= {ts/60:.2f} min')
    print('==========================================================================')


if __name__ == "__main__":
    typer.run(main)
