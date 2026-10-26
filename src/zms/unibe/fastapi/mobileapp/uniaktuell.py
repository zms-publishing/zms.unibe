import asyncio
from datetime import date

from fastapi import APIRouter, Query
from fastapi_cache.decorator import cache
from sqlmodel import not_, select

from ...fastapi.meta import Tags
from ...fastapi.zmscontent.labels import get_content_labels
from ...foundation.sqlmodels.ZMSSite import ZMSSite
from ...mobileapp.schemas.NewsEventsSchema import Section
from ...uniaktuell.schemas import UniaktuellSchema as schema
from ...uniaktuell.sqlmodels import UniaktuellArticle as model
from ...utils.dependencies import ContextDependency, SessionDependency
from ...utils.enums import ContentModel, Locale
from ...utils.helpers import get_attr_by_lang, local_timezone, strip_cmstest

router = APIRouter(tags=[Tags.mobile])


@router.get("/uniaktuell", summary='Magazine articles', response_model=schema.UniaktuellArticleResponse,
            description='Magazine articles from <a href="https://www.uniaktuell.unibe.ch" '
                        'target="_blank">uniaktuell.unibe.ch</a>')
@cache(expire=600)
def get_uniaktuell(
        session: SessionDependency,
        context: ContextDependency,
        lang: Locale = Locale.de,
        date_after: date | None = Query(None, description='Filter by date after'),
        offset: int = 0,
        limit: int = 20):

    data = []

    # get translations from unibe langdict
    labels = asyncio.run(get_content_labels(context, lang, 
                                            '/unibe/content', 
                                            ContentModel.UniaktuellArticle))

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
                 where(date_after is None and True or (model.UniaktuellArticle.publish_dt_de > local_timezone(date_after))).
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
            'date': local_timezone(get_attr_by_lang(lang,
                                                    res.UniaktuellArticle.publish_dt_de,
                                                    res.UniaktuellArticle.publish_dt_en,
                                                    res.UniaktuellArticle.publish_dt_fr)).date(),
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
