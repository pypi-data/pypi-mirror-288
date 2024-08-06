# -*- coding: utf-8 -*-
"""
# ---------------------------------------------------------------------------------------------------------
# ProjectName:  mixiu-pytest-helper
# FileName:     repository.py
# Description:  TODO
# Author:       mfkifhss2023
# CreateDate:   2024/07/31
# Copyright ©2011-2024. Hunan xxxxxxx Company limited. All rights reserved.
# ---------------------------------------------------------------------------------------------------------
"""
import typing as t

from mixiu_pytest_helper.infrastructure import apollo


class MiddlewareRepository(object):

    @classmethod
    def get_devices(cls) -> list:
        return apollo.get_value(key="device_ids") or list()

    @classmethod
    def get_test_data(cls, key: str, namespace: str) -> t.Any:
        return apollo.get_value(key=key, namespace=namespace)

    @classmethod
    def get_test_datas(cls, namespace: str) -> dict:
        test_datas = apollo.get_all_values(namespace=namespace)
        return test_datas if isinstance(test_datas, dict) else dict()
