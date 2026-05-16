from fastapi import APIRouter, HTTPException

from zms.unibe.utils.zope.context import create_zope_app_context
from zms.unibe.fastapi.meta import Tags

from Products.zms.standard import get_installed_packages

router = APIRouter(prefix="/zms/system", tags=[Tags.system])


@router.get(
    path="/packages",
    summary="Get installed Python packages",
)
def get_installed_python_packages(

):
    packages = list(filter(lambda x:
                           len(x) > 0 and x[0] not in ('#', ''),
                           get_installed_packages().splitlines()))
    
    return {packages[0]: packages[1:]}


@router.get(
    path="/mappings",
    summary="Get virtual hosting mappings",
)
def get_virtual_hosting_mappings(

):
    context = create_zope_app_context()
    return context.virtual_hosting.lines


@router.post(
    path="/mappings",
    summary="Set virtual hosting mappings",
)
def set_virtual_hosting_mappings(
        mapping: str
):
    context = create_zope_app_context()
    mappings = '\n'.join(context.virtual_hosting.lines)
    
    context.virtual_hosting.set_map(mapping)
    if "#!" in context.virtual_hosting.lines[-1]:
        raise HTTPException(status_code=404,
                            detail=f"Set virtual hosting mapping failed.")
    mappings += '\n' + mapping
    
    # TODO: restrict access to change the mappings
    import transaction
    for attempt in transaction.attempts(3):
        with attempt as t:
            t.user = str('zms.unibe.fastapi')
            t.note('set_vhm_mappings')
            context.virtual_hosting.set_map(mappings)

    return context.virtual_hosting.lines

  
@router.get(
    path="/subdomains",
    summary="Get virtual hosting subdomains",
)
def get_virtual_hosting_subdomains(

):
    context = create_zope_app_context()
    return context.virtual_hosting.fixed_map


@router.get(
    path="/wildcards",
    summary="Get virtual hosting wildcards",
)
def get_virtual_hosting_wildcards(

):
    context = create_zope_app_context()
    return context.virtual_hosting.sub_map
