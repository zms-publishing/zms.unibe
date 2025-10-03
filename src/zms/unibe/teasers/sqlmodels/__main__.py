from zms.unibe.utils.zms2sql import zms2sql
from .TeaserContainer2022 import TeaserContainer2022
from .TeaserElement2022 import TeaserElement2022
from .Hero2022 import Hero2022
from .Hero import Hero


def update_teasers(zms_context):
    # Example: Drop all sql tables and init ZMSSite to link using foreign keys
    #
    # from zms.unibe.utils.zms2sql.tables import drop_all
    # drop_all(verbose=True)
    # zms2sql([ZMSSite], zms_context, verbose=True)
    
    zms2sql([TeaserContainer2022, TeaserElement2022], zms_context)


def update_heros(zms_context):
    # Example: Drop sql tables before update
    zms2sql([Hero2022, Hero], zms_context, drop=True, verbose=True)
