from zms.unibe.utils.db import zms2sql
from .ContactBox import ContactBox
from .ContactBoxSection import ContactBoxSection
from .Person import Person
from .Team import Team
from .TeamSection import TeamSection


def update_contacts(zms_context):
    zms2sql([ContactBoxSection, ContactBox, TeamSection, Team, Person], zms_context)
