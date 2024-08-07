# coding=utf-8
# @FileName  :csv_tool.py
# @Time      :2024/8/6 16:56
import csv
import datetime
import os


def write_to_csv(filename, data, module="w", write_flag_first=True):
    current_time = datetime.datetime.now()
    filename = f"{filename}_{current_time.strftime('%Y-%m-%d_%H%M%S')}.csv"
    # write_flag_first 第一次写入标识
    fieldnames = []
    for k, v in data[0].items():
        fieldnames.append(k)
    file_size = 0
    if os.path.exists(filename):
        file_size = os.path.getsize(filename)
    # 打开文件并创建csv.writer对象
    with open(filename, module, newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if write_flag_first and file_size == 0:
            writer.writeheader()
        # 写入数据
        for row in data:
            writer.writerow(row)