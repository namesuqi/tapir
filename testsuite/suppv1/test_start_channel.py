# coding=utf-8
import unittest
from lib.protocol.supp.supp_request import *
from lib.protocol.udp_tools import *
from lib.common.decorator import *


class TestStartChannel(unittest.TestCase):

    def tearDown(self):
        time.sleep(1)

    @func_doc
    def testCorrectReq(self):
        """
        正确的起播请求能收到各字段正确的起播回复
        """
        channel_id = get_random_channel_id()
        response_list = supp_start_req(channel_id, SEQUENCE, FILE_URL_DEFAULT)
        supp_fin_req(channel_id, FILE_URL_DEFAULT)
        response = SUPPStartRspStruct(filter_response_list(response_list, 'startRsp'))
        split_udp_data(response)
        flag = verify_have_supp_data(response_list)
        self.assert_(flag)
        self.assertEqual(response.protocol, SUPP_PROTOCOL, 'protocol字段错误')
        self.assertEqual(response.suppType, START_CHANNEL_RSP_TYPE, 'supp type字段错误')
        self.assertEqual(response.channelId, str(hex(channel_id))[2:].rjust(4, '0'), 'channel id字段错误')
        self.assertEqual(response.sequence, SEQUENCE_HEX, 'sequence字段错误')
        self.assertEqual(response.code, CODE_NORMAL, 'code字段错误')
        self.assertEqual(response.reserved, RESERVED_NORMAL, '预留字段不足')
        self.assertEqual(response.pieceSize, PIECE_SIZE_NORMAL, 'piecesize字段错误')
        self.assertEqual(get_udp_check_sum(response), udp_checksum(response.data[0:-4]).rjust(4, '0'), 'checksum'
                                                                                                       '字段错误')
        self.assertEqual(response.length, len(response.data)*2, '长度错误')

        if response.ppc != PPC_32:
            if response.ppc != PPC_16:
                self.fail('ppc应为16或者32')

    @func_doc
    def testWrongCheckSumReq(self):
        """
        checksum错误的起播请求不应被处理
        """
        channel_id = get_random_channel_id()
        response_list = supp_start_req(channel_id, SEQUENCE, FILE_URL_DEFAULT, SDK_VERSION_DEFAULT, WRONG_CHECKSUM)
        supp_fin_req(channel_id, FILE_URL_DEFAULT)
        self.assertEqual(response_list, EMPTY_LIST, 'checksum错误的起播请求不应被处理')

    @func_doc
    def testErrorLongReq(self):
        """
        长度过长的起播请求不应被处理
        """
        channel_id = get_random_channel_id()
        response_list = supp_start_req_error(SUPP_START_REQ_LONG, channel_id)
        supp_fin_req(channel_id, FILE_URL_DEFAULT)
        self.assertEqual(response_list, EMPTY_LIST, '异常请求不应被处理')

    @func_doc
    def testErrorShortReq(self):
        """
        长度过短的起播请求不应被处理
        """
        channel_id = get_random_channel_id()
        response_list = supp_start_req_error(SUPP_START_REQ_SHORT, channel_id)
        supp_fin_req(channel_id, FILE_URL_DEFAULT)
        self.assertEqual(response_list, EMPTY_LIST, '异常请求不应被处理')

    @func_doc
    def testWrongProtocolReq(self):
        """
        协议字段错误的起播请求不应被处理
        """
        channel_id = get_random_channel_id()
        response_list = supp_start_req_error(SUPP_START_REQ_PROTOCOL_WRONG, channel_id)
        supp_fin_req(channel_id, FILE_URL_DEFAULT)
        self.assertEqual(response_list, EMPTY_LIST, '异常请求不应被处理')

    @func_doc
    def testCode5Rsp(self):
        """
        带有错误file url的起播请求应能收到各字段正确的回复，并且不会推送数据
        """
        channel_id = get_random_channel_id()
        response_list = supp_start_req(channel_id, SEQUENCE, FILE_URL_NOT_EXIST)
        supp_fin_req(channel_id, FILE_URL_NOT_EXIST)
        response = SUPPStartRspStruct(filter_response_list(response_list, 'startRsp'))
        split_udp_data(response)
        flag = verify_have_supp_data(response_list)
        self.failIf(flag, '请求不存在的频道不应进行数据推送')
        self.assertEqual(response.protocol, SUPP_PROTOCOL, 'protocol字段错误')
        self.assertEqual(response.suppType, START_CHANNEL_RSP_TYPE, 'supp type字段错误')
        self.assertEqual(response.channelId, str(hex(channel_id))[2:].rjust(4, '0'), 'channel id字段错误')
        self.assertEqual(response.sequence, SEQUENCE_HEX, 'sequence字段错误')
        self.assertEqual(response.code, CODE_FILE_NOT_EXIST, 'code字段错误')
        self.assertEqual(response.reserved, RESERVED_NORMAL, '预留字段不足')
        self.assertEqual(response.pieceSize, PIECE_SIZE_ZERO, 'piecesize字段错误')
        self.assertEqual(get_udp_check_sum(response), udp_checksum(response.data[0:-4]).rjust(4, '0'), 'checksum'
                                                                                                       '字段错误')
        self.assertEqual(response.ppc, PPC_ZERO, 'ppc字段错误')
        self.assertEqual(response.length, len(response.data)*2, '长度错误')


if __name__ == '__main__':
    unittest.main()
