from fastapi import APIRouter, HTTPException
from fastapi_cache.decorator import cache

from zms.unibe.fastapi.meta import Tags
from zms.unibe.utils.enums import VirtualHosting, PipCmd
from zms.unibe.utils.dependencies import ContextDependency

from Products.zms.standard import get_installed_packages
from Products.ZODBMountPoint.MountedObject import manage_getMountStatus

import re

router = APIRouter(prefix="/zms", tags=[Tags.system])


@router.get(
    path="/python/packages",
    summary="Get installed Python packages",
)
@cache(expire=60)
def get_installed_python_packages(
    mode: PipCmd = PipCmd.list,
):
    packages = list(filter(lambda x:
                           len(x) > 0 and x[0] not in ('#', ''),
                           get_installed_packages(pip_cmd=mode).splitlines()))
    
    if mode == PipCmd.freeze:
        return {
            'runtime': packages[0],
            'packages': packages[1:],
        }
    
    package_dict = {}

    for item in packages[3:]:
        # capture: package name + version, ignore anything after the version
        m = re.match(r"^\s*(.+?)\s+([0-9][^\s]*)", item)
        if m:
            name, version = m.groups()
            package_dict[name.strip()] = version.strip()
    
    return {
        'runtime': packages[0],
        'packages': package_dict,
    }

@router.get(
    path="/database/mounts",
    summary="Get mounted Zope Object Databases (ZODB)",
)
@cache(expire=60)
def get_zope_object_databases(
        context: ContextDependency,
):
    mounts = {}
    for zodb in context.Control_Panel.Database.getDatabaseNames():
        mount = context.Control_Panel.Database[zodb]
        mount_status = [x for x in manage_getMountStatus(mount) if x.get("name") == zodb]
        mounts[zodb] = {
            'zodb_location': mount.db_name(),
            'zodb_objects': mount.database_size(),
            'zodb_size': mount.db_size(),
            'zodb_mount': mount_status if mount_status else [{'path': '/',
                                                              'name': zodb,
                                                              'exists': 1,
                                                              'status': 'Ok',
                                                              }],
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
@cache(expire=60)
def get_virtual_hosting_mappings(
        context: ContextDependency,
        filter_by: VirtualHosting | None = None,
):
    flipped = False
    
    match filter_by:
        case 'subdomains':
            items = context.virtual_hosting.fixed_map.items()
        case 'wildcards':
            items = context.virtual_hosting.sub_map.items()
        case 'paths':
            items = {**context.virtual_hosting.fixed_map,
                     **context.virtual_hosting.sub_map}.items()
            flipped = True
        case _:
            return context.virtual_hosting.lines

    mappings = {
        ('*.'+host if host in context.virtual_hosting.sub_map.keys() else host):
            '/' + ('/'.join(reversed(mapping.get(None, [])))).replace('//', '')
        for host, mapping in items
    }

    if flipped:
        tmp = {}
        for host, path in mappings.items():
            tmp.setdefault(path, []).append(host)
        mappings = tmp
    
    return mappings

@router.post(
    path="/domain/mappings",
    summary="Set virtual host Domain/Path mappings",
)
def set_virtual_hosting_mappings(
        context: ContextDependency,
        mapping: str
):
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
