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
from mixiu_pytest_helper.repository import MiddlewareRepository
from mixiu_app_helper.api.page.popup.gift import UiDailyCheckInApi


class BaseTest(object):
    pass


class AppBaseTest(BaseTest):
    test_data: dict = dict()
    app_name: str = 'null'
    config_namespace = "test-data-app"
    device: DeviceProxy = None
    device_api: DeviceApi = None

    @classmethod
    @pytest.fixture(scope="class", autouse=True)
    def base_setup(cls, request: pytest.FixtureRequest, device_context: DeviceProxy):
        test_data = MiddlewareRepository.get_test_datas(namespace=cls.config_namespace)
        device_api = DeviceApi(device=device_context)
        request.cls.test_data = test_data
        request.cls.app_name = test_data.get('app_name')
        # logger.info("开始唤醒设备")
        # device_api.wake()  真机的可能处于息屏状态，因此需要唤醒，模拟机的话，可以忽略此步骤
        logger.info("开始启动APP: {}".format(request.cls.app_name))
        device_api.restart_app(app_name=request.cls.app_name)


class AppBeforeTest(AppBaseTest):

    @classmethod
    @pytest.fixture(scope="class", autouse=True)
    def before_setup(cls, device_context: DeviceProxy):
        popui_api = UiDailyCheckInApi(device=device_context)
        signup_button = popui_api.get_signup_button(
            loop=20, peroid=0.5, is_ignore=True, is_log_output=True, is_log_traceback=True
        )
        # 可能存在签到的弹窗
        if signup_button:
            logger.info("APP打开后，出现了【每日签到】弹窗")
            popui_api.touch_signup_button(
                loop=20, peroid=0.5, is_ignore=True, is_log_output=True, is_log_traceback=True
            )
            logger.info("已签到")
            popui_api.touch_signup_submit_button(
                loop=20, peroid=0.5, is_ignore=True, is_log_output=True, is_log_traceback=True
            )
            popui_api.touch_live_leave_enter(
                loop=20, peroid=0.5, is_ignore=True, is_log_output=True, is_log_traceback=True
            )
            popui_api.touch_close_room_button(
                loop=20, peroid=0.5, is_ignore=True, is_log_output=True, is_log_traceback=True
            )
            logger.info("已退出直播间")
