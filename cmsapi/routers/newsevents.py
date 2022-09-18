from fastapi import APIRouter
from sqlmodel import Session, select
from datetime import datetime
from ..db import engine

from ..models.newsevents import Newsbox
from ..models.zmsdefaults import ZMSSite

router = APIRouter(
    prefix="/v3",
    tags=["News and Events"])


@router.get("/news/{site}", response_model=list[Newsbox])
async def get_news_by_site(
        site: str,
        offset: int = 0,
        limit: int = 10):
    with Session(engine) as session:
        domain = site == 'portal' and 'www.cmstest1.unibe.ch' or f'www.{site}.cmstest1.unibe.ch'
        statement = select(Newsbox).join(ZMSSite).\
            where(ZMSSite.domain == domain).\
            where(Newsbox.boxtype == "news").\
            where(Newsbox.attr_event_start > datetime(2000, 1, 1)).\
            offset(offset).limit(limit)
        results = session.exec(statement)
        return results.all()


@router.get("/events/{site}", response_model=list[Newsbox])
async def get_events_by_site(
        site: str,
        offset: int = 0,
        limit: int = 10):
    with Session(engine) as session:
        domain = site == 'portal' and 'www.cmstest1.unibe.ch' or f'www.{site}.cmstest1.unibe.ch'
        statement = select(Newsbox).join(ZMSSite).\
            where(ZMSSite.domain == domain).\
            where(Newsbox.boxtype == "event").\
            order_by(Newsbox.attr_event_start.desc()).\
            offset(offset).limit(limit)
        results = session.exec(statement)
        return results.all()
