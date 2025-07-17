import os
import traceback
from enum import Enum
from uuid import UUID

import ZODB
import xmltodict
import zodburi
from devtools import debug
from fastapi import APIRouter, Response, HTTPException
from zope.globalrequest import setRequest

from zms.unibe.utils.headless import create_headless_http_request

ZODB_STORAGE = os.getenv('ZODB_STORAGE', 'zeo://127.0.0.1:8000?storage=main')

router = APIRouter(
    prefix="/v1/zms",
    tags=["ZMS Content"],
    include_in_schema=True
)


class ResponseData(str, Enum):
    xml = 'xml'
    json = 'json'


@router.get("/content")
def get_content(
        path: str = '/myzmsx/content/e12/',  # TODO: adjust default value
        uuid: UUID = None,
        deep: bool = False,
        data: ResponseData = ResponseData.xml):

    factory, dbargs = zodburi.resolve_uri(ZODB_STORAGE)  # TODO: refactor in ..db according to ..admin.db
    connection = ZODB.connection(factory(), **dbargs)
    root = connection.root()
    zmsindex = root['Application']['unibe']['zcatalog_index']  # TODO: make flexible - e.g. use myzmsx instead of unibe
    zodb = root['Application']

    headless_http_request = create_headless_http_request()  # TODO: refactor to use in helpers instead of duplicate
    # Set defaults
    headless_http_request.set('ZMS_CONTEXT_URL', True)
    # Set headless_http_request via zope.globalrequest.setRequest.
    # The ZMS uses the zope.globalrequest.getRequest as a fallback.
    setRequest(headless_http_request)

    if uuid is not None:
        try:
            zodb = zmsindex({'get_uid': f'uid:{uuid}'})[0].getObject()
        except Exception as e:
            debug(uuid)
            traceback.print_exc()
            raise HTTPException(status_code=404, detail="Item not found")
    else:
        for item in path.split('/'):
            if item.strip() in ('', 'uniintern', 'portal'):  # TODO: handle portal properly - avoid export of whole site by overriding deep
                continue
            if item not in zodb:
                raise HTTPException(status_code=404, detail="Item not found")
            zodb = zodb[item]

    xml = zodb.toXml(deep=deep)

    if data == 'xml':
        return Response(content=xml, media_type="application/xml")
    else:
        return [xmltodict.parse(xml)]
