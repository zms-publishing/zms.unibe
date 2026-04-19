from datetime import datetime

from fastapi import APIRouter, Query
from sqlmodel import Session, not_, select

from zms.unibe.announcements.schemas import MediaReleasesSchema as schema
from zms.unibe.announcements.sqlmodels import MediaNews as model
from zms.unibe.fastapi.meta import Tags
from zms.unibe.foundation.sqlmodels.ZMSSite import ZMSSite
from zms.unibe.mobileapp.schemas.NewsEventsSchema import Section
from zms.unibe.utils.db import connect_sqldb
from zms.unibe.utils.enums import Locale
from zms.unibe.utils.helpers import get_attr_by_lang, strip_cmstest

router = APIRouter(tags=[Tags.mobile])


@router.get("/mediareleases", summary='Media releases', response_model=schema.MediaReleaseResponse,
            description='Media releases from '
                        '<a href="https://www.unibe.ch/news/media_news/media_relations_e/media_releases" '
                        'target="_blank">unibe.ch/medien</a>')
async def get_mediareleases(
        lang: Locale = Locale.de,
        date_after: datetime | None = Query(None, description='Filter by date after (UTC)'),
        offset: int = 0,
        limit: int = 20):

    data = []

    with Session(connect_sqldb()) as session:
        statement = [select(model.MediaNews, ZMSSite).join(ZMSSite).
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
                     where(date_after is None and True or (model.MediaNews.publish_dt_de > date_after)).
                     order_by(get_attr_by_lang(lang,
                                               de=model.MediaNews.publish_dt_de,
                                               en=model.MediaNews.publish_dt_en,
                                               fr=model.MediaNews.publish_dt_fr).desc())]

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

            data.append(schema.MediaRelease.model_validate({
                'title': get_attr_by_lang(lang,
                                          res.MediaNews.title_de,
                                          res.MediaNews.title_en,
                                          res.MediaNews.title_fr),
                'date': get_attr_by_lang(lang,
                                         res.MediaNews.publish_dt_de,
                                         res.MediaNews.publish_dt_en,
                                         res.MediaNews.publish_dt_fr),
                'infos': get_attr_by_lang(lang,
                                          res.MediaNews.abstract_de,
                                          res.MediaNews.abstract_en,
                                          res.MediaNews.abstract_fr),
                'topics': get_attr_by_lang(lang,
                                           res.MediaNews.topics_de,
                                           res.MediaNews.topics_en,
                                           res.MediaNews.topics_fr),
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
