from Products.mcdutils.mapping import MemCacheMapping

print('Monkeypatch: Products.mcdutils.mapping.MemCacheMapping.tpc_vote')
"""
Avoid raise exception if Memcached connection fails and log instead
- Connection errors suddenly occur only with cluster setup in Docker Swarm mode
- Docker Swarm networking seems to kill idle TCP connections after a while (15min?)
- Memcached is alive and can be reconnected

https://forums.docker.com/t/tcp-timeout-that-occurs-only-in-docker-swarm-not-simple-docker-run/58179
https://github.com/zulip/zulip/issues/14455#issuecomment-609472979
https://docs.docker.com/network/overlay/#bypass-the-routing-mesh-for-a-swarm-service
https://news.ycombinator.com/item?id=25328865
"""

def tpc_vote(self, txn):
    """ See IDataManager.
    """
    server, key = self._p_proxy.client._get_server(self._p_key)
    if server is None:
        from Products.mcdutils import MemCacheError
        # raise MemCacheError("Can't reach memcache server!")
        import logging
        LOGGER = logging.getLogger('Products.mcdutils')
        LOGGER.log(logging.ERROR, MemCacheError("Can't reach memcache server!"))

MemCacheMapping.tpc_vote = tpc_vote
