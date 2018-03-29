# coding=utf-8
import unittest
from lib.protocol.supp.supp_request import *
from lib.protocol.udp_tools import *
from lib.common.decorator import *


class TestChase(unittest.TestCase):

    def tearDown(self):
        time.sleep(1)

    @func_doc
    def testChaseReqCorrect(self):
        """
        正确的chase请求能收到各字段符合要求的chase回复
        """
        channel_id = get_random_channel_id()
        response_list = supp_chase_req(channel_id, SEQUENCE, OFFSET, FILE_URL_DEFAULT)
        flag = verify_have_supp_data(response_list)
        response = SUPPChaseRspStruct(filter_response_list(response_list, 'chaseRsp'))
        split_udp_data(response)
        self.assert_(flag)
        self.assertEqual(response.protocol, SUPP_PROTOCOL, 'chase rsp 中的协议字段错误')
        self.assertEqual(response.suppType, CHASE_RSP_TYPE, 'chase rsp 中的supp类型字段错误')
        self.assertEqual(response.channelId, str(hex(channel_id))[2:], 'chase rsp 中的channel id字段错误')
        self.assertEqual(response.sequence, SEQUENCE_HEX, 'chase rsp中的sequence字段错误')
        self.assertEqual(response.code, CODE_NORMAL, 'chase rsp中的code字段错误')
        self.assertEqual(response.reserved, RESERVED_NORMAL, 'chase rsp中的预留字段不足')
        self.assertEqual(get_udp_check_sum(response), udp_checksum(response.data[0:-4]).rjust(4, '0'), 'chase rsp中的'
                                                                                                       'checksum错误')
        self.assertEqual(response.length, len(response.data)*2)


    @func_doc
    def testChaseReqWrongUrl(self):
        """
        file url不存在的chase请求能收到各字段符合要求的chase回复
        """
        channel_id = get_random_channel_id()
        response_list = supp_chase_req(channel_id, SEQUENCE, OFFSET, FILE_URL_NOT_EXIST)
        response = SUPPChaseRspStruct(filter_response_list(response_list, 'chaseRsp'))
        split_udp_data(response)
        self.assertEqual(response.protocol, SUPP_PROTOCOL, 'chase rsp 中的协议字段错误')
        self.assertEqual(response.suppType, CHASE_RSP_TYPE, 'chase rsp 中的supp类型字段错误')
        self.assertEqual(response.channelId, str(hex(channel_id))[2:], 'chase rsp 中的channel id字段错误')
        self.assertEqual(response.sequence, SEQUENCE_HEX, 'chase rsp中的sequence字段错误')
        self.assertEqual(response.code, CODE_FILE_NOT_EXIST, 'chase rsp中的code字段错误')
        self.assertEqual(response.reserved, RESERVED_NORMAL, 'chase rsp中的预留字段不足')
        self.assertEqual(get_udp_check_sum(response), udp_checksum(response.data[0:-4]).rjust(4, '0'), 'chase rsp中的'
                                                                                                       'checksum错误')
        self.assertEqual(response.length, len(response.data)*2, '长度错误')


    @func_doc
    def testChaseReqWrongChecksum(self):
        """
        checksum错误的chase请求不会被处理
        """
        channel_id = get_random_channel_id()
        response_list = supp_chase_req(channel_id, SEQUENCE, OFFSET, FILE_URL_DEFAULT, SDK_VERSION_DEFAULT,
                                       WRONG_CHECKSUM)
        self.assertEqual(response_list, EMPTY_LIST, '发送checksum错误的chase req不应受到回复')


if __name__ == '__main__':
    unittest.main()
