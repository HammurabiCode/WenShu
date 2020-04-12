__all__ = ['get_proxy_redis_conn']

from redis import ConnectionPool, StrictRedis
from rediscluster import RedisCluster

from src.utils.cfg import proxy_redis_host, proxy_redis_auth, proxy_redis_db
startup_nodes = [
    {'host': host.split(':')[0], 'port': host.split(':')[1] if ':' in host else '6379'}
    for host in proxy_redis_host.split(';')
]

_kwargs = {'decode_responses': True, 'encoding': 'utf-8'}

proxy_redis_conn = None
try:
    proxy_redis_conn = RedisCluster(startup_nodes=startup_nodes, **_kwargs)
    proxy_redis_conn.execute_command('auth {}'.format(proxy_redis_auth))
    proxy_redis_conn.execute_command('select {}'.format(proxy_redis_db))
except Exception as e:
    proxy_redis_conn = None
    url = 'redis://{}@{}/{}'.format(
        ':'+proxy_redis_auth if proxy_redis_auth else '',
        proxy_redis_host,
        proxy_redis_db,
    )
    redis_pool = ConnectionPool.from_url(url, **_kwargs)


def get_proxy_redis_conn():
    return proxy_redis_conn or StrictRedis(connection_pool=redis_pool)
