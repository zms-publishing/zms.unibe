from zms.unibe.utils.db import zms2sql
from .CodeBlock import CodeBlock
from .ZMSDocument import ZMSDocument
from .ZMSFile import ZMSFile
from .ZMSFolder import ZMSFolder
from .ZMSGraphic import ZMSGraphic
from .ZMSSite import ZMSSite
from .ZMSTable import ZMSTable
from .ZMSTextarea import ZMSTextarea


def update_zmssites(zms_context):
    zms2sql([ZMSSite], zms_context)


def update_zmsobjects(zms_context):
    zms2sql([CodeBlock, ZMSDocument, ZMSFile, ZMSFolder, ZMSGraphic, ZMSTable, ZMSTextarea], zms_context)
