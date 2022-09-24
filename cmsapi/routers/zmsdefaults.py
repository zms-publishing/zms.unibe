from fastapi import APIRouter
from sqlmodel import Session, select
from ..db import engine

from ..models import zmsdefaults as model
from ..schemas import zmsdefaults as schema
from ..helpers import strip_cmstest

router = APIRouter(
    prefix="/v3/zms",
    tags=["ZMS Defaults"]
)


@router.get("/subdomains", response_model=list[schema.ZMSSite])
async def get_subdomains(
        offset: int = 0,
        limit: int = 10):
    with Session(engine) as session:
        statement = select(model.ZMSSite). \
            where(model.ZMSSite.domain != ''). \
            order_by(model.ZMSSite.domain). \
            offset(offset).limit(limit)
        results = session.exec(statement)
        rtn = []
        for res in results.all():
            rtn.append(schema.ZMSSite.parse_obj({
                'site': strip_cmstest(res.domain),
                'subdomain': res.domain,
            }))
        return rtn


@router.get("/documents/{site}", response_model=list[model.ZMSDocument])
async def get_documents_by_site(
        site: str,
        offset: int = 0,
        limit: int = 10):
    with Session(engine) as session:
        statement = select(model.ZMSDocument).join(model.ZMSSite). \
            where(model.ZMSSite.domain == strip_cmstest(site, reverse=True)). \
            offset(offset).limit(limit)
        results = session.exec(statement)
        return results.all()


@router.get("/folders/{site}", response_model=list[model.ZMSFolder])
async def get_folders_by_site(
        site: str,
        offset: int = 0,
        limit: int = 10):
    with Session(engine) as session:
        statement = select(model.ZMSFolder).join(model.ZMSSite). \
            where(model.ZMSSite.domain == strip_cmstest(site, reverse=True)). \
            offset(offset).limit(limit)
        results = session.exec(statement)
        return results.all()


@router.get("/forms/{site}", response_model=list[model.ZMSFormulator])
async def get_forms_by_site(
        site: str,
        offset: int = 0,
        limit: int = 10):
    with Session(engine) as session:
        statement = select(model.ZMSFormulator).join(model.ZMSSite). \
            where(model.ZMSSite.domain == strip_cmstest(site, reverse=True)). \
            offset(offset).limit(limit)
        results = session.exec(statement)
        return results.all()


@router.get("/datatables", response_model=list[schema.ZMSDataTable])
async def get_datatables(
        offset: int = 0,
        limit: int = 100):
    with Session(engine) as session:
        statement = select(model.ZMSDataTable, model.ZMSSite).join(model.ZMSSite). \
            offset(offset).limit(limit)
        results = session.exec(statement)
        print(statement)
        rtn = []
        for res in results.all():
            rtn.append(schema.ZMSDataTable.parse_obj({
                'site': strip_cmstest(res.ZMSSite.domain),
                'url': res.ZMSDataTable.dataurl,
            }))
        return rtn
