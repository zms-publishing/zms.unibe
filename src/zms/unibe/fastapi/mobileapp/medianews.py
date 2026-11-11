from datetime import date

from fastapi import APIRouter, Query
from fastapi_cache.decorator import cache
from sqlmodel import not_, select

from ...announcements.schemas import MediaNewsSchema as schema
from ...announcements.sqlmodels import MediaNews as model
from ...fastapi.meta import Tags
from ...foundation.sqlmodels.ZMSSite import ZMSSite
from ...helpers import local_timezone
from ...mobileapp.schemas.NewsEventsSchema import Section
from ...utils.dependencies import SessionDependency
from ...utils.enums import Locale
from ...utils.zms2sql.getters import get_attr_by_lang, strip_cmstest

router = APIRouter(tags=[Tags.mobile])


@router.get("/medianews", summary='Media news', response_model=schema.MediaNewsResponse,
            description='Media news from '
                        '<a href="https://www.unibe.ch/news/media_news/media_relations_e/media_releases" '
                        'target="_blank">unibe.ch/medien</a>')
@cache(expire=600)
def get_medianews(
        session: SessionDependency,
        lang: Locale = Locale.de,
        date_after: date | None = Query(None, description='Filter by date after'),
        categories: list[str] | None = Query(None, description='Filter by categories'),
        offset: int = 0,
        limit: int = 20):

    data = []

    topics = get_attr_by_lang(lang,
                              de=model.MediaNews.topics_de,
                              en=model.MediaNews.topics_en,
                              fr=model.MediaNews.topics_fr)
    
    statement = (select(model.MediaNews, ZMSSite).join(ZMSSite).
                 where(get_attr_by_lang(lang,
                                        de=model.MediaNews.active_de,
                                        en=model.MediaNews.active_en,
                                        fr=model.MediaNews.active_fr)).
                 where(not_(ZMSSite.path.contains('/arbeitgeberin'))).
                 where(not_(ZMSSite.path.contains('/images'))).
                 where(not_(ZMSSite.path.contains('/jahresberichte'))).
                 where(not_(ZMSSite.path.contains('/uniapp'))).
                 where(not_(ZMSSite.path.contains('/uniintern'))).
                 where(not_(ZMSSite.path.contains('/zms_schulung'))).
                 where(not_(model.MediaNews.path.contains('/trashcan'))).
                 where(date_after is None and True or (model.MediaNews.publish_dt_de > local_timezone(date_after))).
                 order_by(get_attr_by_lang(lang,
                                           de=model.MediaNews.publish_dt_de,
                                           en=model.MediaNews.publish_dt_en,
                                           fr=model.MediaNews.publish_dt_fr).desc())
                 )

    if categories:
        results = session.exec(statement.where(topics.overlap(categories)).offset(offset).limit(limit))
        total = session.exec(statement.where(topics.overlap(categories)))
    else:
        results = session.exec(statement.offset(offset).limit(limit))
        total = session.exec(statement)

    for res in results.all():
        section = Section(
            type=res.ZMSSite.type,
            title=get_attr_by_lang(lang,
                                   de=res.ZMSSite.title_de,
                                   en=res.ZMSSite.title_en,
                                   fr=res.ZMSSite.title_fr),
            domain=f'https://{strip_cmstest(res.ZMSSite.domain)}',
            path=res.ZMSSite.path,
            categories=None,
            uuid=res.ZMSSite.uuid
        )

        categories = get_attr_by_lang(lang,
                                      de=res.MediaNews.topics_de,
                                      en=res.MediaNews.topics_en,
                                      fr=res.MediaNews.topics_fr)

        data.append(schema.MediaNews.model_validate({
            'title': get_attr_by_lang(lang,
                                      res.MediaNews.title_de,
                                      res.MediaNews.title_en,
                                      res.MediaNews.title_fr),
            'date': local_timezone(get_attr_by_lang(lang,
                                                    res.MediaNews.publish_dt_de,
                                                    res.MediaNews.publish_dt_en,
                                                    res.MediaNews.publish_dt_fr)).date(),
            'infos': get_attr_by_lang(lang,
                                      res.MediaNews.abstract_de,
                                      res.MediaNews.abstract_en,
                                      res.MediaNews.abstract_fr),
            'categories': categories,
            'topics': ', '.join(categories) if categories is not None else None,
            'image': get_attr_by_lang(lang,
                                      res.MediaNews.img_de,
                                      res.MediaNews.img_en,
                                      res.MediaNews.img_fr),
            'url': get_attr_by_lang(lang,
                                    res.MediaNews.url_de,
                                    res.MediaNews.url_en,
                                    res.MediaNews.url_fr),
            'section': section,
            'dataSource': res.MediaNews.path,
            'dataLevel': res.MediaNews.level,
            'dataUuid': res.MediaNews.uuid,
        }))

    return {
        'offset': offset,
        'limit': limit,
        'total': len(total.all()),
        'data': data
    }
