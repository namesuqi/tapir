# coding=utf-8
"""
发送supp信令
"""
import threading
import time
from lib.protocol.supp.supp_factory import *
from lib.protocol.supp.supp_data import *
from lib.request.udp_request import *


def supp_start_req(channel_id, sequence, file_url, sdk_version=SDK_VERSION_DEFAULT, check_sum=True,
                   listening_port=LISTESNING_PORT_DEFAULT):
    """
    将构建好的起播请求发出
    :param channel_id:
    :param sequence:
    :param file_url:
    :param sdk_version:
    :param check_sum:
    :param listening_port:
    :return:
    """
    data = build_start_channel_data(channel_id, sequence, file_url, sdk_version)
    if check_sum is True:
        check_sum_data = udp_checksum(data).rjust(4, '0')
    else:
        check_sum_data = check_sum

    data = data + check_sum_data

    response_list = send_udp_request_keep_listening(
        '[SuppStartReq]',
        LIVE_PUSH_HOST,
        LIVE_PUSH_SUPP_PORT,
        data,
        listening_port,
        SOCKET_TIME_OUT
    )
    return response_list


def supp_chase_req(channel_id, sequence, offset, file_url, sdk_version=SDK_VERSION_DEFAULT, check_sum=True,
                   listening_port=LISTESNING_PORT_DEFAULT):
    """
    将构造好的chase请求发出
    :param channel_id:
    :param sequence:
    :param offset:
    :param file_url:
    :param sdk_version:
    :param check_sum:
    :param listening_port:
    :return:
    """
    data = build_chase_req_data(channel_id, sequence, offset, file_url, sdk_version)
    if check_sum is True:
        check_sum_data = udp_checksum(data).rjust(4, '0')
    else:
        check_sum_data = check_sum

    data = data + check_sum_data

    response_list = send_udp_request_keep_listening(
        '[SuppChaseReq]',
        LIVE_PUSH_HOST,
        LIVE_PUSH_SUPP_PORT,
        data,
        listening_port,
        SOCKET_TIME_OUT
    )
    return response_list


def supp_chunk_req(channel_id, chunk_id, file_url, sdk_version=SDK_VERSION_DEFAULT, check_sum=True,
                   listening_port=LISTESNING_PORT_DEFAULT):
    """
    将构造好的chunk请求发出
    :param channel_id:
    :param chunk_id:
    :param file_url:
    :param sdk_version:
    :param check_sum:
    :param listening_port:
    :return:
    """
    data = build_chunk_req_data(channel_id, chunk_id, file_url, sdk_version)
    if check_sum is True:
        check_sum_data = udp_checksum(data).rjust(4, '0')
    else:
        check_sum_data = check_sum

    data = data + check_sum_data
    response = send_udp_request(
        '[SuppChunkReq]',
        LIVE_PUSH_HOST,
        LIVE_PUSH_SUPP_PORT,
        data,
        listening_port,
        SOCKET_TIME_OUT
    )
    return response


def supp_ack(channel_id, file_url, max_received_seqno, check_sum=True, listening_port=LISTESNING_PORT_DEFAULT):
    """
    将构造好的ack信令发出
    :param channel_id:
    :param file_url:
    :param max_received_seqno:
    :param check_sum:
    :param listening_port:
    :return:
    """
    data = build_ack_data(channel_id, file_url, max_received_seqno)
    if check_sum is True:
        check_sum_data = udp_checksum(data).rjust(4, '0')
    else:
        check_sum_data = check_sum

    data = data + check_sum_data
    response_list = send_udp_request_keep_listening(
        '[SuppAck]',
        LIVE_PUSH_HOST,
        LIVE_PUSH_SUPP_PORT,
        data,
        listening_port,
        SOCKET_TIME_OUT
    )
    return response_list


def supp_fin_req(channel_id, file_url, check_sum=True, listening_port=LISTESNING_PORT_DEFAULT):
    """
    将构造好的结束信令发出
    :param channel_id:
    :param file_url:
    :param check_sum:
    :param listening_port:
    :return:
    """
    data = build_fin_req_data(channel_id, file_url)
    if check_sum is True:
        check_sum_data = udp_checksum(data).rjust(4, '0')
    else:
        check_sum_data = check_sum

    data = data + check_sum_data
    response = send_udp_request(
        '[SuppFin]',
        LIVE_PUSH_HOST,
        LIVE_PUSH_SUPP_PORT,
        data,
        listening_port,
        0.1
    )
    return response


# def ack_loop():
#     """
#     循环发送ack，调试用
#     :return:
#     """
#     # time.sleep(1)
#     for i in range(20):
#         seqno = str(i*6)
#         supp_ack(CHANNEL_ID, FILE_URL, seqno)
#         time.sleep(1)


def supp_start_req_error(error_type, channel_id_initial, listening_port=LISTESNING_PORT_DEFAULT):
    """
    发一些奇奇怪怪的包
    :param error_type:
    :param channel_id_initial:
    :param listening_port:
    :return:
    """
    channel_id = str(hex(int(channel_id_initial)))[2:].rjust(4, '0')
    data = error_type % channel_id
    tail_data = udp_checksum(data).rjust(4, '0')
    data = data+tail_data
    response_list = send_udp_request_keep_listening(
        '[SuppChaseReqEro]',
        LIVE_PUSH_HOST,
        LIVE_PUSH_SUPP_PORT,
        data,
        listening_port,
        SOCKET_TIME_OUT
    )
    return response_list


def supp_start_req_ack(channel_id, req_sequence, req_file_url, ack_file_url, ack_checksum=True):
    """
    发送起播信令后连续发送ack信令，并返回发送最后一次ack所受到的response
    :param channel_id:
    :param req_sequence:
    :param req_file_url:
    :param ack_file_url:
    :param ack_checksum:
    :return:
    """
    supp_start_req(channel_id, req_sequence, req_file_url)
    for i in range(10):
        ack_max_received_seqno = str(i*15)
        supp_ack(channel_id, ack_file_url, ack_max_received_seqno, ack_checksum)
        time.sleep(0.5)
    time.sleep(1)
    response_list = supp_ack(channel_id, ack_file_url, '165', ack_checksum)
    return response_list


# def supp_other():
    # supp_start_req(CHANNEL_ID, SEQUENCE, FILE_URL, SDK_VERSION_DEFAULT)
    # supp_chunk_req(CHANNEL_ID, CHUNK_ID, FILE_URL)
    # supp_chase_req(CHANNEL_ID, '1234', '5432', FILE_URL, )
    # time.sleep(5)
    # supp_fin_req(CHANNEL_ID, FILE_URL)
#
# t1 = threading.Thread(target=ack_loop())
# t2 = threading.Thread(target=supp_other())
# # t1.setDaemon(True)
# # t2.setDaemon(True)
# t2.start()
# t1.start()
# from lib.protocol.udp_tools import split_udp_data
# if __name__ == '__main__':
#     response_list = supp_chunk_req('123', CHUNK_ID, FILE_URL_NOT_EXIST)
#     print response_list
