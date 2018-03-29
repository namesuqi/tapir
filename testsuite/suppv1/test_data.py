# coding=utf-8
import unittest
from lib.protocol.supp.supp_request import *
from lib.protocol.udp_tools import *
from lib.common.decorator import *


class MyTestCase(unittest.TestCase):

    def tearDown(self):
        time.sleep(1)

    @func_doc
    def testStartChannelData(self):
        """
        开始频道请求到的数据 各字段符合要求
        """
        channel_id = get_random_channel_id()
        response_list = supp_start_req(channel_id, SEQUENCE, FILE_URL_DEFAULT)
        supp_fin_req(channel_id, FILE_URL_DEFAULT)
        flag = verify_have_supp_data(response_list)
        if flag:
            response = SUPPStartRspStruct(filter_response_list(response_list, 'data'))
            split_udp_data(response)
            self.assertEqual(response.protocol, SUPP_PROTOCOL, 'protocol字段错误')
            self.assertEqual(response.suppType, CHUNK_DATA_TYPE, 'supp type字段错误')
            self.assertEqual(response.channelId, str(hex(channel_id))[2:].rjust(4, '0'), 'channel id字段错误')
            self.assertEqual(get_udp_check_sum(response), udp_checksum(response.data[0:-4]).rjust(4, '0'), 'checksum字'
                                                                                                           '段错误')
            self.assertEqual(response.length, len(response.data) * 2, '长度错误')

        else:
            self.fail('请求数据失败')

    @func_doc
    def testAckData(self):
        """
        ack维持推送的数据 各字段符合要求
        """
        channel_id = get_random_channel_id()
        response_list = supp_start_req_ack(channel_id, SEQUENCE, FILE_URL_DEFAULT, FILE_URL_DEFAULT)
        supp_fin_req(channel_id, FILE_URL_DEFAULT)
        flag = verify_have_supp_data(response_list)
        if flag:
            response = SUPPStartRspStruct(filter_response_list(response_list, 'data'))
            split_udp_data(response)
            self.assertEqual(response.protocol, SUPP_PROTOCOL, 'protocol字段错误')
            self.assertEqual(response.suppType, CHUNK_DATA_TYPE,'supp type字段错误')
            self.assertEqual(response.channelId, str(hex(channel_id))[2:].rjust(4, '0'), 'channel id字段错误')
            self.assertEqual(get_udp_check_sum(response), udp_checksum(response.data[0:-4]).rjust(4, '0'),'checkssum'
                                                                                                          '字段错误')
            self.assertEqual(response.length, len(response.data) * 2, '长度错误')

        else:
            self.fail('请求数据失败')

    @func_doc
    def testChaseData(self):
        """
        chase请求到的数据 各字段符合要求
        """
        channel_id = get_random_channel_id()
        response_list = supp_chase_req(channel_id, SEQUENCE, OFFSET, FILE_URL_DEFAULT)
        supp_fin_req(channel_id, FILE_URL_DEFAULT)
        flag = verify_have_supp_data(response_list)
        if flag:
            response = SUPPStartRspStruct(filter_response_list(response_list, 'data'))
            split_udp_data(response)
            self.assertEqual(response.protocol, SUPP_PROTOCOL, 'protocol字段错误')
            self.assertEqual(response.suppType, CHUNK_DATA_TYPE, 'supp type字段错误')
            self.assertEqual(response.channelId, str(hex(channel_id))[2:].rjust(4, '0'), 'channel id字段错误')
            self.assertEqual(get_udp_check_sum(response), udp_checksum(response.data[0:-4]).rjust(4, '0'), 'checksum'
                                                                                                           '字段错误')
            self.assertEqual(response.length, len(response.data) * 2, '长度错误')

        else:
            self.fail('请求数据失败')

if __name__ == '__main__':
    unittest.main()
