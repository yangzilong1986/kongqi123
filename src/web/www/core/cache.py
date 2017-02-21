# coding:utf-8

import redis


class RedisCache(object):
    def __init__(self, redis_client, pre_key=''):
        """

        :param redis_client:
        :param pre_key:
        :return:
        :type  redis_client redis.Redis
        """
        self.redis_client = redis_client
        self.pre_key = pre_key

    def get(self, key):
        return self.redis_client.get(key)

    def set(self, key, value, exp=3600):
        """
        缓存时间
        :param key:
        :param value:
        :param exp:
        :return:
        """
        self.redis_client.set(key, value)
        self.redis_client.expire(key, exp)

    def delete(self, key):
        """
        删除缓存
        @param key:
        @return:
        """
        return self.redis_client.delete(self, key)


_cache = {'redis_cache': None}


def redis_factory(config_name):
    """
    redis factory
    :param config_name:
    :return:
    :rtype: redis.Redis
    """
    import redis
    from config import redis_config
    return redis.from_url(redis_config[config_name])


def factory():
    """

    :return:RedisCache
    """
    if _cache['redis_cache'] is None:
        redis_client = redis_factory('cache')
        redis_cache = RedisCache(redis_client)
        _cache['redis_cache'] = redis_cache
    return _cache['redis_cache']


def test_redis():
    import time

    redis_cache = factory()
    key = 'test%s' % time.time()
    r = redis_cache.get(key)
    assert r is None
    redis_cache.set(key, key, 1)
    r2 = redis_cache.get(key)
    assert r2 == key
    time.sleep(1)
    r3 = redis_cache.get(key)
    assert r3 is None
