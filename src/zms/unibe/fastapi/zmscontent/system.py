import os

from fastapi import APIRouter, Query, HTTPException

from zms.unibe.utils.zope.context import create_zope_app_context, get_zmsindex
from zms.unibe.utils.enums import ContentModel
from zms.unibe.fastapi.meta import Tags

router = APIRouter(prefix="/zms/system", tags=[Tags.system])


@router.get(
    path="/packages",
    summary="Get installed Python packages",
)
def get_installed_python_packages(
        portal_master: str | None = Query(os.getenv('PORTAL_MASTER', '/myzmsx/content'),
                                          description="Portal master with ZMSIndex"),
):
    context = create_zope_app_context()
    zmsindex = get_zmsindex(portal_master, context)
    content = zmsindex.content
    
    packages_html = content.manage_customizeInstalledProducts()
    packages = packages_html.splitlines()
    packages = [content.zms_version(custom=True)] + packages
    # TODO: filter out HTML tags and other unwanted stuff
    
    return packages


@router.get(
    path="/models",
    summary="Get installed content models",
)
def get_installed_content_models(
        content_model: ContentModel | None = None,
        portal_master: str | None = Query(os.getenv('PORTAL_MASTER', '/myzmsx/content'),
                                          description="Portal master with ZMSIndex"),
):
    context = create_zope_app_context()
    zmsindex = get_zmsindex(portal_master, context)
    content = zmsindex.content
 
    metaobjs = {}
    for id in content.getMetaobjIds():
        data = {}
        data['revision'] = content.getMetaobjRevision(id)
        data['attributes'] = content.getMetaobjAttrs(id)
        metaobjs[id] = data

    if content_model in metaobjs:
        return {content_model: metaobjs[content_model]}
    elif content_model:
        raise HTTPException(status_code=404,
                            detail=f"Content model '{content_model.name}' not found.")
    return metaobjs


@router.get(
    path="/actions",
    summary="Get installed content actions",
)
def get_installed_content_actions(
        content_model: ContentModel | None = None,
        portal_master: str | None = Query(os.getenv('PORTAL_MASTER', '/myzmsx/content'),
                                          description="Portal master with ZMSIndex"),
):
    context = create_zope_app_context()
    zmsindex = get_zmsindex(portal_master, context)
    content = zmsindex.content

    metacmds = {}
    for id in content.getMetaCmdIds():
        data = {}
        data['revision'] = content.getMetaCmd(id).get('revision')
        data['package'] = content.getMetaCmd(id).get('package')
        data['description'] = content.getMetaCmdDescription(id)
        metacmds[id] = data

    if content_model in metacmds:
        return {content_model: metacmds[content_model]}
    elif content_model:
        raise HTTPException(status_code=404,
                            detail=f"Content model '{content_model.name}' not found.")
    return metacmds

