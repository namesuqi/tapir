# coding=utf-8
# author: Pan Pan
import json

from lib.common.remoter import remote_execute, remote_execute_result
from lib.sdk.penetrate import pene_util
from lib.sdk.common_tool.sftp_client import SFTPClient
from lib.sdk.penetrate.pene_constant import *


def upload_nat_simulator(ip, remote_path):
    """
    上传nat_simulator
    :param ip:
    :param remote_path:
    :return:
    """
    mkdir_cmd = "mkdir -p {0}".format(remote_path)
    remote_execute(ip, ROOT_USERNAME, ROOT_PWD, mkdir_cmd)
    eg = SFTPClient(ip, ROOT_USERNAME, ROOT_PWD)
    eg.upload_dir(local_dir_path=LOCAL_SIMULATOR_PATH, remote_dir_path=remote_path)
    print "nat_simulator upload done"


def start_nat_simulator(ip, nat_type):
    """
    启动NAT模拟器
    :param ip: ip where start nat simulator
    :param nat_type:
    :return:
    """
    remote_execute(ip, ROOT_USERNAME, ROOT_PWD, START_SIMULATOR_CMD % nat_type)


def stop_nat_simulator(ip):
    """
    stop nat_simulator
    :param ip:
    :return:
    """
    remote_execute_result(ip, ROOT_USERNAME, ROOT_PWD, STOP_SIMULATOR_CMD)


def remove_sdk_yunshang(ip):
    """
    删除sdk的yunshang文件夹，使得再次启动sdk后peer_id发生改变，避免STUN缓存影响
    :param ip
    :return:
    """
    remove_cmd = "rm -rf {0}".format(REMOTE_SDK_DIR_PATH)
    remote_execute(ip, ADMIN_USERNAME, ADMIN_PWD, remove_cmd)


def check_sdk_login(ip):
    """
    验证SDK是否登录成功
    :param ip:
    :return:
    """
    try:
        return pene_util.check_peer_login(retry_times=3, ip=ip)
    except Exception, e:
        print e.message
        return False


def check_sdk_nat_type(ip, nat_type):
    """
    验证NAT类型
    :param ip:
    :param nat_type:
    :return:
    """
    if nat_type == "2":
        nat_type = "1"
    try:
        ret_values = pene_util.get_peer_login_info(ip)
        tmp_obj = json.loads(ret_values)
        if str(tmp_obj["natType"]) != nat_type:
            return False
        else:
            return True
    except Exception, e:
        print e.message
        return False


def mock_ts_info(seed_ip):
    """
    mock ts 的返回值
    :param seed_ip:
    :return:
    """
    try:
        peer_id = pene_util.get_peer_id_info(seed_ip)
        sdk_version = pene_util.get_peer_version_info(seed_ip)
        if peer_id and sdk_version:
            ret_value = pene_util.get_peer_login_info(seed_ip)
            tmp_obj = json.loads(ret_value)
            if pene_util.mock_get_seeds_response(sdk_version, peer_id, tmp_obj):
                return True
            else:
                return False
        else:
            return False
    except Exception, e:
        print e.message
        return False


def start_sdk_play(ip):
    """
    sdk 起播
    :param ip:
    :return:
    """
    try:
        remote_execute(ip, ADMIN_USERNAME, ADMIN_PWD, START_PLAY_CMD)
        return True
    except Exception, e:
        print e.message
        return False


def check_penetrate_log_steps(send_nat_ip, receive_nat_ip, send_nat_type):
    """
    验证log里面记录的穿透是否成功
    :param send_nat_ip:
    :param receive_nat_ip:
    :param send_nat_type:
    :return:
    """
    # Peer类型4的穿透，需要REVERSING_REQ的介入
    if send_nat_type == "4":
        is_reversing = True
    else:
        is_reversing = False

    send_result = pene_util.check_log(send_nat_ip, is_out_forward=True, reversing=is_reversing)
    if not send_result:
        print "check penetrate.log FAILED!ip: %s" % send_nat_ip

    receive_result = pene_util.check_log(receive_nat_ip, is_out_forward=False, reversing=is_reversing)
    if not receive_result:
        print "check penetrate.log FAILED!ip: %s" % receive_nat_ip

    return send_result and receive_result


if __name__ == '__main__':
    # upload_nat_simulator(SEND_NAT_IP, REMOTE_SIMULATOR_PATH)
    # start_nat_simulator(SEND_NAT_IP, 4)
    check_penetrate_log_steps(SEND_NAT_IP, RECEIVE_NAT_IP, send_nat_type='4')
