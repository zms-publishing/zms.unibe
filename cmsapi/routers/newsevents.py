from fastapi import APIRouter
from sqlmodel import Session, select, or_
from datetime import datetime
from ..db import engine

from ..models.newsevents import Newsbox, TeaserElement2022
from ..models.zmsdefaults import ZMSSite
from ..schemas import newsevents as schema
from ..helpers import Lang, SiteType, get_attr_by_lang, strip_cmstest

router = APIRouter(
    prefix="/v3",
    tags=["News and Events"])


@router.get("/newsevents/sites", response_model=list[schema.Site])
async def get_sites_with_news_events(
        lang: Lang = Lang.de,
        type: SiteType = SiteType.Home,
        offset: int = 0,
        limit: int = 10):
    with Session(engine) as session:
        statement = select(ZMSSite).join(Newsbox). \
            where(ZMSSite.domain != ''). \
            where(ZMSSite.type == type). \
            where(or_(Newsbox.type == 'news', Newsbox.type == 'event')). \
            where(get_attr_by_lang(lang, de=ZMSSite.active_de, en=ZMSSite.active_en, fr=ZMSSite.active_fr)). \
            order_by(ZMSSite.domain). \
            offset(offset).limit(limit).distinct()
        results = session.exec(statement)
        rtn = []
        for res in results.all():
            rtn.append(schema.Site.parse_obj({
                'uuid': res.uuid,
                'site': strip_cmstest(res.domain),
                'type': res.type,
                'title': get_attr_by_lang(lang, de=res.title_de, en=res.title_en, fr=res.title_fr),
                'subdomain': res.domain,
            }))
        return rtn


@router.get("/news/{site}", response_model=list[schema.News])
async def get_news_by_site(
        site: str,
        lang: Lang = Lang.de,
        offset: int = 0,
        limit: int = 10):
    return query_news_events("news", site, lang, offset, limit)


@router.get("/events/{site}", response_model=list[schema.Event])
async def get_events_by_site(
        site: str,
        lang: Lang = Lang.de,
        offset: int = 0,
        limit: int = 10):
    return query_news_events("event", site, lang, offset, limit)


def query_news_events(type, site, lang, offset, limit):
    rtn = []
    statement = []
    with Session(engine) as session:
        for model in (TeaserElement2022, Newsbox):
            statement.append(
                select(model).join(ZMSSite).
                where(ZMSSite.domain == strip_cmstest(site, reverse=True)).
                where(model.type == type).
                where(get_attr_by_lang(lang,
                                       de=model.active_start_de,
                                       en=model.active_start_en,
                                       fr=model.active_start_fr) <= datetime.now()).
                where(get_attr_by_lang(lang,
                                       de=model.active_end_de,
                                       en=model.active_end_en,
                                       fr=model.active_end_fr) <= datetime.now()).
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
                'title': get_attr_by_lang(lang, de=res.title_de, en=res.title_en, fr=res.title_fr),
                'level': res.level,
                'lastmod': get_attr_by_lang(lang, de=res.lastmod_dt_de, en=res.lastmod_dt_en, fr=res.lastmod_dt_fr)
            }))

    return rtn
