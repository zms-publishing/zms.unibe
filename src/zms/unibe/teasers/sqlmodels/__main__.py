from zms.unibe.utils.db import zms2sql
from .TeaserContainer2022 import TeaserContainer2022
from .TeaserElement2022 import TeaserElement2022


def update_teasers(zms_context):
    zms2sql([TeaserContainer2022, TeaserElement2022], zms_context)
