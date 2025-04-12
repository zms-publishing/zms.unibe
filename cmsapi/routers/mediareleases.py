from fastapi import APIRouter, Query
from sqlmodel import Session, select, not_
from datetime import datetime
from ..db import engine

from ..models import mediareleases as model
from ..schemas import mediareleases as schema
from ..schemas.newsevents import Section
from ..helpers import Lang, strip_cmstest, get_attr_by_lang

from ..models.zmsobjects import ZMSSite

router = APIRouter(
    prefix="/v3",
    tags=["UniBE News, Events and Announcements"])


@router.get("/mediareleases", summary='Media releases', response_model=schema.MediaReleaseResponse,
            description='Media releases from '
                        '<a href="https://www.unibe.ch/news/media_news/media_relations_e/media_releases" '
                        'target="_blank">unibe.ch/medien</a>')
async def get_mediareleases(
        lang: Lang = Lang.de,
        date_after: datetime | None = Query(None, description='Filter by date after (UTC)'),
        offset: int = 0,
        limit: int = 20):

    data = []

    with Session(engine) as session:
        statement = [select(model.MediaRelease, ZMSSite).join(ZMSSite).
                     where(get_attr_by_lang(lang,
                                            de=model.MediaRelease.active_de,
                                            en=model.MediaRelease.active_en,
                                            fr=model.MediaRelease.active_fr)).
                     where(not_(ZMSSite.path.contains('/arbeitgeberin'))).
                     where(not_(ZMSSite.path.contains('/images'))).
                     where(not_(ZMSSite.path.contains('/jahresberichte'))).
                     where(not_(ZMSSite.path.contains('/uniapp'))).
                     where(not_(ZMSSite.path.contains('/uniintern'))).
                     where(not_(ZMSSite.path.contains('/zms_schulung'))).
                     where(not_(model.MediaRelease.path.contains('/trashcan'))).
                     where(date_after is None and True or (model.MediaRelease.publish_dt_de > date_after)).
                     order_by(get_attr_by_lang(lang,
                                               de=model.MediaRelease.publish_dt_de,
                                               en=model.MediaRelease.publish_dt_en,
                                               fr=model.MediaRelease.publish_dt_fr).desc())]

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
                                          res.MediaRelease.title_de,
                                          res.MediaRelease.title_en,
                                          res.MediaRelease.title_fr),
                'date': get_attr_by_lang(lang,
                                         res.MediaRelease.publish_dt_de,
                                         res.MediaRelease.publish_dt_en,
                                         res.MediaRelease.publish_dt_fr),
                'infos': get_attr_by_lang(lang,
                                          res.MediaRelease.abstract_de,
                                          res.MediaRelease.abstract_en,
                                          res.MediaRelease.abstract_fr),
                'topics': get_attr_by_lang(lang,
                                           res.MediaRelease.topics_de,
                                           res.MediaRelease.topics_en,
                                           res.MediaRelease.topics_fr),
                'image': get_attr_by_lang(lang,
                                          res.MediaRelease.img_de,
                                          res.MediaRelease.img_en,
                                          res.MediaRelease.img_fr),
                'url': get_attr_by_lang(lang,
                                        res.MediaRelease.url_de,
                                        res.MediaRelease.url_en,
                                        res.MediaRelease.url_fr),
                'section': section,
                'dataSource': res.MediaRelease.path,
                'dataLevel': res.MediaRelease.level,
                'dataUuid': res.MediaRelease.uuid,
            }))

        return {
            'offset': offset,
            'limit': limit,
            'total': len(total.all()),
            'data': data
        }
