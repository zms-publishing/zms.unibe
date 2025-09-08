import typer
from zms.unibe.agenda.sqlmodels.__main__ import fetch_agendas
from zms.unibe.mobileapp.sqlmodels.__main__ import fetch_statusmessages, update_newsevents, update_servicelinks
from zms.unibe.foundation.sqlmodels.__main__ import update_zmssites, update_zmsobjects
from zms.unibe.teasers.sqlmodels.__main__ import update_teasers
from zms.unibe.announcements.sqlmodels.__main__ import update_newsboxes, update_mediareleases
from zms.unibe.uniaktuell.sqlmodels.__main__ import update_uniaktuell
from zms.unibe.datatables.sqlmodels.__main__ import update_datatables
from zms.unibe.formulator.sqlmodels.__main__ import update_formulator
from zms.unibe.contacts.sqlmodels.__main__ import update_contacts
from zms.unibe.layouts.sqlmodels.__main__ import update_layouts
from zms.unibe.utils.zope.context import create_zope_app_context

AVAILABLE_COMMANDS = {
    'fetch-agendas': fetch_agendas,
    'fetch-statusmessages': fetch_statusmessages,
    'update-zmssites': update_zmssites,
    'update-teasers': update_teasers,
    'update-newsboxes': update_newsboxes,
    'update-newsevents': update_newsevents,
    'update-servicelinks': update_servicelinks,
    'update-mediareleases': update_mediareleases,
    'update-uniaktuell': update_uniaktuell,
    'update-zmsobjects': update_zmsobjects,
    'update-datatables': update_datatables,
    'update-formulator': update_formulator,
    'update-contacts': update_contacts,
    'update-layouts': update_layouts
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
