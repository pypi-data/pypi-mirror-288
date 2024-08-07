# coding=utf-8
# @FileName  :csv_tools_test.py
# @Time      :2024/8/6 17:45
from jeyoTools.csv_tool import write_to_csv

data = [{"name": "xiao"}]

write_to_csv("test.csv", data)
