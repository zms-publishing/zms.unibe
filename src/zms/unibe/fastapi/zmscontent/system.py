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
    path="/database/mounts",
    summary="Get mounted Zope Object Databases (ZODB)",
)
def get_zope_object_databases():
    context = create_zope_app_context()
    mounts = {}
    for zodb in context.Control_Panel.Database.getDatabaseNames():
        mount = context.Control_Panel.Database[zodb]
        mount_status = [x for x in manage_getMountStatus(mount) if x.get("name") == zodb]
        mounts[zodb] = {
            'zodb_location': mount.db_name(),
            'zodb_objects': mount.database_size(),
            'zodb_size': mount.db_size(),
            'zodb_mount': mount_status if len(mount_status)>0 else {'path': '/', 
                                                                    'name': zodb,
                                                                    'exists': 1,
                                                                    'status': 'Ok',
                                                                    },
            'cache_size': mount.cache_size(),
            'cache_length': mount.cache_length(),
            'cache_length_bytes': mount.cache_length_bytes(),
            'cache_active_and_inactive_count': mount.cache_active_and_inactive_count(),
        }
    return mounts


@router.get(
    path="/domain/mappings",
    summary="Get virtual host Domain/Path mappings",
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
