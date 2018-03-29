# coding=utf-8
import random
from lib.protocol.puff.puff_data import *


def split_udp_data(udp_data):
    """
    根据data的结构长度，组装出各个字段的值
    除了返回值以外（该返回值并没太大用处），最重要的是udp_data的属性发生了变化
    :param udp_data:
    :return:
    """
    edge = 0
    for i in udp_data.field_list:
        udp_data.__setattr__(i[0], udp_data.data[edge:edge + i[1] * 2])
        edge += i[1] * 2
    return edge


def get_field_edge(field_list, index):
    edge = 0
    for i, d in enumerate(field_list):
        edge += d[1] * 2
        if i == index:
            break
    return edge


def get_udp_check_sum(udp_data):
    """
    获取response中的checksum字段
    :param udp_data:
    :return:
    """
    return udp_data.data[-4:]


def get_container_list(udp_data, field_list, index):
    """

    :param udp_data:
    :param field_list:
    :param index:
    :return:
    """
    start = get_field_edge(field_list, index-1)
    end = get_field_edge(field_list, index)
    container_length = int(udp_data[start:end], 16)
    return container_length


def get_random_channel_id():
    """
    随机返回一个可用的channel id
    """
    channel_id = random.randint(1, 65535)
    return channel_id


def check_puff_protocol(response_list):
    flag = True
    for index, response in enumerate(response_list):
        if response[0:2] != PUFF_PROTOCOL:
            print "Error: not puff_protocol: '{0}{1}'".format(response[0], response[1])
            flag = False
    return flag


# def check_puff_signal(response_list, signal):
#     flag = False
#     if signal == 'req':
#         for index, response in enumerate(response_list):
#             if response[2:4] == PUFF_SESSION_REQ:
#                 flag = True
#     elif signal == 'resp':
#         for index, response in enumerate(response_list):
#             if response[2:4] == PUFF_SESSION_RSP:
#                 flag = True
#     elif signal == 'data':
#         for index, response in enumerate(response_list):
#             if response[2:4] == PUFF_SESSION_DAT:
#                 flag = True
#     elif signal == 'hib':
#         for index, response in enumerate(response_list):
#             if response[2:4] == PUFF_SESSION_HIB:
#                 flag = True
#     elif signal == 'fin':
#         for index, response in enumerate(response_list):
#             if response[2:4] == PUFF_SESSION_FIN:
#                 flag = True
#     return flag

def check_puff_signal(response_list):
    flag = True
    puff_signal_code = ['01', '02', '03', '04', '05']
    for index, response in enumerate(response_list):
        if response[2:4] not in puff_signal_code:
            flag = False
    return flag


# def get_length_of_struct(class_name):
#     obj = class_name('')
#     obj.field_list
