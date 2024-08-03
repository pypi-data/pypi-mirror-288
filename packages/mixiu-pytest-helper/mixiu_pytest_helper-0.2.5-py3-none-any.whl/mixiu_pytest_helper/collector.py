# -*- coding: utf-8 -*-
"""
# ---------------------------------------------------------------------------------------------------------
# ProjectName:  mixiu-pytest-helper
# FileName:     collector.py
# Description:  TODO
# Author:       mfkifhss2023
# CreateDate:   2024/08/03
# Copyright ©2011-2024. Hunan xxxxxxx Company limited. All rights reserved.
# ---------------------------------------------------------------------------------------------------------
"""
import os
import sys
from _pytest.config import Config
from _pytest.config import _prepareconfig


def collect_marks(collect_dir: str):
    # 将测试目录添加到 sys.path
    sys.path.insert(0, os.path.abspath(collect_dir))

    # 创建 pytest 配置对象
    def create_config(args=None) -> Config:
        """创建 pytest 配置对象"""
        config = _prepareconfig(args or [])
        return config

    # 运行 pytest 并获取测试项
    def collect_test_items(config: Config):
        """从 pytest 配置中收集测试项"""
        items = []
        for item in config.hook.pytest_collection_modifyitems(items):
            items.extend(item)
        return items

    # 打印测试函数的标记信息
    def print_marks():
        # 创建配置对象
        config = create_config(['--disable-warnings'])

        # 收集测试项
        items = collect_test_items(config)

        # 打印标记信息
        print("Collected Markers:")
        for item in items:
            if hasattr(item, 'keywords'):
                print(f"Test: {item.nodeid}")
                for marker in item.keywords:
                    print(f"  - Marker: {marker} -> {item.keywords[marker]}")

    print_marks()
