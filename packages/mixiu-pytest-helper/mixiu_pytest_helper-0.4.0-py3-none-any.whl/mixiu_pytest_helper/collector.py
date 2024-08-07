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
import json
import subprocess
from mixiu_pytest_helper.log import logger
from mixiu_pytest_helper.dir import get_project_path, delete_file, init_dir


def collect_marks(collect_dir: str) -> list:
    if collect_dir is None:
        collect_dir = get_project_path()
    init_dir(project_path=collect_dir)
    collect_marks = list()
    collect_marks_file = 'collect_marks.json'
    # 使用 subprocess 运行 pytest
    result = subprocess.run(
        ['pytest', '--disable-warnings', '--collect-only', '--verbose', '--json-report',
         '--json-report-file={}'.format(collect_marks_file),
         collect_dir],
        capture_output=True,
        text=True
    )

    # 检查 pytest 是否成功执行
    if result.returncode != 0:
        logger.error(result.stderr)
        return collect_marks

    # 解析 pytest 输出的 JSON 报告
    with open(collect_marks_file, 'r') as f:
        report = json.load(f)

    delete_file(file_path=collect_marks_file)

    for x in report.get("collectors"):
        print("x: {}".format(x))
        for y in x.get("result"):
            print("y: {}".format(y))
            if y.get("type") == "Function":
                print(y.get('nodeid'))
