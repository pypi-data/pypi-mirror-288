# -*- coding: utf-8 -*-
"""
# ---------------------------------------------------------------------------------------------------------
# ProjectName:  mixiu-pytest-helper
# FileName:     dir.py
# Description:  TODO
# Author:       mfkifhss2023
# CreateDate:   2024/07/31
# Copyright ©2011-2024. Hunan xxxxxxx Company limited. All rights reserved.
# ---------------------------------------------------------------------------------------------------------
"""
import os
from mixiu_pytest_helper.config import logging_config, pytest_config, coverage_config
from airtest_helper.dir import get_project_path as get_exec_path, is_dir, join_path, is_exists, create_directory


def find_configuration_path(current_path):
    # 构造配置目录的完整路径
    config_path = join_path([current_path, "configuration"])

    if is_dir(file_path=str(config_path)):
        return current_path

    parent_path = os.path.dirname(current_path)

    # 如果到达根目录则返回 None
    if parent_path == current_path:
        return None

    return find_configuration_path(parent_path)


def get_project_path():
    # 执行文件所在的路径
    exec_path = get_exec_path()
    return find_configuration_path(exec_path) or exec_path


def save_file(content: str, file_path: str) -> None:
    if is_exists(file_name=file_path) is False:
        if is_dir(os.path.dirname(file_path)) is True:
            with open(file_path, 'w', encoding="utf-8") as f:
                f.write(content)


def delete_file(file_path: str):
    """删除指定路径的文件。"""
    try:
        if is_exists(file_name=file_path) is True:
            os.remove(file_path)
    except (Exception,):
        pass


def init_dir(project_path: str) -> None:
    config_dir = join_path([project_path, "configuration"])
    logging_template = str(join_path([config_dir, "logging.yaml"]))
    pytest_template = str(join_path([project_path, "pytest.ini"]))
    coverage_template = str(join_path([project_path, ".coveragerc"]))
    create_directory(dir_path=config_dir)
    save_file(content=logging_config, file_path=logging_template)
    save_file(content=pytest_config, file_path=pytest_template)
    save_file(content=coverage_config, file_path=coverage_template)
