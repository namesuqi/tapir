# coding=utf-8
# __author__ = 'zengyuetian'

import inspect
import os
import sys


def get_root_path():
    """
    获得自动测试框架根目录
    :return:
    """
    file_path = os.path.abspath(inspect.getfile(sys.modules[__name__]))
    parent_path = os.path.dirname(file_path)
    lib_path = os.path.dirname(parent_path)
    root_path = os.path.dirname(lib_path)
    return root_path


def get_root_parent_path():
    """
    获得自动测试框架根目录的父目录
    :return:
    """
    root_parent_path = os.path.dirname(get_root_path())
    return root_parent_path


def get_root_dir_name():
    return os.path.basename(get_root_path())


RESULT_PATH = get_root_path() + "/result"
MISC_PATH = get_root_path() + "/misc"
UTILITY_PATH = get_root_path() + "/utility"


###############################
# 调试用
###############################
if __name__ == "__main__":
    print get_root_path()
    print get_root_dir_name()



