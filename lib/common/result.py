# coding=utf-8
# author: zengyuetian

from lib.common.path import *
from lib.common.times import *


def get_result_file():
    return RESULT_PATH + '/result.html'


def get_result_file_with_time():
    return RESULT_PATH + '/result_{0}.html'.format(get_date_time_sec_string())
