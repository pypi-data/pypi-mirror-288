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
import os
import sys
import pytest
import pytest_cov
import logging.config
from airtest_helper.dir import join_path
from mixiu_pytest_helper.dir import init_dir
from allure_pytest.utils import ALLURE_DESCRIPTION_MARK
from distributed_logging.parse_yaml import ProjectConfig
from pytest_html.__version import version as html_version
from pytest_metadata.__version import version as metadata_version


def run_tests(project_path: str = None, report_type: str = ALLURE_DESCRIPTION_MARK):
    pytest_args = list()
    pytest_plugins = list()
    run_scripts = sys.argv[0]
    if project_path is None:
        test_path = run_scripts
        project_path = os.path.dirname(os.path.abspath(run_scripts))
    else:
        test_path = project_path
    init_dir(project_path=project_path)
    config = ProjectConfig(project_home=project_path).get_object()
    logging_plus = getattr(config, "logging")
    logging.config.dictConfig(logging_plus)
    if (report_type == ALLURE_DESCRIPTION_MARK and pytest_cov.__version__ >= '5.0.0' and
            html_version >= '4.1.1' and metadata_version >= '3.1.1'):
        allure_dir = join_path([project_path, "allure-results"])
        pytest_plugins.extend(['allure_pytest', 'pytest_cov', 'pytest_html', 'pytest_metadata'])
        pytest_args.extend(
            ['--alluredir={}'.format(allure_dir), '--cov', '--cov-report=html', '--cov-config=.coveragerc']
        )
    pytest_args.append(test_path)
    pytest.main(args=pytest_args, plugins=pytest_plugins)
