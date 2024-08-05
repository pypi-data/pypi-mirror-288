# -*- coding: utf-8 -*-
"""
# ---------------------------------------------------------------------------------------------------------
# ProjectName:  mixiu-pytest-helper
# FileName:     infrastructure.py
# Description:  TODO
# Author:       mfkifhss2023
# CreateDate:   2024/07/31
# Copyright ©2011-2024. Hunan xxxxxxx Company limited. All rights reserved.
# ---------------------------------------------------------------------------------------------------------
"""
import typing as t
from apollo_proxy.client import ApolloClient
from mixiu_pytest_helper.config import apollo_params_map
from middleware_helper.redis import get_redis_connection, Redis

__all__ = ['apollo', 'RedisClientManager', 'RedisCacheClientManager', 'RedisLockClientManager']


class ApolloClientManager:

    def __new__(cls, *args, **kwargs):
        return ApolloClient(
            domain=apollo_params_map.get('domain'), namespace=apollo_params_map.get('namespace_name'),
            app_id=apollo_params_map.get('app_id'), cluster=apollo_params_map.get("cluster"),
            secret=apollo_params_map.get("secret")
        )


apollo = ApolloClientManager()


class RedisClientManager(object):

    def __init__(self, redis: Redis):
        self.redis = redis

    def get_redis_data(self, key: str) -> t.Any:
        return self.redis.get(key).decode("utf-8") if isinstance(self.redis.get(key), bytes) else self.redis.get(key)

    def set_redis_data(self, key: str, value: t.Any, ex: int = 3600) -> t.Any:
        return self.redis.set(name=key, value=value, ex=ex)


class RedisLockClientManager:
    def __new__(cls, *args, **kwargs):
        return get_redis_connection(**apollo.get_value("redis.lock"))


class RedisCacheClientManager:
    def __new__(cls, *args, **kwargs):
        return get_redis_connection(**apollo.get_value("redis.cache"))
