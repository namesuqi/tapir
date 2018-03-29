# coding=utf-8
# linux sdk login testcase

import unittest
from lib.sdk.common_tool.sdk_handle import *
from lib.sdk.sdk_constant import *
from lib.common.decorator import *
from lib.sdk.common_tool.specific_handle import *
from lib.sdk.common_tool.verify_handle import *


class TestLogin(unittest.TestCase):
    @func_doc
    def setUp(self):
        """
        上传sdk，使用ys_service_static版本
        """
        execute_command(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD, 'iptables -F')
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
    def testLoginRequest(self):
        """
        testlink tc-13 && tc-780
        SDK发送登录请求; SDK登录汇报macs字段正确
        @owner: jinyifan
        """
        start_capture(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD, REMOTE_ETH)
        start_sdk(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD, REMOTE_SDK_PATH)
        time.sleep(15)
        stop_capture(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD)

        # 判断login字段是否都存在
        login_req = verify_sdk_http_request("/session/peers/", "POST", 'version', 'natType', 'publicIP', 'publicPort',
                                            'privateIP', 'privatePort', 'stunIP', 'deviceInfo', 'macs')
        print "result is:", login_req

        # 采集SDK macs字段，只采集一条
        get_macs = get_interface_macs(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD)
        macs = get_macs[1].upper()
        macs_result = ("{'name': '" + get_macs[0] + "', 'addr': '" + macs + "'}").encode("utf-8")

        # 检验SDK login请求字段存在且内容正确(由于在同一台机器跑，故IP,natType和deviceInfo字段内容写死)
        self.assertEqual(login_req['version'], EXPECT_SDK_VERSION, "version not equal")
        self.assertEqual(login_req['natType'], EXPECT_NATTYPE, "natType wrong")
        self.assertEqual(login_req['publicIP'], EXPECT_PUBLICIP, "publicIP wrong")
        self.assertEqual(login_req['privateIP'], EXPECT_PRIVATEIP, "privateIP wrong")
        self.assertEqual(login_req['stunIP'], EXPECT_STUN_IP, "stunIP wrong")
        self.assertEqual(str(login_req['macs']), macs_result, "macs wrong")
        self.assertEqual(login_req['deviceInfo'], EXPECT_DEVICEINFO, "deviceInfo wrong")

    @func_doc
    def testLoginOK(self):
        """
        testlink tc-1
        SDK登录成功，dashboard中ajax/login显示信息与实际向ts发送的Login请求中信息一致
        @owner: jinyifan
        """
        start_capture(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD, REMOTE_ETH)
        start_sdk(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD, REMOTE_SDK_PATH)
        time.sleep(15)
        stop_capture(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD)

        # 检验SDK登录成功，dashboard中ajax/login显示信息与实际向ts发送的Login请求中信息一致
        login_req = verify_sdk_http_request("/session/peers/", "POST", 'version', 'natType', 'publicIP', 'publicPort',
                                            'privateIP', 'privatePort', 'stunIP', 'deviceInfo', 'macs')
        resp_text = get_sdk_dashboard(REMOTE_SDK_IP, SDK_PORT, LOGIN_DASHBOARD_URL)
        dashboard_result = get_json_value(resp_text)
        self.assertEqual(dashboard_result['status'], 'E_OK', "status is not OK")
        self.assertEqual(dashboard_result['natType'], login_req['natType'], "natType different")
        self.assertEqual(dashboard_result['publicIP'], login_req['publicIP'], "publicIP different")
        self.assertEqual(dashboard_result['publicPort'], login_req['publicPort'], "publicPort different")
        self.assertEqual(dashboard_result['privateIP'], login_req['privateIP'], "privateIP different")
        self.assertEqual(dashboard_result['privatePort'], login_req['privatePort'], "privatePort different")
        self.assertEqual(dashboard_result['stunIP'], login_req['stunIP'], "stunIP different")

    @func_doc
    def testLoginRetry(self):
        """
        testlink tc-4
        SDK登录失败后尝试登录
        @owner: jinyifan
        """
        execute_command(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD, DROP_TCP)
        start_sdk(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD, REMOTE_SDK_PATH)
        time.sleep(16)
        resp_text = get_sdk_dashboard(REMOTE_SDK_IP, SDK_PORT, LOGIN_DASHBOARD_URL)
        dashboard_result = get_json_value(resp_text)
        self.assertEqual(dashboard_result['status'], 'E_TS_NOT_LOGIN', "status should not be OK")
        print "last_login:", dashboard_result['last_login']

        time.sleep(7)
        resp_text = get_sdk_dashboard(REMOTE_SDK_IP, SDK_PORT, LOGIN_DASHBOARD_URL)
        dashboard_result = get_json_value(resp_text)
        self.assertLessEqual(dashboard_result['last_login'], 11000, 'timeout is more than 11s')

        execute_command(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD, RECOVER_TCP)
        time.sleep(11)
        resp_text = get_sdk_dashboard(REMOTE_SDK_IP, SDK_PORT, LOGIN_DASHBOARD_URL)
        dashboard_result = get_json_value(resp_text)
        self.assertEqual(dashboard_result['status'], 'E_OK', "status should be OK")


if __name__ == '__main__':
    unittest.main()
