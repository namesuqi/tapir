# coding=utf-8
# author: Gu Zehao
# session data
import unittest
from lib.protocol.puff.puff_request import *
from lib.protocol.puff.puff_data import *
from lib.common.decorator import *
from lib.protocol.udp_tools import *


class PuffData(unittest.TestCase):
    def tearDown(self):
        send_puff_fin()

    @func_doc
    def testDataNormal(self):
        """
        校验服务器发送给LF的数据信令长度符合要求，checksum、协议字段、协议类型正确，并且session id与请求信令的session id相等
        """
        response_list = send_puff_request(SESSION_ID_DEFAULT, PEER_ID_DEFAULT, FILE_URL_DEFAULT, CPPC_DEFAULT)
        time.sleep(0.1)
        result = check_puff_protocol(response_list)
        self.assert_(result, 'not puff_protocol')
        signal = check_puff_signal(response_list)
        self.assert_(signal, 'signal code out of range')
        data = response_filter(response_list, 'data')
        self.assert_(data, 'no data')
        response = PuffDataStruct(data)
        split_udp_data(response)
        self.assertEqual(len(response.data), response.length * 2, "数据长度不正确")
        self.assertEqual(get_udp_check_sum(response), udp_checksum(response.data[0:-4]).rjust(4, '0'), "checksum不一致")
        self.assertEqual(response.protocol, PUFF_PROTOCOL, "协议字段错误")
        self.assertEqual(response.puffType, PUFF_SESSION_DAT, "puff类型错误")
        self.assertEqual(response.sessionId, SESSION_ID_DEFAULT_HEX, "session id错误")

    @func_doc
    def testDataCppcZero(self):
        """
        cppc为0的请求不会收到任何data数据包
        """
        response_list = send_puff_request(SESSION_ID_DEFAULT, PEER_ID_DEFAULT, FILE_URL_DEFAULT, CPPC_ZERO)
        time.sleep(2)
        result = check_puff_protocol(response_list)
        self.assert_(result, 'not puff_protocol')
        signal = check_puff_signal(response_list)
        self.assert_(signal, 'signal code out of range')
        data = response_filter(response_list, 'data')
        self.assertEqual(data, None, '应该不返回任何data包')

    @func_doc
    def testDataFileNotExist(self):
        """
        发送频道不存在的请求不会收到任何data数据包
        """
        response_list = send_puff_request_row(SESSION_ID_DEFAULT, PEER_ID_DEFAULT, FILE_URL_NOT_EXIST, CPPC_DEFAULT)
        time.sleep(2)
        result = check_puff_protocol(response_list)
        self.assert_(result, 'not puff_protocol')
        signal = check_puff_signal(response_list)
        self.assert_(signal, 'signal code out of range')
        data = response_filter(response_list, 'data')
        self.assertEqual(data, None, '应该不返回任何data包')

    @func_doc
    def testDataLongurl(self):
        """
        LF请求的url有多余字符串，能正常收到服务器的数据
        """
        response_list = send_puff_request(SESSION_ID_DEFAULT, PEER_ID_DEFAULT, FILE_URL_LONG, CPPC_DEFAULT)
        time.sleep(0.1)
        result = check_puff_protocol(response_list)
        self.assert_(result, 'not puff_protocol')
        signal = check_puff_signal(response_list)
        self.assert_(signal, 'signal code out of range')
        data = response_filter(response_list, 'data')
        self.assert_(data, 'no data')
        response = PuffDataStruct(data)
        split_udp_data(response)
        self.assertEqual(len(response.data), response.length * 2, "数据长度不正确")
        self.assertEqual(get_udp_check_sum(response), udp_checksum(response.data[0:-4]).rjust(4, '0'), "checksum不一致")
        self.assertEqual(response.protocol, PUFF_PROTOCOL, "协议字段错误")
        self.assertEqual(response.puffType, PUFF_SESSION_DAT, "puff类型错误")
        self.assertEqual(response.sessionId, SESSION_ID_DEFAULT_HEX, "session id错误")


if __name__ == '__main__':
    # testData = unittest.TestSuite()
    # testData.addTest(TestData('testNormalData'))
    # fp = open(RESULT_PATH + '/result.html', 'wb')
    # runner = HTMLTestRunner(stream=fp,
    #                         title='puff report')
    # runner.run(testData)
    # fp.close()
    unittest.main()
