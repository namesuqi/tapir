# coding=utf-8
# author: zengyuetian

from lib.android.adber import *


def logcat_clear(device):
    """
    clear logcat log
    :param device: android device
    :return: N.A.
    """
    cmd = "logcat -c"
    adb_shell(device, cmd)


def logcat_get(device):
    """
    get all logcat log
    :param device:
    :return: log content
    """
    cmd = "logcat -d"
    return adb_shell(device, cmd)


def logcat_filter(device, keyword):
    """
    get all logcat log
    :param device:
    :return: log content
    """
    cmd = "logcat -d -s {0}".format(keyword)
    return adb_shell(device, cmd)




