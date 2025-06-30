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

    zmsindex_result = zmsindex({'meta_id': ContactBoxSection.get_zms_metaid()})
    process_sql_updates(zmsindex_result, ContactBoxSection)
    
    zmsindex_result = zmsindex({'meta_id': ContactBox.get_zms_metaid()})
    process_sql_updates(zmsindex_result, ContactBox)
    
    zmsindex_result = zmsindex({'meta_id': TeamSection.get_zms_metaid()})
    process_sql_updates(zmsindex_result, TeamSection)
    
    zmsindex_result = zmsindex({'meta_id': Team.get_zms_metaid()})
    process_sql_updates(zmsindex_result, Team)
    
    zmsindex_result = zmsindex({'meta_id': Person.get_zms_metaid()})
    process_sql_updates(zmsindex_result, Person)

