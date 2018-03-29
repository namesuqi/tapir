# coding=utf-8
# author: Gu Zehao
# session hib

import unittest
from lib.protocol.puff.puff_request import *
from lib.protocol.puff.puff_data import *
import time
from lib.common.path import *
from lib.common.HTMLTestRunner import HTMLTestRunner
from lib.common.decorator import *
from lib.protocol.udp_tools import *


class PuffHib(unittest.TestCase):

    def tearDown(self):
        send_puff_fin()
        time.sleep(1)

    @func_doc
    def testHibT9(self):
        """
        LF在规定时间(30s)给live-push-srv发送正确的puff-hib后（每9秒一次），live-push-srv不会停止推送数据
        """
        t0 = time.time()
        send_puff_request()
        for i in range(10):
            while True:
                time.sleep(1)
                if time.time() - t0 > 9 * (i + 1):
                    break
            send_puff_hib()
        result = check_puff_protocol(send_puff_hib())
        self.assert_(result, 'not puff_protocol')
        signal = check_puff_signal(send_puff_hib())
        self.assert_(signal, 'signal code out of range')
        self.assert_(verify_push_data(), "100秒后数据中断")

    @func_doc
    def testHibT29(self):
        """
        LF在规定时间(30s)给live-push-srv发送正确的puff-hib后（每29秒一次），live-push-srv不会停止推送数据
        :return:
        """
        t0 = time.time()
        send_puff_request()
        for i in range(3):
            while True:
                time.sleep(1)
                if time.time()-t0 > 28*(i+1):
                    break
            send_puff_hib()
        result = check_puff_protocol(send_puff_hib())
        self.assert_(result, 'not puff_protocol')
        signal = check_puff_signal(send_puff_hib())
        self.assert_(signal, 'signal code out of range')
        self.assert_(verify_push_data(), "90秒后数据中断")

    @func_doc
    def testHibOutTime(self):
        """
        LF未在规定时间（30s）内live push srv发送puff hib后live push srv停止推送数据
        """
        resp = send_puff_request()
        self.assertTrue(resp, 'no resp data')
        time.sleep(31)
        self.failIf(verify_push_data(), "无心跳情况下超出三十秒不应推送数据")

    @func_doc
    def testInvalidPeerId(self):
        """
        发送的hib中peer id错误时，live push srv视作没有发送hib
        """
        resp = send_puff_request()
        self.assertTrue(resp, 'no resp data')
        time.sleep(15)
        send_puff_hib(SESSION_ID_DEFAULT, PEER_ID_INVALID)
        time.sleep(16)
        self.failIf(verify_push_data(), "带有错误peer id的心跳不应维持推送数据")

    @func_doc
    def testInvalidUrlMD5(self):
        """
        发送的hib中url MD5错误时，live push srv视作没有发送hib
        """
        resp = send_puff_request()
        self.assertTrue(resp, 'no resp data')
        time.sleep(15)
        send_puff_hib(SESSION_ID_DEFAULT, PEER_ID_DEFAULT, FILE_URL_TEST3)
        time.sleep(16)
        self.failIf(verify_push_data(), "带有错误file url的心跳不应维持推送数据")


if __name__ == '__main__':
    # testHib = unittest.TestSuite()
    # testHib.addTest(TestHib("testHibT9"))
    # testHib.addTest(TestHib("testHibT25"))
    # testHib.addTest(TestHib("testHibOutTime"))
    # testHib.addTest(TestHib("testInvalidPeerId"))
    # testHib.addTest(TestHib("testInvalidUrlMD5"))
    # fp = open(RESULT_PATH + '/result.html', 'wb')
    # runner = HTMLTestRunner(stream=fp,
    #                         title='puff report')
    # runner.run(testHib)
    # fp.close()
    unittest.main()
