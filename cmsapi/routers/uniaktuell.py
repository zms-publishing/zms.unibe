from fastapi import APIRouter
from sqlmodel import Session, select
from ..db import engine

from ..models import uniaktuell as model
from ..schemas import uniaktuell as schema
from ..helpers import Lang, strip_cmstest, get_attr_by_lang

from ..models.zmsdefaults import ZMSSite

router = APIRouter(
    prefix="/v3/uniaktuell",
    tags=["Uniaktuell"]
)


@router.get("/articles", response_model=list[schema.UniaktuellArticle])
async def get_articles(
        lang: Lang = Lang.de,
        offset: int = 0,
        limit: int = 10):
    with Session(engine) as session:
        statement = select(model.UniaktuellArticle, ZMSSite).join(ZMSSite).\
            where(get_attr_by_lang(lang,
                                   de=model.UniaktuellArticle.active_de,
                                   en=model.UniaktuellArticle.active_en,
                                   fr=model.UniaktuellArticle.active_fr)).\
            offset(offset).limit(limit)
        results = session.exec(statement)
        rtn = []
        for res in results.all():
            print(res)
            rtn.append(schema.UniaktuellArticle.parse_obj({
                'uuid': res.UniaktuellArticle.uuid,
                'title': get_attr_by_lang(lang,
                                          res.UniaktuellArticle.title_de,
                                          res.UniaktuellArticle.title_en,
                                          res.UniaktuellArticle.title_fr),
                'site': strip_cmstest(res.ZMSSite.domain),
            }))
        return rtn
