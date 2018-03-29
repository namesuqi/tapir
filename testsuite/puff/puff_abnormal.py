# coding=utf-8
# author: Gu Zehao
# abnormal cases
import unittest
from lib.protocol.puff.puff_request import *
from lib.protocol.puff.puff_data import *
from lib.common.path import *
from lib.common.HTMLTestRunner import HTMLTestRunner
from lib.common.decorator import *


class PuffAbnormal(unittest.TestCase):

    def tearDown(self):
        send_puff_fin()
        time.sleep(5)

    @func_doc
    def testRsp2Srv(self):
        """
        向live push发送符合格式的建立回复信令，服务器不作响应
        """
        response = send_rsp2srv()
        self.assertEqual(response, None)
        time.sleep(1)
        self.assert_(send_puff_request())

    @func_doc
    def testData2Srv(self):
        """
        向live push发送符合格式的数据信令，服务器不作响应
        """
        response = send_data2srv()
        self.assertEqual(response, None)
        time.sleep(1)
        self.assert_(send_puff_request())

    @func_doc
    def testHib2Srv(self):
        """
        在没有建立正确会话的情况下向push srv发送hib信令，服务器不作响应
        """
        response = send_puff_hib()
        self.assertEqual(response, EMPTY_LIST)
        time.sleep(1)
        self.assert_(send_puff_request())

    @func_doc
    def testFin2Srv(self):
        """
        在没有建立正确会话的情况下向push srv发送fin信令，服务器不作响应
        """
        self.assertEqual(send_puff_fin(), EMPTY_LIST)
        time.sleep(1)
        self.assert_(send_puff_request())

    @func_doc
    def test2SrvTailLong(self):
        """
        向live push发送其长于正常信令的信令（在尾部添加），服务器不作响应
        """
        response = send_tail_long_data()
        self.assertEqual(response, None)
        time.sleep(1)
        self.assert_(send_puff_request())

    @func_doc
    def test2SrvHeadLong(self):
        """
        向live push发送其长于正常信令的信令（在头部添加），服务器不作响应
        """
        response = send_head_long_data()
        self.assertEqual(response, None)
        time.sleep(1)
        self.assert_(send_puff_request())

    @func_doc
    def test2SrvTailShort(self):
        """
        向live push发送其短于正常信令的信令（在尾部减少），服务器不作响应
        """
        response = send_tail_short_data()
        self.assertEqual(response, None)
        time.sleep(1)
        self.assert_(send_puff_request())

    @func_doc
    def test2SrcHeadShort(self):
        """
        向live push发送其短于正常信令的信令（在头部减少），服务器不作响应
        """
        response = send_head_short_data()
        self.assertEqual(response, None)
        time.sleep(1)
        self.assert_(send_puff_request())


if __name__ == '__main__':
    # testAbnormal = unittest.TestSuite()
    # testAbnormal.addTest(TestAbnormal("testRsp2Srv"))
    # testAbnormal.addTest(TestAbnormal("testData2Srv"))
    # testAbnormal.addTest(TestAbnormal("testHib2Srv"))
    # testAbnormal.addTest(TestAbnormal("testFin2Srv"))
    # testAbnormal.addTest(TestAbnormal("test2SrvTailLong"))
    # testAbnormal.addTest(TestAbnormal("test2SrvHeadLong"))
    # testAbnormal.addTest(TestAbnormal("test2SrvTailShort"))
    # testAbnormal.addTest(TestAbnormal("test2SrcHeadShort"))
    # fp = open(RESULT_PATH + '/result.html', 'wb')
    # runner = HTMLTestRunner(stream=fp,
    #                         title='puff report')
    # runner.run(testAbnormal)
    # fp.close()
    unittest.main()
