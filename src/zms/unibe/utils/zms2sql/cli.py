import typer
from zms.unibe.agenda.sqlmodels.__main__ import fetch_agendas, fetch_statusmessages
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
    'update-zmssites': update_zmssites,             # (512)
    # MUST-HAVE
    'update-teasers': update_teasers,               # (5.944)
    'update-heros': update_heros,                   # (85)
    'update-newsboxes': update_newsboxes,           # (18.203)
    'fetch-agendas': fetch_agendas,
    'fetch-statusmessages': fetch_statusmessages,
    'update-newsevents': update_newsevents,         # (11.594)
    'update-servicelinks': update_servicelinks,     # (105)
    # NICE-TO-HAVE
    'update-mediareleases': update_mediareleases,   # (2.088)
    'update-uniaktuell': update_uniaktuell,         # (2.808)
    # OPTIONAL
    'update-datatables': update_datatables,         # (150)
    'update-boris': update_boris,                   # (746)
    'update-formulator': update_formulator,         # (1.556)
    # EXTENSIVE
    'update-contacts': update_contacts,             # (41.840)
    'update-layouts': update_layouts,               # (62.494)
    'update-zmsobjects': update_zmsobjects,         # (324.209)
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
