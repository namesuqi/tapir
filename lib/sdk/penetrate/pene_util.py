# coding=utf-8
# author: Pan Pan

import time
import json
import re
from lib.common.remoter import remote_execute_result
from lib.sdk.penetrate.pene_constant import ADMIN_USERNAME, ADMIN_PWD, MOCK_TS_IP, GET_SEED_RSP_FORMAT, MOCK_TS_FILE, \
    REMOTE_PENETRATE_LOG_PATH, ROOT_USERNAME, ROOT_PWD, IN_NO_REVERSING, IN_REVERSING, OUT_NO_REVERSING, OUT_REVERSING, \
    DCCP_DISTINGUISH
from lib.sdk.sdk_constant import LOGIN_DASHBOARD_URL, CONF_DASHBOARD_URL, VERSION_DASHBOARD_URL


def check_peer_login(retry_times, ip):
    """
    检查SDK是否已经登录
    :param retry_times:
    :param ip:
    :return:
    """
    login_val = False
    count = 0
    while count < retry_times and not login_val:
        check_dict = get_peer_login_info(ip)
        if check_dict.find('"status": "E_OK"') > -1:
            login_val = True
        else:
            login_val = False
        time.sleep(4)
        count += 1
    return login_val


def get_peer_login_info(ip):
    """
    获得ajax/login页的数据
    :param ip:
    :return:
    """
    check_cmd = 'curl http://127.0.0.1:32717%s' % LOGIN_DASHBOARD_URL
    value = remote_execute_result(ip, ADMIN_USERNAME, ADMIN_PWD, check_cmd)
    return value


def get_peer_id_info(ip):
    """
    获得Peer节点的PeerID
    :param ip:
    :return:
    """
    get_peer_id_cmd = "curl http://127.0.0.1:32717%s" % CONF_DASHBOARD_URL
    ret_values = remote_execute_result(ip, ADMIN_USERNAME, ADMIN_PWD, get_peer_id_cmd)
    tmp_obj = json.loads(ret_values)
    return tmp_obj["peer_id"]


def get_peer_version_info(ip):
    """
    获得SDK版本信息
    :param ip:
    :return:
    """
    get_peer_version_cmd = "curl http://127.0.0.1:32717%s" % VERSION_DASHBOARD_URL
    ret_values = remote_execute_result(ip, ADMIN_USERNAME, ADMIN_PWD, get_peer_version_cmd)
    tmp_obj = json.loads(ret_values)
    return tmp_obj["core"]


def mock_get_seeds_response(sdk_version, peer_id, pinf_obj):
    """
    将期望的ts响应写入jsontext.text
    :param sdk_version:
    :param peer_id:
    :param pinf_obj:
    :return:
    """
    ret_str = GET_SEED_RSP_FORMAT % (
        pinf_obj["stunIP"], sdk_version, pinf_obj["natType"], pinf_obj["publicIP"], pinf_obj["publicPort"],
        pinf_obj["privateIP"], pinf_obj["privatePort"], peer_id)
    mock_cmd = "> %s; echo '%s' > %s" % (MOCK_TS_FILE, ret_str, MOCK_TS_FILE)
    value = remote_execute_result(MOCK_TS_IP, ADMIN_USERNAME, ADMIN_PWD, mock_cmd)
    if len(value) > 0:
        return False
    else:
        return True


def check_log(ip, is_out_forward, reversing=False):
    """
    检查penetrate.log
    :param ip:
    :param is_out_forward:
    :param reversing:
    :return:
    """
    ret_values = remote_execute_result(ip, ROOT_USERNAME, ROOT_PWD, "cat %s" % REMOTE_PENETRATE_LOG_PATH)
    lines = ret_values.split("\n")
    if check_log_pene(lines, is_out_forward, reversing):
        if check_log_dccp(lines):
            return True
        else:
            return False
    else:
        return False


def check_log_pene(lines, is_out_forward, reversing=False):
    """
    检查penetrate.log中pene协议的部分
    :param lines:
    :param is_out_forward:
    :param reversing:
    :return:
    """
    # 初始化期望的日志内容
    if is_out_forward:
        if reversing:
            log_pattern = OUT_REVERSING
        else:
            log_pattern = OUT_NO_REVERSING
    else:
        if reversing:
            log_pattern = IN_REVERSING
        else:
            log_pattern = IN_NO_REVERSING

    # 起初，所有的item[1]都是False,也就是尚未检查成功的
    # 每次找到一个期望的项目，就将item[1]置为True
    # 最后，如果里面还有item[1]为False,就表示该item[0]没有找到，验证不通过
    for line in lines:
        for index, item in enumerate(log_pattern):
            if not item[1]:
                if re.match(item[0], line):
                    log_pattern[index][1] = True
                break
    for temp_item in log_pattern:
        if not temp_item[1]:
            return False
    return True


def check_log_dccp(lines):
    """
    检查penetrate.log中dccp协议的部分, DCCP distinguish = d1
    :param lines:
    :return:
    """
    for line in lines:
        if line.find("packet: {0}".format(DCCP_DISTINGUISH)) > -1:
            return True

