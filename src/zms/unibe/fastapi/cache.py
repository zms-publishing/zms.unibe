from fastapi import APIRouter, HTTPException
from typing import Optional
import json

from zms.unibe.fastapi.meta import Tags
from zms.unibe.utils .dependencies import CacheDependency

router = APIRouter(prefix="/cache", tags=[Tags.redis])


@router.post(
    path="/{prefix}/{key}",
    summary="Set a key-value pair with a prefix in Redis Cache (with optional TTL in seconds)",
)
def set_cached_value(
        cache: CacheDependency,
        prefix: str,
        key: str,
        value: dict = {'data': 'demo'},
        ttl: Optional[int] = None,
        overwrite: Optional[bool] = False,
):
    prefix_key = f"{prefix}:{key}"
    if not overwrite and cache.get(prefix_key):
        raise HTTPException(
            status_code=400,
            detail=f"Key '{prefix_key}' already exists. Set 'overwrite=True' to update.",
        )

    cache.set(prefix_key, json.dumps(value), ex=None if ttl==0 else ttl, nx=not overwrite)
    expiry = f"for {ttl} seconds" if ttl else "indefinitely"

    return {
        "status": "success",
        "message": f"Value for '{prefix_key}' successfully cached {expiry}.",
    }


@router.get(
    path="/{prefix}/{key}",
    summary="Get a key-value pair with a prefix from Redis Cache",
)
def get_cached_value(
        cache: CacheDependency,
        prefix: str,
        key: str,
):
    prefix_key = f"{prefix}:{key}"
    cached_value = cache.get(prefix_key)

    if cached_value:
        return {
            "prefix": prefix,
            "key": key,
            "value": json.loads(cached_value),
        }

    raise HTTPException(
        status_code=404,
        detail=f"Key '{prefix_key}' not found in cache."
    )


@router.delete(
    path="/{prefix}/{key}",
    summary="Delete a key-value pair with a prefix from Redis Cache",
)
def delete_cached_value(
        cache: CacheDependency,
        prefix: str,
        key: str,
):
    prefix_key = f"{prefix}:{key}"
    deleted = cache.delete(prefix_key)

    if deleted:
        return {
            "status": "success",
            "message": f"Key '{prefix_key}' deleted.",
        }

    raise HTTPException(
        status_code=404,
        detail=f"Key '{prefix_key}' does not exist."
    )
