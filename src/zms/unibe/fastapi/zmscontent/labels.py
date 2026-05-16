import os
import xmltodict
from fastapi import APIRouter, Query, Response

from Products.zms._multilangmanager import exportXml
from zms.unibe.fastapi.meta import Tags
from zms.unibe.utils.enums import ContentModel, LabelPrefix, Lang, Locale
from zms.unibe.utils.zope.context import create_zope_app_context, get_zmsindex

router = APIRouter(prefix="/zms/content", tags=[Tags.content])

@router.get(
    path="/labels",
    summary="Get label translations from language dictionary filtered by content model or prefix",
    # response_model=schema.ZMSAgendaResponse,
)
def get_content_labels(
        locale: Locale = Locale.de,
        portal_master: str | None = Query(os.getenv('PORTAL_MASTER', '/myzmsx/content'),
                                          description="Portal master with ZMSIndex"),
        content_model: ContentModel | None = None,
        prefix: str | None = None,
):
    context = create_zope_app_context()
    zmsindex = get_zmsindex(portal_master, context)
    
    lang = Lang[locale].value
    content = zmsindex.content
    
    if content_model in LabelPrefix._member_names_:
        prefix = LabelPrefix[content_model].value
    else:
        if prefix is None:
            prefix = ''
        if content_model is not None:
            prefix = '###'
    
    langdict = xmltodict.parse(exportXml(content, []))

    labels = {}
    for listitem in langdict['list']['item']:
        key = val = ''
        for dictitem in listitem['dictionary']['item']:
            if '#text' in list(dictitem.keys()) and dictitem['@key'] == 'key':
                key = dictitem['#text']
            if '#text' in list(dictitem.keys()) and dictitem['@key'] == lang:
                val = dictitem['#text']
        if key.startswith(prefix):
            labels[key] = val
    return labels
    