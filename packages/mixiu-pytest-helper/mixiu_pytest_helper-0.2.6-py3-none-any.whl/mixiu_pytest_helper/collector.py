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
from mixiu_pytest_helper.dir import delete_file


def collect_marks(collect_dir: str):
    collect_marks_file = 'collect_marks.json'
    # 使用 subprocess 运行 pytest
    result = subprocess.run(
        ['pytest', '--disable-warnings', '--collect-only', '--json-report',
         '--json-report-file={}'.format(collect_marks_file),
         collect_dir],
        capture_output=True,
        text=True
    )

    # 检查 pytest 是否成功执行
    if result.returncode != 0:
        print("pytest 执行失败:")
        print(result.stderr)
        return

    # 解析 pytest 输出的 JSON 报告
    with open(collect_marks_file, 'r') as f:
        report = json.load(f)

    delete_file(file_path=collect_marks_file)

    # 提取标记信息
    marks = {}
    for item in report['tests']:
        marks[item['nodeid']] = item.get('markers', [])

    # 打印标记信息
    for nodeid, marker_list in marks.items():
        print(f"{nodeid}: {marker_list}")
