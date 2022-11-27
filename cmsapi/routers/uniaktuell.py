from fastapi import APIRouter, Query
from sqlmodel import Session, select
from datetime import datetime
from ..db import engine

from ..models import uniaktuell as model
from ..schemas import uniaktuell as schema
from ..schemas.newsevents import Section
from ..helpers import Lang, strip_cmstest, get_attr_by_lang, get_uniaktuell_lang_str

from ..models.zmsobjects import ZMSSite

router = APIRouter(
    prefix="/v3",
    tags=["UniBE News and Events"])


@router.get("/uniaktuell", summary='Magazine articles', response_model=schema.UniaktuellArticleResponse,
            description='Magazine articles from <a href="https://www.uniaktuell.unibe.ch" '
                        'target="_blank">uniaktuell.unibe.ch</a>')
async def get_uniaktuell(
        lang: Lang = Lang.de,
        date: datetime | None = Query(None, description='Filter by date after (UTC)'),
        offset: int = 0,
        limit: int = 20):

    data = []

    with Session(engine) as session:
        statement = [select(model.UniaktuellArticle, ZMSSite).join(ZMSSite).
                     where(get_attr_by_lang(lang,
                                            de=model.UniaktuellArticle.active_de,
                                            en=model.UniaktuellArticle.active_en,
                                            fr=model.UniaktuellArticle.active_fr)).
                     where(ZMSSite.path.like('%uni%aktuell%')).
                     where(date is None and True or (model.UniaktuellArticle.publish_dt_de > date)).
                     order_by(get_attr_by_lang(lang,
                                               de=model.UniaktuellArticle.publish_dt_de,
                                               en=model.UniaktuellArticle.publish_dt_en,
                                               fr=model.UniaktuellArticle.publish_dt_fr).desc())]

        results = session.exec(statement[0].offset(offset).limit(limit))
        total = session.exec(statement[0])

        for res in results.all():
            if '/uniintern' in res.ZMSSite.path \
                    or '/zms_schulung' in res.ZMSSite.path \
                    or '/trashcan' in res.UniaktuellArticle.path:
                continue

            section = Section(
                type='/unibiblio' in res.ZMSSite.path and
                     'Library' or res.ZMSSite.type,  # overwrite deprecated type "Uniaktuell" of UB (Library)
                title=get_attr_by_lang(lang,
                                       de=res.ZMSSite.title_de,
                                       en=res.ZMSSite.title_en,
                                       fr=res.ZMSSite.title_fr),
                domain=f'https://{strip_cmstest(res.ZMSSite.domain)}',
                path=res.ZMSSite.path,
                uuid=res.ZMSSite.uuid
            )

            topics = [get_uniaktuell_lang_str(lang, get_attr_by_lang(lang,
                                                                     res.UniaktuellArticle.category_de,
                                                                     res.UniaktuellArticle.category_en,
                                                                     res.UniaktuellArticle.category_fr)),
                      get_uniaktuell_lang_str(lang, get_attr_by_lang(lang,
                                                                     res.UniaktuellArticle.topics_de,
                                                                     res.UniaktuellArticle.topics_en,
                                                                     res.UniaktuellArticle.topics_fr))]

            data.append(schema.UniaktuellArticle.parse_obj({
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
