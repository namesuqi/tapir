# coding=utf-8
# author: Gu Zehao
# session request and session response

import unittest
from lib.protocol.puff.puff_request import *
from lib.protocol.puff.puff_data import *
import time
from lib.common.path import *
from lib.common.HTMLTestRunner import HTMLTestRunner
from lib.common.decorator import *
from lib.protocol.udp_tools import *


class PuffReqRsp(unittest.TestCase):
    def tearDown(self):
        send_puff_fin()
        time.sleep(5)

    @func_doc
    def testReqNormal(self):
        """
        正确的session请求建立信令能够收到各参数和长度均正确的回复
        """
        response_list = send_puff_request()
        result = check_puff_protocol(response_list)
        self.assert_(result, 'not puff_protocol')
        signal = check_puff_signal(response_list)
        self.assert_(signal, 'signal code out of range')
        resp = response_filter(response_list, 'rsp')
        self.assert_(resp, 'no resp')
        response = PuffResponseStruct(resp)
        split_udp_data(response)
        self.assertEqual(response.protocol, PUFF_PROTOCOL, '返回的协议类型应为puff类型')
        self.assertEqual(response.puffType, PUFF_SESSION_RSP, '返回的puff类型应为建立回复信令')
        self.assertEqual(response.result, PUFF_CODE_OK, '返回的结果应为正常, real is {0}'.format(response.result))
        self.assertEqual(response.sessionId, SESSION_ID_DEFAULT_HEX, '返回的session id应与本次会话的session id一致')
        self.assertEqual(len(response.data), response.length * 2, '返回的信令应长度正确')
        self.assertEqual(get_udp_check_sum(response), udp_checksum(response.data[0:-4]).rjust(4, '0'), 'checksum应一致')

    @func_doc
    def testReqCppcZero(self):
        """
        cppc请求为0的请求建立信令能收到错误码为PUFF_CODE_BAD_REQUEST且长度正确的回复
        """
        response_list = send_puff_request(SESSION_ID_DEFAULT, PEER_ID_DEFAULT, FILE_URL_DEFAULT, CPPC_ZERO)
        result = check_puff_protocol(response_list)
        self.assert_(result, 'not puff_protocol')
        signal = check_puff_signal(response_list)
        self.assert_(signal, 'signal code out of range')
        resp = response_filter(response_list, 'rsp')
        self.assert_(resp, 'no resp')
        response = PuffResponseStruct(resp)
        split_udp_data(response)
        self.assertEqual(response.protocol, PUFF_PROTOCOL, '返回的协议类型应为puff类型')
        self.assertEqual(response.puffType, PUFF_SESSION_RSP, '返回的puff类型应为建立回复信令')
        self.assertEqual(response.result, PUFF_CODE_BAD_REQUEST, '返回的结果应为参数错误, real is {0}'.format(response.result))
        self.assertEqual(response.sessionId, SESSION_ID_DEFAULT_HEX, '返回的session id应与本次会话的session id一致')
        self.assertEqual(len(response.data), response.length * 2, '返回的信令长度应正确')
        self.assertEqual(get_udp_check_sum(response), udp_checksum(response.data[0:-4]).rjust(4, '0'), 'checksum应一致')

    @func_doc
    def testReqFileNotExist(self):
        """
        发送源地址存在但频道名不存在的频道请求建立信令后能收到错误码为PUFF_CODE_NOT_FOUND且长度正确的回复
        """
        response_list = send_puff_request_row(SESSION_ID_DEFAULT, PEER_ID_DEFAULT, FILE_URL_NOT_EXIST)
        result = check_puff_protocol(response_list)
        self.assert_(result, 'not puff_protocol')
        signal = check_puff_signal(response_list)
        self.assert_(signal, 'signal code out of range')
        resp = response_filter(response_list, 'rsp')
        self.assert_(resp, 'no resp')
        response = PuffResponseStruct(resp)
        split_udp_data(response)
        self.assertEqual(response.protocol, PUFF_PROTOCOL, '返回回的协议类型应为puff类型')
        self.assertEqual(response.puffType, PUFF_SESSION_RSP, '返回的puff类型应为建立回复信令')
        self.assertEqual(response.result, PUFF_CODE_NOT_FOUND, '返回的结果应为文件不存在, real is {0}'.format(response.result))
        self.assertEqual(response.sessionId, SESSION_ID_DEFAULT_HEX, '返回的session id应与本次会话的session id一致')
        self.assertEqual(len(response.data), response.length * 2, '返回的信令长度应正确')
        self.assertEqual(get_udp_check_sum(response), udp_checksum(response.data[0:-4]).rjust(4, '0'), 'checksum应一致')
        time.sleep(5)

    @func_doc
    def testReqFileNotExist1(self):
        """
        发送源地址不存在的频道请求建立信令后能收到错误码为PUFF_CODE_NOT_FOUND且长度正确的回复
        """
        response_list = send_puff_request_row(SESSION_ID_DEFAULT, PEER_ID_DEFAULT, FILE_URL_NOT_EXIST1)
        result = check_puff_protocol(response_list)
        self.assert_(result, 'not puff_protocol')
        signal = check_puff_signal(response_list)
        self.assert_(signal, 'signal code out of range')
        resp = response_filter(response_list, 'rsp')
        self.assert_(resp, 'no resp')
        response = PuffResponseStruct(resp)
        split_udp_data(response)
        self.assertEqual(response.protocol, PUFF_PROTOCOL, '返回回的协议类型应为puff类型')
        self.assertEqual(response.puffType, PUFF_SESSION_RSP, '返回的puff类型应为建立回复信令')
        self.assertEqual(response.result, PUFF_CODE_NOT_FOUND, '返回的结果应为文件不存在, real is {0}'.format(response.result))
        self.assertEqual(response.sessionId, SESSION_ID_DEFAULT_HEX, '返回的session id应与本次会话的session id一致')
        self.assertEqual(len(response.data), response.length * 2, '返回的信令长度应正确')
        self.assertEqual(get_udp_check_sum(response), udp_checksum(response.data[0:-4]).rjust(4, '0'), 'checksum应一致')
        time.sleep(5)


if __name__ == '__main__':
    # testReqRsp = unittest.TestSuite()
    # testReqRsp.addTest(TestReqRsp("testReqNormal"))
    # testReqRsp.addTest(TestReqRsp("testReqCppcZero"))
    # testReqRsp.addTest(TestReqRsp("testReqFileNotExist"))
    #  fp = open(RESULT_PATH + '/result.html', 'wb')
    #  runner = HTMLTestRunner(stream=fp,
    #                          title='puff report')
    # runner.run(testReqRsp)
    # fp.close()
    unittest.main()
