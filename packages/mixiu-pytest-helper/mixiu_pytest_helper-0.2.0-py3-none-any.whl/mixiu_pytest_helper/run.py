# -*- coding: utf-8 -*-
"""
# ---------------------------------------------------------------------------------------------------------
# ProjectName:  mixiu-pytest-helper
# FileName:     run.py
# Description:  TODO
# Author:       mfkifhss2023
# CreateDate:   2024/07/31
# Copyright ©2011-2024. Hunan xxxxxxx Company limited. All rights reserved.
# ---------------------------------------------------------------------------------------------------------
"""
import sys
import pytest
import pytest_cov
import logging.config
from allure_pytest.utils import ALLURE_DESCRIPTION_MARK
from distributed_logging.parse_yaml import ProjectConfig
from pytest_html.__version import version as html_version
from airtest_helper.dir import join_path, create_directory
from mixiu_pytest_helper.dir import get_project_path, save_file
from pytest_metadata.__version import version as metadata_version
from mixiu_pytest_helper.config import logging_config, pytest_config


def run_tests(script_path: str = None, report_type: str = ALLURE_DESCRIPTION_MARK):
    project_path = get_project_path()
    config_dir = join_path([project_path, "configuration"])
    logging_template = str(join_path([config_dir, "logging.yaml"]))
    pytest_template = str(join_path([project_path, "pytest.ini"]))
    create_directory(dir_path=config_dir)
    save_file(content=logging_config, file_path=logging_template)
    save_file(content=pytest_config, file_path=pytest_template)
    config = ProjectConfig(project_home=get_project_path()).get_object()
    logging_plus = getattr(config, "logging")
    logging.config.dictConfig(logging_plus)
    pytest_args = list()
    pytest_plugins = list()
    if (report_type == ALLURE_DESCRIPTION_MARK and pytest_cov.__version__ >= '5.0.0' and
            html_version >= '4.1.1' and metadata_version >= '3.1.1'):
        allure_dir = join_path([project_path, "allure-results"])
        pytest_plugins.extend(['allure_pytest', 'pytest_cov', 'pytest_html', 'pytest_metadata'])
        pytest_args.extend(['--alluredir={}'.format(allure_dir), '--cov-report=html'])
    if script_path is not None:
        if script_path == "__main__":
            script_path = sys.argv[0]
        pytest_args.append(script_path)
    pytest.main(args=pytest_args, plugins=pytest_plugins)
