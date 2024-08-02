# -*- coding: utf-8 -*-
"""
# ---------------------------------------------------------------------------------------------------------
# ProjectName:  mixiu-pytest-helper
# FileName:     annotation.py
# Description:  TODO
# Author:       mfkifhss2023
# CreateDate:   2024/07/31
# Copyright ©2011-2024. Hunan xxxxxxx Company limited. All rights reserved.
# ---------------------------------------------------------------------------------------------------------
"""
import traceback
from functools import wraps
from mixiu_pytest_helper.log import logger


def auto_log(func):
    """
    自动打印日志
    :param func:
    :return:
    """

    @wraps(func)
    def _deco(*args, **kwargs):
        try:
            real_func = func(*args, **kwargs)
            return real_func
        except Exception as e:
            logger.error(traceback.format_exc())
            string = f"调用入口函数：{func.__name__}失败。"
            if args or kwargs:
                logger.error(f"{string}传递参数：args->{args}，kwargs->{kwargs}。")
            return False, str(e)

    return _deco
