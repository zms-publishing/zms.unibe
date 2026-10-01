from fastapi import APIRouter, HTTPException
from typing import Optional
import json

from zms.unibe.fastapi.meta import Tags
from zms.unibe.utils .dependencies import CacheDependency

router = APIRouter(prefix="/cache", tags=[Tags.redis])


@router.post(
    path="/data/{key}",
    summary="Set a key-value pair in Redis Cache (with optional TTL)",
)
def set_cached_data(
        cache: CacheDependency,
        key: str,
        value: dict,
        ttl: Optional[int] = 60,  # default TTL of 60 seconds if not provided
):
    cache.set(key, json.dumps(value), ex=ttl)

    return {
        "status": "success",
        "message": f"Data for '{key}' successfully cached for {ttl} seconds.",
    }


@router.get(
    path="/data/{key}",
    summary="Get a key-value pair from Redis Cache",
)
def get_cached_data(
        cache: CacheDependency,
        key: str,
):
    cached_value = cache.get(key)

    if cached_value:
        return {
            "source": "cache",
            "key": key,
            "value": json.loads(cached_value),
        }

    raise HTTPException(status_code=404, detail=f"Key '{key}' not found in cache.")


@router.delete(
    path="/data/{key}",
    summary="Delete a key-value pair from Redis Cache",
)
def delete_cached_data(
        cache: CacheDependency,
        key: str,
):
    deleted = cache.delete(key)

    if deleted:
        return {
            "status": "success",
            "message": f"Key '{key}' deleted.",
        }

    raise HTTPException(status_code=404, detail=f"Key '{key}' did not exist.")
