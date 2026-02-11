import typer
from zms.unibe.agenda.sqlmodels.__main__ import update_agendas, fetch_agendas, fetch_statusmessages
from zms.unibe.mobileapp.sqlmodels.__main__ import update_newsevents, update_servicelinks
from zms.unibe.foundation.sqlmodels.__main__ import update_zmssites, update_zmsobjects
from zms.unibe.teasers.sqlmodels.__main__ import update_teasers, update_heros
from zms.unibe.announcements.sqlmodels.__main__ import update_newsboxes, update_mediareleases
from zms.unibe.uniaktuell.sqlmodels.__main__ import update_uniaktuell
from zms.unibe.datatables.sqlmodels.__main__ import update_datatables, update_boris
from zms.unibe.formulator.sqlmodels.__main__ import update_formulator
from zms.unibe.contacts.sqlmodels.__main__ import update_contacts
from zms.unibe.layouts.sqlmodels.__main__ import update_layouts
from zms.unibe.utils.zope.context import create_zope_app_context

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
        fn(zope_context)

def main():
    typer.run(run)

if __name__ == "__main__":
    main()
