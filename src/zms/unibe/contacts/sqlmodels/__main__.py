from zms.unibe.utils.db import connect_zodb
from zms.unibe.utils.zms2sql.tables import process_sql_updates
from .ContactBox import ContactBox
from .ContactBoxSection import ContactBoxSection
from .Person import Person
from .Team import Team
from .TeamSection import TeamSection


def update_contacts():
    print("update_contacts")

    zmsindex = connect_zodb()

    models = [ContactBoxSection, ContactBox, TeamSection, Team, Person]
    for model in models:
        zmsindex_result = zmsindex({'meta_id': model.get_zms_metaid()})
        process_sql_updates(zmsindex_result, model)

