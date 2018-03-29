# coding=utf-8
# author: Gu Zehao
# session fin
# 由于LF发送FIN之后可能会收到live push flying的data包。因此在发送第一次FIN包之后间隔一段时间再发送心跳包，若live push无数据返回，则表明FIN包发送成功
import unittest
from lib.protocol.puff.puff_request import *
from lib.protocol.puff.puff_data import *
import time
from lib.common.path import *
from lib.common.HTMLTestRunner import HTMLTestRunner
from lib.common.decorator import *
from lib.protocol.udp_tools import *


class PuffFin(unittest.TestCase):
    """
    雷锋可能会发reason是OK, NoResp, NoData原因的fin包
    所以本测试套件只测这三种
    """

    def tearDown(self):
        send_puff_fin()
        time.sleep(1)

    @func_doc
    def testFinReasonOk(self):
        """
        给正给LF推送数据的live push srv发送reason值为0(正常)的正确puff fin后，push srv停止数据推送
        """
        send_puff_request()
        time.sleep(0.1)
        self.assert_(verify_push_data(), "请求不到数据")
        send_puff_fin(PUFF_CODE_OK)
        time.sleep(1)
        response_list = send_puff_hib()
        self.failIf(response_list, "发送FIN后不应继续推送数据")

    @func_doc
    def testFinReasonNoResp(self):
        """
        给正给LF推送数据的live push srv发送reason值为4（no resp）的正确puff fin后，push srv停止数据推送
        """
        send_puff_request()
        time.sleep(0.1)
        self.assert_(verify_push_data(), "请求不到数据")
        send_puff_fin(PUFF_CODE_NO_RESP)
        time.sleep(1)
        response_list = send_puff_hib()
        self.failIf(response_list, "发送FIN后不应继续推送数据")

    @func_doc
    def testFinReasonNoData(self):
        """
        给正给LF推送数据的live push srv发送reason值为5(no data)的正确puff fin后，push srv停止数据推送
        """
        send_puff_request()
        time.sleep(0.1)
        self.assert_(verify_push_data(), "请求不到数据")
        send_puff_fin(PUFF_CODE_NO_DATA)
        time.sleep(1)
        response_list = send_puff_hib()
        self.failIf(response_list, "发送FIN后不应继续推送数据")

    @func_doc
    def testFinInvalidPeerId(self):
        """
        给正给LF推送数据的live push srv发送peer_id错误的puff fin后，push srv不作响应，照常推送数据
        """
        send_puff_request()
        time.sleep(0.1)
        self.assert_(verify_push_data(), "请求不到数据")
        send_puff_fin(PUFF_CODE_NO_RESP, SESSION_ID_DEFAULT, PEER_ID_INVALID)
        time.sleep(1)
        response_list = send_puff_hib()
        result = check_puff_protocol(response_list)
        self.assert_(result, 'not puff_protocol')
        signal = check_puff_signal(response_list)
        self.assert_(signal, 'signal code out of range')
        data = response_filter(response_list, 'data')
        self.assert_(data, "发送错误的FIN后应继续推送数据")

    @func_doc
    def testFinInvalidUrlMd5(self):
        """
        给正给LF推送数据的live push srv发送url MD5错误的puff fin后，push srv不作响应，照常推送数据
        """
        send_puff_request()
        time.sleep(0.1)
        self.assert_(verify_push_data(), "请求不到数据")
        send_puff_fin(PUFF_CODE_NO_RESP, SESSION_ID_DEFAULT, PEER_ID_DEFAULT, FILE_URL_NOT_EXIST)
        time.sleep(1)
        response_list = send_puff_hib()
        result = check_puff_protocol(response_list)
        self.assert_(result, 'not puff_protocol')
        signal = check_puff_signal(response_list)
        self.assert_(signal, 'signal code out of range')
        data = response_filter(response_list, 'data')
        self.assert_(data, "发送错误的FIN后应继续推送数据")


if __name__ == '__main__':
    # testFin = unittest.TestSuite()
    # testFin.addTest(PuffFin("testFinReasonNoResp"))
    # testFin.addTest(TestFin("testFinReason05"))
    # testFin.addTest(TestFin("testFinInvalidPeerId"))
    # testFin.addTest(TestFin("testFinInvalidUrlMd5"))
    # fp = open(RESULT_PATH + '/result.html', 'wb')
    # runner = HTMLTestRunner(stream=fp,
    #                         title='puff report')
    # runner = unittest.TextTestRunner()
    # runner.run(testFin)
    # fp.close()
    unittest.main()
