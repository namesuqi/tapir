# coding=utf-8

import unittest
from lib.protocol.supp.supp_request import *
from lib.protocol.udp_tools import *
from lib.common.decorator import *


class TestFin(unittest.TestCase):
    def tearDown(self):
        time.sleep(1)

    @func_doc
    def testMatchedGroup(self):
        """
        对照组
        """
        channel_id = get_random_channel_id()
        response_list = supp_start_req_ack(channel_id, SEQUENCE, FILE_URL_DEFAULT, FILE_URL_DEFAULT)
        flag = verify_have_supp_data(response_list)
        self.assert_(flag, '对照组错误')
        response_list = supp_ack(channel_id, FILE_URL_DEFAULT, ACK_MAX_RECEIVED_SEQNO)
        flag = verify_have_supp_data(response_list)
        self.assert_(flag, '对照组错误')

    @func_doc
    def testFinCorrect(self):
        """
        正确的结束信令能让live push停止推送数据
        """
        channel_id = get_random_channel_id()
        response_list = supp_start_req_ack(channel_id, SEQUENCE, FILE_URL_DEFAULT, FILE_URL_DEFAULT)
        flag = verify_have_supp_data(response_list)
        self.assert_(flag, '发送ack应能维持推送数据')
        supp_fin_req(channel_id, FILE_URL_DEFAULT)
        time.sleep(0.5)
        response_list = supp_ack(channel_id, FILE_URL_DEFAULT, ACK_MAX_RECEIVED_SEQNO)
        flag = verify_have_supp_data(response_list)
        self.failIf(flag, '发送fin后再发送ack不应能维持推送数据')

    @func_doc
    def testFinWrongFileUrl(self):
        """
        带有错误file url的结束信令不应起效
        """
        channel_id = get_random_channel_id()
        response_list = supp_start_req_ack(channel_id, SEQUENCE, FILE_URL_DEFAULT, FILE_URL_DEFAULT)
        flag = verify_have_supp_data(response_list)
        self.assert_(flag, '发送ack应能维持推送数据')
        supp_fin_req(channel_id, FILE_URL_NOT_EXIST)
        response_list = supp_ack(channel_id, FILE_URL_DEFAULT, ACK_MAX_RECEIVED_SEQNO)
        flag = verify_have_supp_data(response_list)
        self.assert_(flag, '发送file url错误的fin不应起效')

    @func_doc
    def testFinWrongCheckSum(self):
        """
        带有错误checksum的结束信令不应起效
        """
        channel_id = get_random_channel_id()
        response_list = supp_start_req_ack(channel_id, SEQUENCE, FILE_URL_DEFAULT, FILE_URL_DEFAULT)
        flag = verify_have_supp_data(response_list)
        self.assert_(flag, '发送ack应能维持推送数据')
        supp_fin_req(channel_id, FILE_URL_DEFAULT, WRONG_CHECKSUM)
        response_list = supp_ack(channel_id, FILE_URL_DEFAULT, ACK_MAX_RECEIVED_SEQNO)
        flag = verify_have_supp_data(response_list)
        self.assert_(flag, '发送checksum错误的fin不应起效')


if __name__ == '__main__':
    unittest.main()
