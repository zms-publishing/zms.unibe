import xmltodict
from fastapi import APIRouter
from Products.zms._multilangmanager import exportXml
from zms.unibe.utils.zope.context import create_zope_app_context
from zms.unibe.utils.enums import Locale, Lang, ContentModel, LabelPrefix


router = APIRouter(
    prefix="/v3/zms",
    tags=["UniBE Web CMS (unibe.ch)"],
)


@router.get(
    path="/content/labels",
    summary="Get label translations from language dictionary filtered by content model or prefix",
    # response_model=schema.ZMSAgendaResponse,
)
def get_content_labels(
        locale: Locale = Locale.de,
        content_model: ContentModel | None = None,
        prefix: str | None = None,
):
    context = create_zope_app_context()
    lang = Lang[locale].value
    
    if content_model in LabelPrefix._member_names_:
        prefix = LabelPrefix[content_model].value
        if content_model.value == 'Uniaktuell':
            context = context.portal.uni_aktuell.content
            # TODO: use UniaktuellArticle.KEYWORD in ...?!
    else:
        if prefix is None:
            prefix = ''
        if content_model is not None:
            prefix = '###'
    
    langdict = xmltodict.parse(exportXml(context, []))

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
    