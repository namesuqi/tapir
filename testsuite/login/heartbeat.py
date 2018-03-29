# coding=utf-8
# linux sdk heartbeat testcase

import unittest
from lib.sdk.common_tool.sdk_handle import *
from lib.sdk.sdk_constant import *
from lib.common.decorator import *
from lib.sdk.common_tool.specific_handle import *
from lib.sdk.common_tool.verify_handle import *


class TestHeartbeat(unittest.TestCase):
    @func_doc
    def setUp(self):
        """
        上传sdk，使用ys_service_static版本
        """
        remove_file(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD, REMOTE_SDK_API_PATH, LOG_FILE)
        upload_sdk(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD, REMOTE_SDK_PATH)

    @func_doc
    def tearDown(self):
        """
        移除sdk
        """
        stop_sdk(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD)
        remove_sdk(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD, REMOTE_SDK_PATH)

    @func_doc
    def test_Heartbeat_Login(self):
        """
        testlink tc-12
        摘要
        SDK login之后每隔10min定时发送心跳请求
        @owner: jinyifan
        """
        start_capture(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD, REMOTE_ETH)
        start_sdk(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD, REMOTE_SDK_PATH)

        # 判断SDK login之后10min发送心跳请求
        time.sleep(10*60-2)
        heartbeat_req = verify_sdk_http_request("/session/peers/", "GET")
        print "result is:", heartbeat_req
        self.assertEqual(heartbeat_req, False, 'should not have heartbeat')

        time.sleep(3)
        heartbeat_req = verify_sdk_http_request("/session/peers/", "GET")
        print "result is:", heartbeat_req
        self.assertNotEqual(heartbeat_req, False, 'should have heartbeat')


if __name__ == '__main__':
    unittest.main()
