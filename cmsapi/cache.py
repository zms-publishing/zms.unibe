from flask_caching import Cache
import os

CACHE_BACKEND = os.getenv('CACHE_BACKEND', 'SimpleCache')
CACHE_TIMEOUT = os.getenv('CACHE_TIMEOUT', 60)
CACHE_SERVERS = os.getenv('CACHE_SERVERS', '')  # used for MemcachedCache
CACHE_STORAGE = os.getenv('CACHE_STORAGE', '')  # used for FileSystemCache

print(CACHE_BACKEND, CACHE_SERVERS, CACHE_TIMEOUT, CACHE_STORAGE)

cache = Cache(config={'CACHE_TYPE': CACHE_BACKEND,
                      'CACHE_DEFAULT_TIMEOUT': int(CACHE_TIMEOUT),
                      'CACHE_MEMCACHED_SERVERS': [CACHE_SERVERS],
                      'CACHE_DIR': CACHE_STORAGE,
                      })
