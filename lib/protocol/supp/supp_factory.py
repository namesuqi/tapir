# coding=utf-8
import binascii
import hashlib
from lib.protocol.udp_tools import get_container_list
from lib.protocol.supp.supp_data import *


# supp 各信令的结构
class SUPPStartChannelStruct(object):

    def __init__(self):
        self.protocol = None
        self.suppType = None
        self.channelId = None
        self.sequence = None
        self.urlMd5 = None
        self.fileUrl = None
        self.sdkVersion = None

    def get_data(self):
        data = self.protocol + self.suppType + self.channelId + self.sequence + self.urlMd5 + self.fileUrl \
               + self.sdkVersion
        return data


class SUPPStartRspStruct(object):

    def __init__(self, data):
        self.data = data
        self.protocol = None
        self.suppType = None
        self.channelId = None
        self.sequence = None
        self.code = None
        self.reserved = None
        self.pieceSize = None
        self.ppc = None
        self.birate = None
        self.iframeOffset = None
        self.iframeElepsed = None
        self.userLen = None
        self.userData = None
        self.field_list = [('protocol', 1),
                           ('suppType', 1),
                           ('channelId', 2),
                           ('sequence', 2),
                           ('code', 1),
                           ('reserved', 1),
                           ('pieceSize', 2),
                           ('ppc', 2),
                           ('birate', 4),
                           ('iframeOffset', 8),
                           ('iframeElepsed', 8),
                           ('userLen', 2),
                           ]
        user_len = get_container_list(self.data, self.field_list, 11)
        self.field_list.append(("userData", user_len))

        self.length = 2  # checksum为两个字节，因此初始长度设定为2
        for field in self.field_list:
            self.length += field[1]

    def get_data(self):
        return self.protocol + self.suppType + self.channelId + self.sequence + self.code + self.reserved \
               + self.pieceSize + self.ppc + self.birate + self.iframeOffset + self.iframeElepsed + self.userLen \
               + self.userData


class SUPPChaseReqStruct:

    def __init__(self):
        self.protocol = None
        self.suppType = None
        self.channelId = None
        self.sequence = None
        self.offSet = None
        self.urlMd5 = None
        self.fileUrl = None
        self.sdkVersion = None

    def get_data(self):
        data = self.protocol + self.suppType + self.channelId + self.sequence + self.offSet + self.urlMd5 \
               + self.fileUrl + self.sdkVersion
        return data


class SUPPChaseRspStruct(object):

    def __init__(self, data):
        self.protocol = None
        self.suppType = None
        self.channelId = None
        self.sequence = None
        self.code = None
        self.reserved = None
        self.iframeOffset = None
        self.iframeElepsed = None
        self.userLen = None
        self.container = None
        self.data = data
        self.field_list = [('protocol', 1),
                           ('suppType', 1),
                           ('channelId', 2),
                           ('sequence', 2),
                           ('code', 1),
                           ('reserved', 1),
                           ('iframeOffset', 8),
                           ('iframeElepsed', 8),
                           ('userLen', 2)
                           ]
        user_len = get_container_list(self.data, self.field_list, 8)
        self.field_list.append(("container", user_len))

        self.length = 2  # checksum为两个字节，因此初始长度设定为2
        for field in self.field_list:
            self.length += field[1]


class SUPPChunkReqStruct:

    def __init__(self):
        self.protocol = None
        self.suppType = None
        self.channelId = None
        self.chunkId = None
        self.urlMd5 = None
        self.sdkVersion = None
        self.bitmapLen = '0000'  # 固定字段
        self.bitmap = ''

    def get_data(self):
        data = self.protocol + self.suppType + self.channelId + self.chunkId + self.urlMd5 + self.sdkVersion + \
               self.bitmapLen + self.bitmap
        return data


class SUPPChunkRspStruct(object):

    def __init__(self, data):
        self.protocol = None
        self.suppType = None
        self.channelId = None
        self.chunkId = None
        self.code = None
        self.iframeOffset = None
        self.iframeElepsed = None
        self.userLen = None
        self.container = None
        self.data = data
        self.field_list = [('protocol', 1),
                           ('suppType', 1),
                           ('channelId', 2),
                           ('chunkId', 4),
                           ('code', 1),
                           ('reserved', 1),
                           ('iframeOffset', 8),
                           ('iframeElepsed', 8),
                           ('userLen', 2)
                           ]
        user_len = get_container_list(self.data, self.field_list, 8)
        self.field_list.append(("container", user_len))

        self.length = 2  # checksum为两个字节，因此初始长度设定为2
        for field in self.field_list:
            self.length += field[1]

    def get_data(self):
        self.data = self.protocol + self.suppType + self.channelId + self. chunkId + self.chunkId + self.code \
               + self.iframeOffset + self.iframeElepsed + self.userLen + self.container
        return self.data

        # self.fields = [('protocol', 1),
        #                   ('suppType', 1),
        #                   ('channelId', 2),
        #                   ('chunkId', 4),
        #                   ('code', 1),
        #                   ('iframeOffset', 8),
        #                   ('iframeElepsed', 8),
        #                   ('userLen', 2),
        #                   ('container', int(self.data[50:54], 16))
        #                   ]
        # last_element_length = self.fieldlist[-1][1]


class SUPPPieceDataStruct(object):

    def __init__(self):
        self.protocol = None
        self.suppType = None
        self.channelId = None
        self.seqNo = None
        self.chunkId = None
        self.piece = None
        self.field_list = [('protocol', 1),
                           ('suppType', 1),
                           ('channelId', 2),
                           ('seqNo', 2),
                           ('chunkId', 4),
                           ('piece', 868)
                           ]

        self.length = 2  # checksum为两个字节，因此初始长度设定为2
        for field in self.field_list:
            self.length += field[1]


class SUPPAckStruct:

    def __init__(self):
        self.protocol = None
        self.suppType = None
        self.channelId = None
        self.rppc = '0012'
        self.urlMd5 = None
        self.maxReceivedSeqno = None
        self.accumulatedLost = '00000000'
        self.elepsed = '0000'
        self.ackOpt = '02'
        self.reserved = '00000000000000'
        self.cmap = '00'
        self.ackLen = '04'
        self.minChunkId = '00000000'  # 固定且暂时不知道规律的值

    def get_data(self):
        data = self.protocol + self.suppType + self.channelId + self.rppc + self.urlMd5 + self.maxReceivedSeqno \
               + self.accumulatedLost + self.elepsed + self.ackOpt + self.reserved + self.cmap + self.ackLen \
               + self.minChunkId
        return data


class SUPPFinReqStruct:

    def __init__(self):
        self.protocol = None
        self.suppType = '09'
        self.channelId = None
        self.urlMd5 = None

    def get_data(self):
        data = self.protocol + self.suppType + self.channelId + self.urlMd5
        return data


'''
    生成协议数据
'''


def build_start_channel_data(channel_id, sequence, file_url, sdk_version):
    """
    构建start channel信令
    :param channel_id:
    :param sequence:
    :param file_url:
    :param sdk_version:
    :return:
    """
    structure = SUPPStartChannelStruct()
    structure.protocol = SUPP_PROTOCOL
    structure.suppType = START_CHANNEL_REQ_TYPE
    structure.channelId = str(hex(int(channel_id)))[2:].rjust(4, '0')
    structure.sequence = str(hex(int(sequence)))[2:].rjust(4, '0')
    structure.urlMd5 = hashlib.md5(str(file_url)).hexdigest().rjust(32, '0')
    structure.fileUrl = binascii.b2a_hex(file_url).ljust(512, "0")
    structure.sdkVersion = sdk_version_to_hex_string(sdk_version)
    return structure.get_data()


def build_chase_req_data(channel_id, sequence, offset, file_url, sdk_version):
    """
    构建chase req信令
    :param channel_id:
    :param sequence:
    :param offset:
    :param file_url:
    :param sdk_version:
    :return:
    """
    structure = SUPPChaseReqStruct()
    structure.protocol = SUPP_PROTOCOL
    structure.suppType = CHASE_REQ_TYPE
    structure.channelId = str(hex(int(channel_id)))[2:].rjust(4, '0')
    structure.sequence = str(hex(int(sequence)))[2:].rjust(4, '0')
    structure.offSet = str(hex(int(offset)))[2:].rjust(16, '0')
    structure.urlMd5 = hashlib.md5(str(file_url)).hexdigest().rjust(32, '0')
    structure.fileUrl = binascii.b2a_hex(file_url).ljust(512, "0")
    structure.sdkVersion = sdk_version_to_hex_string(sdk_version)

    return structure.get_data()


def build_chunk_req_data(channel_id, chunk_id, file_url, sdk_version):
    """
    构建chunk req信令
    :param channel_id:
    :param chunk_id:
    :param file_url:
    :param sdk_version:
    :return:
    """
    structure = SUPPChunkReqStruct()
    structure.protocol = SUPP_PROTOCOL
    structure.suppType = CHUNK_REQ_TYPE
    structure.channelId = str(hex(int(channel_id)))[2:].rjust(4, '0')
    structure.chunkId = str(hex(int(chunk_id)))[2:].rjust(8, '0')
    structure.urlMd5 = hashlib.md5(str(file_url)).hexdigest().rjust(32, '0')
    structure.sdkVersion = sdk_version_to_hex_string(sdk_version)
    structure.bitmapLen = ''.rjust(4, '0')

    return structure.get_data()


def build_ack_data(channel_id, file_url, max_received_seqno):
    """
    构建ack信令
    :param channel_id:
    :param file_url:
    :param max_received_seqno:
    :return:
    """
    structure = SUPPAckStruct()
    structure.protocol = SUPP_PROTOCOL
    structure.suppType = ACK_TYPE
    structure.channelId = str(hex(int(channel_id)))[2:].rjust(4, '0')
    structure.urlMd5 = hashlib.md5(str(file_url)).hexdigest().rjust(32, '0')
    structure.maxReceivedSeqno = str(hex(int(max_received_seqno)))[2:].rjust(4, '0')

    return structure.get_data()


def build_fin_req_data(channel_id, file_url):
    """
    构建fin信令
    :param channel_id:
    :param file_url:
    :return:
    """
    structure = SUPPFinReqStruct()
    structure.protocol = SUPP_PROTOCOL
    structure.suppType = FIN_TYPE
    structure.channelId = str(hex(int(channel_id)))[2:].rjust(4, '0')
    structure.urlMd5 = hashlib.md5(str(file_url)).hexdigest().rjust(32, '0')

    return structure.get_data()


'''
    处理特殊参数
'''


def sdk_version_to_hex_string(sdk_version):
    string = ''
    for i, version in enumerate(sdk_version.split('.')):
        if i == 2:
            string += str(hex(int(version)))[2:].rjust(4, '0')
        else:
            string += str(hex(int(version)))[2:].rjust(2, '0')
    return string


def verify_have_supp_data(response_list):
    """
    校验回复列表中存在数据信令
    :param response_list:
    :return:
    """
    flag = False
    for response in response_list:
        if response[0:4] == 'b107':  # 第1和第二个字节为b107是supp数据信令的特征
            flag = True
            break
    return flag


# def get_code_of_start_req(response_list):
#     """
#     获取start response的code参数
#     :param response_list:
#     :return:
#     """
#     code = 'not found'
#     for response in response_list:
#         if response[0:4] == 'b102':
#             code = response[12:14]
#             break
#     return code


def filter_response_list(response_list, target_type):
    """
    从一串回复中找到指定类型的回复
    :param response_list:
    :param target_type:
    :return:
    """
    if target_type == "startRsp":
        target_type = START_CHANNEL_RSP_TYPE
    elif target_type == "data":
        target_type = CHUNK_DATA_TYPE
    elif target_type == "chaseRsp":
        target_type = CHASE_RSP_TYPE
    elif target_type == "chunkRsp":
        target_type == CHUNK_RSP_TYPE
    for index, response in enumerate(response_list):
        if response[2:4] == target_type:
            return response
