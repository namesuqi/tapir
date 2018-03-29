# coding=utf-8
"""
__author__ = 'zengyuetian'
时间相关函数
"""

import time


def get_date_time_sec_string():
    """
    获得当前时间戳字符串
    :return:字符串
    """
    current = time.localtime()
    time_str = time.strftime("%Y%m%d%H%M%S", current)
    return time_str


def get_time_sec_string():
    """
    获得当前时间戳字符串
    :return:字符串
    """
    current = time.localtime()
    time_str = time.strftime("%H%M%S", current)
    return time_str


def get_formated_time_sec_string():
    """
    获得当前时间戳字符串
    :return:字符串
    """
    current = time.localtime()
    time_str = time.strftime("%H:%M:%S", current)
    return time_str


###############################
# 调试用
###############################
if __name__ == "__main__":
    print get_date_time_sec_string()