from zms.unibe.utils.zms2sql import zms2sql
from .TeaserContainer2022 import TeaserContainer2022
from .TeaserElement2022 import TeaserElement2022
from .Hero2022 import Hero2022
from .Hero import Hero


def update_teasers(zms_context):
    zms2sql([TeaserContainer2022, TeaserElement2022], zms_context)

def update_heros(zms_context):
    zms2sql([Hero2022, Hero], zms_context)
