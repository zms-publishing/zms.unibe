from datetime import datetime

from fastapi import APIRouter, Query
from sqlmodel import Session, select, not_

from zms.unibe.foundation.sqlmodels.ZMSSite import ZMSSite
from zms.unibe.uniaktuell.sqlmodels import UniaktuellArticle as model
from zms.unibe.utils.db import connect_sqldb
from zms.unibe.utils.helpers import get_attr_by_lang, strip_cmstest
from zms.unibe.utils.enums import Lang, ContentModel  # TODO: Lang->Locale as in zmscontent.routers
from ..schemas import uniaktuell as schema
from ..schemas.newsevents import Section
from ...zmscontent.routers.labels import get_content_labels

router = APIRouter(
    prefix="/v3",
    tags=["UniBE Mobile App (unibe.app)"])


@router.get("/uniaktuell", summary='Magazine articles', response_model=schema.UniaktuellArticleResponse,
            description='Magazine articles from <a href="https://www.uniaktuell.unibe.ch" '
                        'target="_blank">uniaktuell.unibe.ch</a>')
async def get_uniaktuell(
        lang: Lang = Lang.de,
        date_after: datetime | None = Query(None, description='Filter by date after (UTC)'),
        offset: int = 0,
        limit: int = 20):

    data = []

    # get translations from unibe langdict
    locale = {'ger': 'de', 'eng': 'en', 'fra': 'fr'}
    labels = get_content_labels(locale[lang.value], ContentModel.Uniaktuell)

    with Session(connect_sqldb()) as session:
        statement = [select(model.UniaktuellArticle, ZMSSite).join(ZMSSite).
                     where(get_attr_by_lang(lang,
                                            de=model.UniaktuellArticle.active_de,
                                            en=model.UniaktuellArticle.active_en,
                                            fr=model.UniaktuellArticle.active_fr)).
                     where(not_(ZMSSite.path.contains('/arbeitgeberin'))).
                     where(not_(ZMSSite.path.contains('/images'))).
                     where(not_(ZMSSite.path.contains('/jahresberichte'))).
                     where(not_(ZMSSite.path.contains('/uniapp'))).
                     where(not_(ZMSSite.path.contains('/uniintern'))).
                     where(not_(ZMSSite.path.contains('/zms_schulung'))).
                     where(not_(model.UniaktuellArticle.path.contains('/trashcan'))).
                     where(ZMSSite.path.like('%uni%aktuell%')).
                     where(date_after is None and True or (model.UniaktuellArticle.publish_dt_de > date_after)).
                     order_by(get_attr_by_lang(lang,
                                               de=model.UniaktuellArticle.publish_dt_de,
                                               en=model.UniaktuellArticle.publish_dt_en,
                                               fr=model.UniaktuellArticle.publish_dt_fr).desc())]

        results = session.exec(statement[0].offset(offset).limit(limit))
        total = session.exec(statement[0])

        for res in results.all():
            section = Section(
                type=res.ZMSSite.type,
                title=get_attr_by_lang(lang,
                                       de=res.ZMSSite.title_de,
                                       en=res.ZMSSite.title_en,
                                       fr=res.ZMSSite.title_fr),
                domain=f'https://{strip_cmstest(res.ZMSSite.domain)}',
                path=res.ZMSSite.path,
                uuid=res.ZMSSite.uuid
            )
            category = get_attr_by_lang(lang,
                                        res.UniaktuellArticle.category_de,
                                        res.UniaktuellArticle.category_en,
                                        res.UniaktuellArticle.category_fr)
            topic = get_attr_by_lang(lang,
                                     res.UniaktuellArticle.topics_de,
                                     res.UniaktuellArticle.topics_en,
                                     res.UniaktuellArticle.topics_fr)

            # TODO: check use cases and value settings
            # TODO: UniaktuellArticle.rubrik -> category
            # TODO: UniaktuellArticle.themen -> topics
            # TODO: UniaktuellArticle.get_ontology
            if labels.get(topic) is not None:
                topics = category + [labels.get(topic)]
            else:
                topics = category

            data.append(schema.UniaktuellArticle.model_validate({
                'title': get_attr_by_lang(lang,
                                          res.UniaktuellArticle.title_de,
                                          res.UniaktuellArticle.title_en,
                                          res.UniaktuellArticle.title_fr),
                'date': get_attr_by_lang(lang,
                                         res.UniaktuellArticle.publish_dt_de,
                                         res.UniaktuellArticle.publish_dt_en,
                                         res.UniaktuellArticle.publish_dt_fr),
                'infos': get_attr_by_lang(lang,
                                          res.UniaktuellArticle.abstract_de,
                                          res.UniaktuellArticle.abstract_en,
                                          res.UniaktuellArticle.abstract_fr),
                'topics': ', '.join(topics),
                'image': get_attr_by_lang(lang,
                                          res.UniaktuellArticle.img_de,
                                          res.UniaktuellArticle.img_en,
                                          res.UniaktuellArticle.img_fr),
                'url': get_attr_by_lang(lang,
                                        res.UniaktuellArticle.url_de,
                                        res.UniaktuellArticle.url_en,
                                        res.UniaktuellArticle.url_fr),
                'section': section,
                'dataSource': res.UniaktuellArticle.path,
                'dataLevel': res.UniaktuellArticle.level,
                'dataUuid': res.UniaktuellArticle.uuid,
            }))

        return {
            'offset': offset,
            'limit': limit,
            'total': len(total.all()),
            'data': data
        }
