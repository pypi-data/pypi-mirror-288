# -*- coding: utf-8 -*-
"""
# ---------------------------------------------------------------------------------------------------------
# ProjectName:  mixiu-pytest-helper
# FileName:     base_test.py
# Description:  TODO
# Author:       mfkifhss2023
# CreateDate:   2024/07/31
# Copyright ©2011-2024. Hunan xxxxxxx Company limited. All rights reserved.
# ---------------------------------------------------------------------------------------------------------
"""
import pytest
from mixiu_pytest_helper.annotation import logger
from airtest_helper.core import DeviceProxy, DeviceApi
from mixiu_pytest_helper.infrastructure import lock_client
from mixiu_pytest_helper.repository import MiddlewareRepository
from mixiu_app_helper.api.page.popup.gift import UiDailyCheckInApi
from mixiu_pytest_helper.conftest import get_idle_device, get_phone_device_lock_key


class SetupClass(object):

    @classmethod
    @pytest.fixture(scope="class")
    def init_setup(cls):
        logger.info("开始初始化自动化测试环境...")


class DataSetupClass(SetupClass):
    test_data: dict = dict()
    config_namespace = "test-data-app"

    @classmethod
    @pytest.fixture(scope="class")
    def data_setup(cls, init_setup: pytest.Function):
        cls.test_data = MiddlewareRepository.get_test_datas(namespace=cls.config_namespace)
        logger.info("step1: 获取apollo配置的测试【预期数据】成功")


class DeviceSetupClass(DataSetupClass):
    device: DeviceProxy = None

    @classmethod
    @pytest.fixture(scope="class")
    def device_setup(cls, data_setup: pytest.Function):
        # 此处的 setup 只会在每个测试类开始时调用一次
        cls.device = get_idle_device(redis_api=lock_client)
        if cls.device is None:
            logger.error("step2: 绑定移动终端设备失败，当前没有空闲设备，或者网络连接不正常")
        else:
            logger.info("step2: 绑定移动终端成功---> {}".format(cls.device.device_id))
        yield
        if cls.device:
            lock_key = get_phone_device_lock_key(device_ip=cls.device.device_id)
            lock_client.set_redis_data(key=lock_key, value="idle", ex=86400)


class AppSetupClass(DeviceSetupClass):
    app_name: str = 'null'
    device_api: DeviceApi = None

    @classmethod
    @pytest.fixture(scope="class")
    def app_setup(cls, device_setup: pytest.Function):
        cls.device_api = DeviceApi(device=cls.device)
        cls.app_name = cls.test_data.get('app_name')
        # logger.info("开始唤醒设备")
        # device_api.wake()  真机的可能处于息屏状态，因此需要唤醒，模拟机的话，可以忽略此步骤
        logger.info("step3: 开始启动APP---> {}".format(cls.app_name))
        cls.device_api.restart_app(app_name=cls.app_name)


class BeforeAppTest(AppSetupClass):

    @classmethod
    @pytest.fixture(scope="class", autouse=True)
    def before_test_setup(cls, app_setup: pytest.Function):
        popui_api = UiDailyCheckInApi(device=cls.device)
        signup_button = popui_api.get_signup_button()
        # 可能存在签到的弹窗
        if signup_button:
            logger.info("step4*: 检测到【每日签到】弹窗，关闭弹窗并退出直播室")
            popui_api.touch_signup_button()
            logger.info("step4.1*: 已签到")
            popui_api.touch_signup_submit_button()
            popui_api.touch_live_leave_enter()
            popui_api.touch_close_room_button()
            logger.info("step4.2*: 已退出直播间")
