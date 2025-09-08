import xmltodict
from fastapi import APIRouter
from enum import Enum
from Products.zms._multilangmanager import exportXml
from zms.unibe.utils.zope.zope_context import create_zope_app_context


class Locale(str, Enum):  # https://en.wikipedia.org/wiki/ISO_639-1
    de = "de"
    en = "en"
    fr = "fr"


class Lang(str, Enum):  # https://en.wikipedia.org/wiki/ISO_639-3
    de = "ger"
    en = "eng"
    fr = "fra"


class ContentModel(str, Enum):
    Uniaktuell = "Uniaktuell"
    ZMSFormulator = "ZMSFormulator"
    ZMSAgenda = "ZMSAgenda"


class LabelPrefix(str, Enum):
    Uniaktuell = "UA_"
    ZMSFormulator = "zms.formulator.lib."
    ZMSAgenda = "ZMSAgenda."


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
        offset: int = 0,
        limit: int = 20,
):
    lang = Lang[locale].value
    prefix = LabelPrefix[content_model].value if content_model is not None else prefix

    context = create_zope_app_context()
    langdict = xmltodict.parse(exportXml(context, []))

    labels = []
    if prefix is not None:
        for i in langdict['list']['item']:
            for j in i['dictionary']['item']:
                if '#text' in j:
                    if j['#text'].startswith(prefix):
                        for x in i['dictionary']['item']:
                            if '#text' in x and x['@key'] == lang:
                                labels.append({j['#text']: x['#text']})
    return labels
    