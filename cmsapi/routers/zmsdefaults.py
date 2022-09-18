from fastapi import APIRouter
from sqlmodel import Session, select
from ..db import engine

from ..models import zmsdefaults as model
from ..schemas import zmsdefaults as schema
from ..helpers import parse_subdomain

router = APIRouter(
    prefix="/v3/zms",
    tags=["ZMS Defaults"]
)


@router.get("/sites", response_model=list[schema.ZMSSite])
async def get_sites(
        offset: int = 0,
        limit: int = 100):
    with Session(engine) as session:
        statement = select(model.ZMSSite).offset(offset).limit(limit)
        results = session.exec(statement)
        rtn = []
        for res in results.all():
            subdomain = parse_subdomain(res.domain)
            if subdomain != '':
                rtn.append(schema.ZMSSite.parse_obj({
                    'subdomain': subdomain
                }))
        return rtn


@router.get("/documents", response_model=list[model.ZMSDocument])
async def get_documents(
        offset: int = 0,
        limit: int = 100):
    with Session(engine) as session:
        statement = select(model.ZMSDocument).offset(offset).limit(limit)
        results = session.exec(statement)
        return results.all()


@router.get("/folders", response_model=list[model.ZMSFolder])
async def get_folders(
        offset: int = 0,
        limit: int = 100):
    with Session(engine) as session:
        statement = select(model.ZMSFolder).offset(offset).limit(limit)
        results = session.exec(statement)
        return results.all()
