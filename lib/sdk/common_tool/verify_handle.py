# coding=utf-8
import json
import os
import re

from lib.sdk.common_tool.ssh_client import *
from lib.sdk.sdk_constant import *


def get_occupied_ports(remote_ip, username, password, process_keyword=None):
    ssh_client = SSHClient(remote_ip, username, password)
    if process_keyword is None:
        cmd = "netstat -anut "
    else:
        cmd = "netstat -anutp | grep tcp | grep {0}".format(process_keyword)
    stand_out, stand_err = ssh_client.execute_command(cmd)
    occupied_port_list = []
    for i, item in enumerate(stand_out.split('\n')):
        if i == 0 or i == 1:
            continue
        elif item == "":
            continue
        else:
            occupied_port_list.append(item.split(':')[1].split(' ')[0])
    occupied_port_list = set(occupied_port_list)
    return occupied_port_list


def verify_port_not_occupancy(remote_ip, username, password, *ports):

    """
        检查远端端口占用情况。未被占用返回True
    :param remote_ip:
    :param username:
    :param password:
    :param ports:
    :return:
    """
    occupied_ports = get_occupied_ports(remote_ip, username, password)
    flag = True
    for port in ports:
        if port in occupied_ports:
            print "pls check {0} port is occupied!".format(port)
            flag = False
    return flag

def verify_port_occupancy(remote_ip, username, password, *ports):

    """
        检查远端端口占用情况。全被占用返回True
    :param remote_ip:
    :param username:
    :param password:
    :param ports:
    :return:
    """
    occupied_ports = get_occupied_ports(remote_ip, username, password)
    flag = True
    for port in ports:
        if port not in occupied_ports:
            print "{0} port is not occupied.".format(port)
            flag = False
    return flag

def verify_process_port_occupancy(remote_ip, username, password, process_keyword):
    """
        验证某进程的tcp端口监听，监听存在返回 False,不存在返回 True
    :return:
    """
    occupied_ports = get_occupied_ports(remote_ip, username, password, process_keyword)
    return len(occupied_ports) == 0


def verify_progress_alive(remote_ip, username, password, progress_keyword):
    """
        进程若启动返回 False,未启动返回True
    :param remote_ip:
    :param username:
    :param password:
    :param progress_keyword:
    :return:
    """
    ssh_client = SSHClient(remote_ip, username, password)
    cmd = "ps aux | grep -v grep | grep {0}".format(progress_keyword)
    stand_out, stand_err = ssh_client.execute_command(cmd)
    return stand_out == ""


def get_network_monitor_log(protocol, behave):
    """
    获取并解析sdk执行机器上的网络包log文件
    """
    log_data = list()

    # if not os.path.exists(os.path.abspath(os.path.dirname(__file__)) + "/NetworkMonitor.log"):
    from lib.sdk.common_tool.sftp_client import SFTPClient
    sftp_client = SFTPClient(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD)
    local_path = os.path.abspath(os.path.dirname(__file__)) + "/NetworkMonitor.log"
    sftp_client.download(remote_path='/root/sdk_api/NetworkMonitor.log', local_path=local_path)
    time.sleep(15)

    with open(os.path.abspath(os.path.dirname(__file__)) + '/NetworkMonitor.log', 'r') as reader:
        origin_lines = reader.readlines()
    re_str = ".*{}\((.*)\)\n".format(behave.capitalize())
    if protocol.upper() == "HTTP":
        for line in origin_lines:
            if line.startswith(protocol.upper()):
                if line.find(behave.capitalize()) > 0:
                    data = re.compile(re_str).search(line).group(1).replace("\"", "'")
                    log_data_list = list()
                    re_list = re.split(",\s([^'&^0-9])", data)
                    for i, item in enumerate(re_list):
                        if i == 0:
                            log_data_list.append(item)
                        if i % 2 != 0:
                            log_data_list.append(re_list[i] + re_list[i + 1])
                    log_data_dict = dict()
                    for list_data in log_data_list:
                        list_data.split('=', 1)
                        if len(list_data.split('=', 1)) > 1:
                            list_res = list_data.split('=', 1)
                            log_data_dict[list_res[0]] = list_res[1]
                    log_data.append(log_data_dict)
            else:
                continue
    elif protocol.upper() == "UDP":
        for line in origin_lines:
            if line.startswith(protocol.upper()):
                pass
            else:
                continue
    else:
        raise Exception("protocol is not support!")

    return log_data


def verify_sdk_http_request(uri, method, *body_keys):
    """
    检查sdk发出去的http请求
    """
    temp_data = get_network_monitor_log("http", "request")
    for log in temp_data:
        if log['uri'][2:-1].startswith(uri):
            if log['method'][2:-1] == method:
                if len(body_keys) == 0:
                    return log
                else:
                    body_dict = eval(log['body'][1:-1])
                    if set(body_keys) == set(body_dict.keys()):
                        # return True
                        return body_dict
                    else:
                        print "uri", log['uri']
                        print "real", body_dict.keys()
                        print "except", body_keys
                        return False
            else:
                continue
    return False


def verify_server_http_response(uri, *body_keys):
    """
    检查server回复的http响应
    """
    temp_data = get_network_monitor_log("http", "response")
    for log in temp_data:
        if log['uri'][1:-1].startswith(uri):
            if len(body_keys) == 0:
                return True
            else:
                body_dict = eval(log['body'][1:-1])
                if set(body_keys) == set(body_dict.keys()):
                    return True
                else:
                    print "uri", log['uri']
                    print "real", body_dict.keys()
                    print "except", body_keys
                    return False
    return False

# def get_log(sdk_ip, username, password):
#     ssh_client = SSHClient(sdk_ip, username, password)
#     command = "cat /root/sdk_test/NetworkMonitor.log"
#     stand_out, stant_err = ssh_client.execute_command(command)
#     origin_lines = stand_out.split('\n')
#     print origin_lines


def verify_sdk_http_request_sublist_dict(uri, method, node_name, *body_keys):
    temp_data = get_network_monitor_log("http", "request")
    for log in temp_data:
        if log['uri'][1:-1].startswith(uri):
            if log['method'][1:-1] == method:
                body_dict = eval(log['body'][1:-1])
                for item in body_dict[node_name]:
                    if set(item.keys()) != set(body_keys):
                        return False
    return True


def get_sdk_http_request_sublist_dict_value(uri, method, node_name, key_name):
    # Should Contain
    value_list = []
    temp_data = get_network_monitor_log("http", "request")
    for log in temp_data:
        if log['uri'][1:-1].startswith(uri):
            if log['method'][1:-1] == method:
                body_dict = eval(log['body'][1:-1])
                for item in body_dict[node_name]:
                    value_list.append(item[key_name])
    return value_list


def verify_peer_id_legal(peer_id):
    flag = True
    if len(peer_id) != 32:
        flag = False
    if peer_id[:8] != '00000004':
        if peer_id[:8] != USER_PREFIX:
            flag = False
    return flag


if __name__ == '__main__':
    # print get_occupied_ports('10.6.3.28', 'root', 'Yunshang2014')
    # print verify_port_occupancy('10.6.3.28', 'root', 'Yunshang2014', '32717', '32718', '32719')
    # print verify_process_port_occupancy('10.6.3.28', 'root', 'Yunshang2014', 'ys_service')
    # print verify_progress_alive('10.6.3.28', 'root', 'Yunshang2014', 'ys_service')get_network_monitor_log
    # print get_network_monitor_log("http", "request")
    # print verify_sdk_http_request('/session/peers/', 'POST', 'publicIP', 'version', 'macs', 'stunIP', 'privatePort', 'deviceInfo', 'natType', 'publicPort', 'privateIP')
    # print verify_sdk_http_request('/sdk/opt_report/v1', 'POST', 'timestamp', 'peer_id', 'nat_type', 'duration', 'req_rtt', 'penetrate_stats')
    # get_log('10.6.3.28', 'root', 'Yunshang2014')
    # print verify_sdk_http_request_sublist_dict('/sdk/opt_report/v1', 'POST', 'req_rtt', 'domain', 'ip', 'rtt')
    # print get_sdk_http_request_sublist_dict_value('/sdk/opt_report/v1', 'POST', 'req_rtt', 'domain')
    # print verify_port_occupancy('192.168.2.44', 'root', 'root', '32717')
    pass
