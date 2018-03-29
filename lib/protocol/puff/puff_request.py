# coding=utf-8
# __author__ = 'Guzehao'
"""
通过udp_request将准备好的Puff data发出
并返回收到的包，通过puff factory进行分割校验
17-3-27
"""
from puff_factory import *
from puff_data import *
from lib.request.udp_request import *


def send_puff_request(session_id=SESSION_ID_DEFAULT, peer_id=PEER_ID_DEFAULT, file_url=FILE_URL_DEFAULT,
                      cppc=CPPC_DEFAULT, priority=PRIORITY_DEFAULT, listening_port=LISTENING_PORT_DEFAULT):
    """
    发送puff请求信令
    :param session_id:
    :param peer_id:
    :param file_url:
    :param cppc:
    :param priority:
    :param listening_port:
    :return:
    """
    request_data = build_request_data(session_id, peer_id, file_url, cppc, priority)
    send_data = request_data + udp_checksum(request_data).rjust(4, '0')
    response_list = send_udp_request_keep_listening("puff_request", LIVE_PUSH_HOST, LIVE_PUSH_PUFF_PORT,
                                                    send_data, listening_port)
    return response_list


def send_puff_request_row(session_id=SESSION_ID_DEFAULT, peer_id=PEER_ID_DEFAULT, file_url=FILE_URL_DEFAULT,
                          cppc=CPPC_DEFAULT, priority=PRIORITY_DEFAULT, listening_port=LISTENING_PORT_DEFAULT):
    """
    快速发送一串puff请求信令
    :param session_id:
    :param peer_id:
    :param file_url:
    :param cppc:
    :param priority:
    :param listening_port:
    :return:
    """
    response_list = list()
    request_data = build_request_data(session_id, peer_id, file_url, cppc, priority)
    send_data = request_data+udp_checksum(request_data).rjust(4, '0')
    for i in range(5):
        response = send_udp_request_special("puff_request", LIVE_PUSH_HOST, LIVE_PUSH_PUFF_PORT, send_data,
                                            listening_port, 2)
        time.sleep(2)
        if response:
            response_list.append(response)
    return response_list


def send_puff_hib(session_id=SESSION_ID_DEFAULT, peer_id=PEER_ID_DEFAULT, file_url=FILE_URL_DEFAULT,
                  listening_port=LISTENING_PORT_DEFAULT):
    """
    发送puff心跳信令
    :param session_id:
    :param peer_id:
    :param file_url:
    :param listening_port:
    :return:
    """
    request_data = build_hib_data(session_id, peer_id, file_url)
    send_data = request_data + udp_checksum(request_data).rjust(4, '0')
    response_list = send_udp_request_keep_listening("puff_hib", LIVE_PUSH_HOST, LIVE_PUSH_PUFF_PORT,
                                                    send_data, listening_port)
    return response_list


def send_puff_fin(reason=REASON_DEFAULT, session_id=SESSION_ID_DEFAULT, peer_id=PEER_ID_DEFAULT,
                  file_url=FILE_URL_DEFAULT, listening_port=LISTENING_PORT_DEFAULT):
    """
    发送puff结束信令
    :param session_id:
    :param peer_id:
    :param file_url:
    :param reason:
    :param listening_port:
    :return:
    """
    request_data = build_fin_data(session_id, peer_id, file_url, reason)
    send_data = request_data + udp_checksum(request_data).rjust(4, '0')
    response_list = send_udp_request_keep_listening("puff_fin", LIVE_PUSH_HOST, LIVE_PUSH_PUFF_PORT,
                                                    send_data, listening_port)
    return response_list


# 以下为发送异常情况的包
def send_rsp2srv():
    """
    发送回复信令
    :return:
    """
    request_data = ABNORMAL_DATA_1
    response = send_udp_request("puff_abnormal", LIVE_PUSH_HOST, LIVE_PUSH_PUFF_PORT, request_data,
                                LISTENING_PORT_DEFAULT)
    return response


def send_data2srv():
    """
    发送数据信令
    :return:
    """
    request_data = ABNORMAL_DATA_2
    response = send_udp_request("robot_puff_abnormal", LIVE_PUSH_HOST, LIVE_PUSH_PUFF_PORT, request_data,
                                LISTENING_PORT_DEFAULT)
    return response


def send_tail_long_data():
    """
    发送尾部过长的信令
    :return:
    """
    request_data = LONG_DATA_TAIL
    response = send_udp_request("robot_puff_abnormal", LIVE_PUSH_HOST, LIVE_PUSH_PUFF_PORT, request_data,
                                LISTENING_PORT_DEFAULT)
    return response


def send_head_long_data():
    """
    发送头部过长的信令
    :return:
    """
    request_data = LONG_DATA_HEAD
    response = send_udp_request("robot_puff_abnormal", LIVE_PUSH_HOST, LIVE_PUSH_PUFF_PORT, request_data,
                                LISTENING_PORT_DEFAULT)
    return response


def send_tail_short_data():
    """
    发送尾部过短的信令
    :return:
    """
    request_data = SHORT_DATA_TAIL
    response = send_udp_request("robot_puff_abnormal", LIVE_PUSH_HOST, LIVE_PUSH_PUFF_PORT, request_data,
                                LISTENING_PORT_DEFAULT)
    return response


def send_head_short_data():
    """
    发送头部过短的信令
    :return:
    """
    request_data = SHORT_DATA_HEAD
    response = send_udp_request("robot_puff_abnormal", LIVE_PUSH_HOST, LIVE_PUSH_PUFF_PORT, request_data,
                                LISTENING_PORT_DEFAULT)
    return response
