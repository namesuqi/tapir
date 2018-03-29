# coding=utf-8
import unittest
from lib.protocol.supp.supp_request import *
from lib.protocol.udp_tools import *
from lib.common.decorator import *


class MyTestCase(unittest.TestCase):

    def tearDown(self):
        time.sleep(1)

    @func_doc
    def testAckCorrect(self):
        """
        发送正确的ack能维持推送数据
        """
        channel_id = get_random_channel_id()
        response_list = supp_start_req_ack(channel_id, SEQUENCE, FILE_URL_DEFAULT, FILE_URL_DEFAULT)
        supp_fin_req(channel_id, FILE_URL_DEFAULT)
        flag = verify_have_supp_data(response_list)
        self.assert_(flag, 'ack应能维持推送数据')

    @func_doc
    def testAckWrongCheckSum(self):
        """
        发送checksum错误的ack不能维持推送数据
        """
        channel_id = get_random_channel_id()
        response_list = supp_start_req_ack(channel_id, SEQUENCE, FILE_URL_DEFAULT, FILE_URL_DEFAULT, WRONG_CHECKSUM)
        supp_fin_req(channel_id, FILE_URL_DEFAULT)
        flag = verify_have_supp_data(response_list)
        self.failIf(flag, 'checksum错误的ack不应维持推送数据')

    @func_doc
    def testAckWrongFileUrl(self):
        """
        发送file url与播放频道不一致的ack不能维持推送数据
        """
        channel_id = get_random_channel_id()
        response_list = supp_start_req_ack(channel_id, SEQUENCE, FILE_URL_DEFAULT, FILE_URL_NOT_EXIST)
        supp_fin_req(channel_id, FILE_URL_DEFAULT)
        self.assertEqual(response_list, EMPTY_LIST, 'file url错误的ack不应能维持推送数据')


if __name__ == '__main__':
    unittest.main()
