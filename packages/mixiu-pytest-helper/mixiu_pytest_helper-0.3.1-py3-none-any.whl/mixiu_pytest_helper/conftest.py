# -*- coding: utf-8 -*-
"""
# ---------------------------------------------------------------------------------------------------------
# ProjectName:  mixiu-pytest-helper
# FileName:     conftest.py
# Description:  TODO
# Author:       mfkifhss2023
# CreateDate:   2024/07/31
# Copyright ©2011-2024. Hunan xxxxxxx Company limited. All rights reserved.
# ---------------------------------------------------------------------------------------------------------
"""
import sys
import pytest
from airtest_helper.core import DeviceProxy
from mixiu_pytest_helper.annotation import logger
from mixiu_pytest_helper.repository import MiddlewareRepository
from mixiu_pytest_helper.infrastructure import RedisCacheClientManager, RedisLockClientManager, RedisClientManager


def get_phone_device_lock_key(device_ip: str, port: int = None) -> str:
    string = "phone:{}".format(device_ip)
    if port and port > 0:
        string += ":{}".format(port)
    return string


def get_redis_lock_api() -> RedisClientManager:
    redis_client = RedisLockClientManager()
    redis_api = RedisClientManager(redis=redis_client)
    return redis_api


def get_idle_device(redis_api: RedisClientManager) -> DeviceProxy or None:
    devices = MiddlewareRepository.get_devices()
    for device_info in devices:
        port = device_info.get("port")
        device_ip = device_info.get("device")
        lock_key = get_phone_device_lock_key(device_ip=device_ip, port=port)
        lock_status = redis_api.get_redis_data(key=lock_key)
        if not lock_status or lock_status != "running":
            try:
                # 重置 sys.argv 为新的参数列表，避免与airtest包冲突，同时保留当前运行的文件名，作为sys.argv的第一个参数
                sys.argv = sys.argv[:1]
                device = DeviceProxy(**device_info)
                redis_api.set_redis_data(key=lock_key, value="running", ex=7200)
                return device
            except Exception as e:
                logger.error(e)
    return None


@pytest.fixture(scope="session")
def device_context() -> tuple:
    redis_api = get_redis_lock_api()
    device = get_idle_device(redis_api=redis_api)
    yield device
    if device:
        lock_key = get_phone_device_lock_key(device_ip=device.device_id)
        redis_api.set_redis_data(key=lock_key, value="idle", ex=86400)
    redis_api.redis.close()


@pytest.fixture(scope="session")
def redis_context() -> RedisClientManager:
    redis_client = RedisCacheClientManager()
    redis_api = RedisClientManager(redis=redis_client)
    yield redis_api
    redis_api.redis.close()
