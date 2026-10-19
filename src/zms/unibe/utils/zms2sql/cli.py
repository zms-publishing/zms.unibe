import typer

from ...agenda.sqlmodels.__main__ import fetch_agendas, fetch_statusmessages, update_agendas
from ...announcements.sqlmodels.__main__ import update_mediareleases, update_newsboxes
from ...contacts.sqlmodels.__main__ import update_contacts
from ...datatables.sqlmodels.__main__ import update_boris, update_datatables
from ...formulator.sqlmodels.__main__ import update_formulator
from ...foundation.sqlmodels.__main__ import update_zmsobjects, update_zmssites
from ...layouts.sqlmodels.__main__ import update_layouts
from ...mobileapp.sqlmodels.__main__ import update_newsevents, update_servicelinks
from ...teasers.sqlmodels.__main__ import update_heros, update_teasers
from ...uniaktuell.sqlmodels.__main__ import update_uniaktuell
from ...utils.zope.context import create_zope_app_context

AVAILABLE_COMMANDS = {
    # DEFAULT
    'update-zmssites': update_zmssites,             #     (512) =  0.97 min
    # MUST-HAVE
    'update-servicelinks': update_servicelinks,     #     (105) =  0.02 min
    'update-heros': update_heros,                   #      (84) =  0.05 min 
    'update-teasers': update_teasers,               #   (5,842) =  2.98 min
    'update-newsboxes': update_newsboxes,           #  (18,397) =  5.67 min
    'update-agendas': update_agendas,
    'fetch-agendas': fetch_agendas,
    'fetch-statusmessages': fetch_statusmessages,
    'update-newsevents': update_newsevents,         #  (11,594) => aggregates above to access via zms-fastapi
    # NICE-TO-HAVE
    'update-mediareleases': update_mediareleases,   #   (2,069) =  0.72 min
    'update-uniaktuell': update_uniaktuell,         #   (2,180) =  0.72 min
    # OPTIONAL
    'update-datatables': update_datatables,         #     (150) =  0.11 min (w/o data in mediadb on localhost)
    'update-boris': update_boris,                   #     (741) =  0.35 min (w/o data in mediadb on localhost)
    'update-formulator': update_formulator,         #   (1,528) =  0.97 min
    # EXTENSIVE
    'update-contacts': update_contacts,             #  (41,348) = 11.42 min
    'update-layouts': update_layouts,               #  (61,788) = 22.65 min
    'update-zmsobjects': update_zmsobjects,         # (317,300) = 65.17 min 
}

def run(command: str = typer.Argument(None, help=' | '.join(AVAILABLE_COMMANDS.keys()))):
    if command not in AVAILABLE_COMMANDS:
        raise ValueError(f'{command} does not exist')
    fn = AVAILABLE_COMMANDS[command]
    args_count = fn.__code__.co_argcount
    if args_count == 0:
        fn()
    else:
        zope_context = create_zope_app_context()
        fn(zope_context.unibe.content)

def main():
    typer.run(run)

if __name__ == "__main__":
    main()
