# coding=utf-8
# __author__ = 'Guzehao'
"""
组装puff数据
分割puff数据
校验puff数据
"""

import binascii
import hashlib
from lib.protocol.puff.puff_data import *


# 定义协议结构
class PuffRequestStruct:
    def __init__(self):
        self.protocol = None
        self.puffType = None
        self.sessionId = None
        self.peerId = None
        self.urlmd5 = None
        self.fileUrl = None
        self.cppc = None
        self.priority = None

    def get_data(self):
        data = self.protocol + self.puffType + self.sessionId + \
               self.peerId + self.urlmd5 + self.fileUrl + self.cppc + self.priority

        return data


class PuffHibStruct:
    def __init__(self):
        self.protocol = None
        self.puffType = None
        self.sessionId = None
        self.peerId = None
        self.urlmd5 = None

    def get_data(self):
        data = self.protocol + self.puffType + self.sessionId + self.peerId + self.urlmd5

        return data


class PuffFinStruct:
    def __init__(self):
        self.protocol = None
        self.puffType = None
        self.sessionId = None
        self.peerId = None
        self.urlmd5 = None
        self.reason = None

    def get_data(self):
        data = self.protocol + self.puffType + self.sessionId + self.peerId + self.urlmd5 + self.reason

        return data


class PuffResponseStruct(object):
    def __init__(self, data):
        self.data = data
        self.protocol = None
        self.puffType = None
        self.sessionId = None
        self.result = None
        # 字段顺序与长度 单位：byte
        self.field_list = [('protocol', 1),
                           ('puffType', 1),
                           ('sessionId', 1),
                           ('result', 1)
                           ]
        self.length = 2  # checksum为两个字节，因此初始长度设定为2
        for field in self.field_list:
            self.length += field[1]


class PuffDataStruct(object):
    def __init__(self, data):
        self.data = data
        self.protocol = None
        self.puffType = None
        self.sessionId = None
        self.chunkId = None
        self.pieceCheck = None
        self.pieceIndex = None
        self.pieceData = None
        self.t0 = None
        # 字段顺序与长度 单位：byte
        self.field_list = [('protocol', 1),
                           ('puffType', 1),
                           ('sessionId', 1),
                           ('chunkId', 4),
                           ('pieceCheck', 1),
                           ('pieceIndex', 3),
                           ('pieceData', 864),
                           ('t0', 8)
                           ]
        self.length = 2  # checksum为两个字节，因此初始长度设定为2
        for field in self.field_list:
            self.length += field[1]


# 组装协议
def build_request_data(session_id, peer_id, file_url, cppc, priority):
    """
    :param session_id: int 0~255
    :param peer_id: string
    :param file_url: string
    :param cppc: string
    :param priority: string
    :return:
    """
    structure = PuffRequestStruct()
    structure.protocol = PUFF_PROTOCOL
    structure.puffType = PUFF_SESSION_REQ

    # 一共1个字节长度，服务器并不计，不是真正的session
    structure.sessionId = str(hex(session_id))[2:].rjust(2, '0')
    structure.peerId = peer_id.lower()
    structure.cppc = cppc.rjust(4, '0')
    structure.urlmd5 = hashlib.md5(str(file_url[7:])).hexdigest().rjust(32, '0')
    structure.fileUrl = binascii.b2a_hex(file_url).ljust(256 * 2, '0')
    structure.priority = priority.rjust(2, '0')

    return structure.get_data()


def build_hib_data(session_id, peer_id, file_url):
    """

    :param session_id:int 0~255
    :param peer_id:string
    :param file_url:string
    :return:
    """
    structure = PuffHibStruct()
    structure.protocol = 'c1'
    structure.puffType = '04'
    structure.sessionId = str(hex(session_id))[2:].rjust(2, '0')
    structure.peerId = peer_id.lower()
    structure.urlmd5 = hashlib.md5(str(file_url[7:])).hexdigest().rjust(32, '0')

    return structure.get_data()


def build_fin_data(session_id, peer_id, file_url, reason):
    """

    :param session_id:
    :param peer_id:
    :param file_url:
    :param reason:
    :return:
    """
    structure = PuffFinStruct()
    structure.protocol = 'c1'
    structure.puffType = '05'
    structure.sessionId = str(hex(session_id))[2:].rjust(2, '0')
    structure.peerId = peer_id.lower()
    structure.urlmd5 = hashlib.md5(str(file_url[7:])).hexdigest().rjust(32, '0')
    structure.reason = reason.rjust(2, '0')
    return structure.get_data()


def response_filter(response_list, target_type):
    if target_type == "rsp":
        target_type = PUFF_SESSION_RSP
    elif target_type == "data":
        target_type = PUFF_SESSION_DAT
    for index, response in enumerate(response_list):
        if response[2:4] == target_type:
            return response
