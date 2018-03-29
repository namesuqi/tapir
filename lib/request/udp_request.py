# coding=utf-8
# __author__ = 'Guzehao'
"""
udp收发包
"""

import binascii
import struct
import socket
import time
from lib.protocol.puff.puff_data import *


def udp_checksum(udp_data):
    """
    根据udp数据生成checksum
    :param udp_data: "810101"
    :return:
    """
    data_binascii = binascii.a2b_hex(udp_data)
    data = bytearray(data_binascii)
    length = len(data)

    t = length >> 3
    rest = length & 7
    # print t, rest
    sum = socket.htons(0x7973)
    for i in range(0, t):
        p = struct.unpack_from("Q", data, i * 8)[0]
        sum = sum ^ p

    if rest:
        temp = bytearray(8)
        for i in range(0, rest):
            temp[i] = data[t * 8 + i]
        last = struct.unpack_from("Q", temp, 0)[0]
        sum = sum ^ last

    sum = ((sum >> 32) ^ sum) & 0xffffffff
    cs = (((sum >> 16) ^ sum) & 0xffff)
    checksum = socket.ntohs(cs)
    checksum_hex = str(hex(checksum)).replace("0x", "")
    return checksum_hex


def verify_push_data(listening_port=60680, socket_timeout=5):
    """
    校验指定端口在timeout内是否收到数据
    :param listening_port:
    :param socket_timeout:
    :return:
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind(("", listening_port))
        s.settimeout(socket_timeout)
        response_list = list()
        data, addr = s.recvfrom(1024)
        response_list.append(binascii.b2a_hex(data))
        s.close()
        for index, response in enumerate(response_list):
            if response[0:4] == PUFF_PROTOCOL + PUFF_SESSION_DAT:
                return True
            else:
                return False
    except Exception, e:
        print "Exception:", e
        if isinstance(e, socket.timeout):
            return False
        else:
            return False


def send_udp_request_keep_listening(req_from, api_host, api_port, req_data, listening_port, socket_timeout=5):
    """
    发送req后接受其后收到的二十个包并返回list
    :param req_from:
    :param api_host:
    :param api_port:
    :param req_data:
    :param listening_port:
    :param socket_timeout:
    :return:
    """
    try:
        print "-------------------------%sRequest-----------------------------" % req_from
        print "listening port: " + str(listening_port)
        print "sent data: " + str(req_data)
        print "------------------------------------------------------------------------"
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind(("", int(listening_port)))
        s.settimeout(socket_timeout)
        s.sendto(binascii.a2b_hex(req_data), (api_host, int(api_port)))
        response_list = list()
        for i in range(20):
            data, addr = s.recvfrom(1024)
            response_list.append(binascii.b2a_hex(data))
            print "+++++++++++++++++++++++++++%sResponse++++++++++++++++++++++++++" % req_from
            print "response list "+str(i+1)+' : ' + response_list[i]
            print "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
        # print binascii.b2a_hex(data)
        s.close()
        return response_list

    except Exception, e:
        print "Exception:", e
        if isinstance(e, socket.timeout):
            return response_list
        else:
            return False


def send_udp_request_special(req_from, api_host, api_port, req_data, listening_port, socket_timeout=5):
    """
    特殊的发包方法，用于快速发包，并方便存入列表
    :param req_from:
    :param api_host:
    :param api_port:
    :param req_data:
    :param listening_port:
    :param socket_timeout:
    :return:
    """
    try:
        print "-------------------------%sRequest-----------------------------" % req_from
        print "listening port: " + str(listening_port)
        print "sent data: " + str(req_data)
        print "------------------------------------------------------------------------"
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind(("", listening_port))
        s.settimeout(socket_timeout)
        s.sendto(binascii.a2b_hex(req_data), (api_host, int(api_port)))
        data, addr = s.recvfrom(1024)
        # print binascii.b2a_hex(data)
        s.close()
        print "+++++++++++++++++++++++++++%sResponse++++++++++++++++++++++++++" % req_from
        print "received data: " + str(binascii.b2a_hex(data))
        print "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
        return binascii.b2a_hex(data)

    except Exception, e:
        print "Exception:", e
        if isinstance(e, socket.timeout):
            return ''
        else:
            return False


def send_udp_request(req_from, api_host, api_port, req_data, listening_port, socket_timeout=5):
    try:
        print "-------------------------%sRequest-----------------------------" % req_from
        print "listening port: " + str(listening_port)
        print "sent data: " + str(req_data)
        print "------------------------------------------------------------------------"
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind(("", listening_port))
        s.settimeout(socket_timeout)
        s.sendto(binascii.a2b_hex(req_data), (api_host, int(api_port)))
        data, addr = s.recvfrom(1024)
        # print binascii.b2a_hex(data)
        s.close()
        print "+++++++++++++++++++++++++++%sResponse++++++++++++++++++++++++++" % req_from
        print "received data: " + str(binascii.b2a_hex(data))
        print "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
        return binascii.b2a_hex(data)

    except Exception, e:
        print "error:", e
        if isinstance(e, socket.timeout):
            return None
        else:
            return False
