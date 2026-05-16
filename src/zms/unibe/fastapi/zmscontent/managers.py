import os

from fastapi import APIRouter, Query, HTTPException

from zms.unibe.utils.zope.context import create_zope_app_context, get_zmsindex
from zms.unibe.fastapi.meta import Tags
from zms.unibe.utils.enums import ContentModel

router = APIRouter(prefix="/zms/content", tags=[Tags.content])


@router.get(
    path="/models",
    summary="Get installed content models filtered by content model or substring in name or package",
)
def get_installed_content_models(
        portal_master: str | None = Query(os.getenv('PORTAL_MASTER', '/myzmsx/content'),
                                          description="Portal master with ZMSIndex"),
        content_model: ContentModel | None = None,
        substring: str | None = None,
):
    context = create_zope_app_context()
    zmsindex = get_zmsindex(portal_master, context)
    content = zmsindex.content
    
    metaobjs = {}
    for id in content.getMetaobjIds():
        data = {}
        data['revision'] = content.getMetaobjRevision(id)
        data['package'] = content.getMetaobj(id).get('package')
        data['attributes'] = content.getMetaobjAttrs(id)
        metaobjs[id] = data

    if substring is not None:
        metaobjs = dict(filter(lambda x:
                               substring.lower() in x[0].lower() or
                               substring.lower() in x[1]['package'].lower(),
                               metaobjs.items()))

    if content_model in metaobjs:
        return {content_model: metaobjs[content_model]}
    elif content_model:
        raise HTTPException(status_code=404,
                            detail=f"Content model '{content_model.name}' not found.")
    return metaobjs


@router.get(
    path="/actions",
    summary="Get installed content actions filtered by content model or substring in name or package",
)
def get_installed_content_actions(
        portal_master: str | None = Query(os.getenv('PORTAL_MASTER', '/myzmsx/content'),
                                          description="Portal master with ZMSIndex"),
        content_model: ContentModel | None = None,
        substring: str | None = None,
):
    context = create_zope_app_context()
    zmsindex = get_zmsindex(portal_master, context)
    content = zmsindex.content

    metacmds = {}
    for id in content.getMetaCmdIds():
        data = {}
        data['revision'] = content.getMetaCmd(id).get('revision')
        data['package'] = content.getMetaCmd(id).get('package')
        data['roles'] = content.getMetaCmd(id).get('roles')
        data['nodes'] = content.getMetaCmd(id).get('nodes')
        data['meta_types'] = content.getMetaCmd(id).get('meta_types')
        data['description'] = content.getMetaCmdDescription(id)
        metacmds[id] = data

    if substring is not None:
        metacmds = dict(filter(lambda x:
                               substring.lower() in x[0].lower() or
                               substring.lower() in x[1]['package'].lower(),
                               metacmds.items()))

    if content_model is not None:
        metacmds = dict(filter(lambda x:
                               content_model.value in x[1]['meta_types'] or
                               f'type({content_model.value})' in x[1]['meta_types'],
                               metacmds.items()))

    return metacmds