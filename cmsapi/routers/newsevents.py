from fastapi import APIRouter
from sqlmodel import Session, select, or_
from datetime import datetime, timedelta
from ..db import engine

from ..models.newsevents import Newsbox, TeaserElement2022
from ..models.zmsdefaults import ZMSSite
from ..schemas import newsevents as schema
from ..helpers import Lang, get_attr_by_lang, strip_cmstest, local_timezone

router = APIRouter(
    prefix="/v3",
    tags=["News and Events"])


@router.get("/news", response_model=list[schema.News])
async def get_news(
        lang: Lang = Lang.de,
        days_back: int = 365,
        offset: int = 0,
        limit: int = 50):
    return retrieve("news", lang, days_back, offset, limit)


@router.get("/events", response_model=list[schema.Event])
async def get_events(
        lang: Lang = Lang.de,
        days_back: int = 365,
        offset: int = 0,
        limit: int = 10):
    return retrieve("event", lang, days_back, offset, limit)


def retrieve(type, lang, days_back, offset, limit):
    rtn = []
    statement = []
    with Session(engine) as session:
        for model in (TeaserElement2022, Newsbox):
            statement.append(
                select(model, ZMSSite).join(ZMSSite).
                where(model.type == type).
                where(or_(ZMSSite.type == 'Home',
                          ZMSSite.type == 'Fakultaet',
                          ZMSSite.type == 'Institut',
                          ZMSSite.type == 'Uniaktuell',  # to fetch UB
                          ZMSSite.type == 'Microsite')).
                where(get_attr_by_lang(lang,
                                       de=model.active_start_de,
                                       en=model.active_start_en,
                                       fr=model.active_start_fr) <= datetime.now()).
                where(get_attr_by_lang(lang,
                                       de=model.active_end_de,
                                       en=model.active_end_en,
                                       fr=model.active_end_fr) <= datetime.now()).
                where(get_attr_by_lang(lang,
                                       de=model.lastmod_dt_de,
                                       en=model.lastmod_dt_en,
                                       fr=model.lastmod_dt_fr) >= datetime.now() - timedelta(days=days_back)).
                where(get_attr_by_lang(lang,
                                       de=model.active_de,
                                       en=model.active_en,
                                       fr=model.active_fr))
            )

        query = statement[0].union(statement[1]). \
            order_by(TeaserElement2022.level,
                     Newsbox.level). \
            order_by(get_attr_by_lang(lang,
                                      de=TeaserElement2022.lastmod_dt_de,
                                      en=TeaserElement2022.lastmod_dt_en,
                                      fr=TeaserElement2022.lastmod_dt_fr).desc()). \
            order_by(get_attr_by_lang(lang,
                                      de=Newsbox.lastmod_dt_de,
                                      en=Newsbox.lastmod_dt_en,
                                      fr=Newsbox.lastmod_dt_fr).desc()). \
            alias('alias')

        results = session.query(query).offset(offset).limit(limit)

        if type == 'news':
            cls = schema.News
        else:
            cls = schema.Event

        for res in results:
            rtn.append(cls.parse_obj({
                'uuid': res.uuid,
                'title': get_attr_by_lang(lang,
                                          de=res.title_de,
                                          en=res.title_en,
                                          fr=res.title_fr),
                'topic': res.topic,
                'start_dt':
                    res.start_dt is not None and (
                    local_timezone(res.start_dt) or None) or None,
                'end_dt':
                    res.end_dt is not None and (
                    res.end_dt > datetime.fromisoformat('1970-01-01T00:00:00+00:00') and
                    local_timezone(res.end_dt) or None) or None,
                'level': res.level,
                'lastmod': get_attr_by_lang(lang,
                                            de=local_timezone(res.lastmod_dt_de),
                                            en=local_timezone(res.lastmod_dt_en),
                                            fr=local_timezone(res.lastmod_dt_fr)),
                'site': strip_cmstest(res.domain),
                'site_type': res.type_1,
                'subdomain': res.domain,
            }))

    return rtn
