# coding=utf-8
# linux sdk init port testcase
import unittest
from lib.sdk.common_tool.sdk_handle import *
from lib.sdk.common_tool.specific_handle import *
from lib.sdk.common_tool.verify_handle import *
from lib.sdk.sdk_constant import *
from lib.common.decorator import *


class TestPort(unittest.TestCase):

    @func_doc
    def setUp(self):
        """
        上传sdk
        """
        remove_sdk(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD, REMOTE_SDK_PATH)
        upload_sdk(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD, REMOTE_SDK_PATH)

    @func_doc
    def tearDown(self):
        """
        移除sdk
        """
        stop_sdk(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD)
        remove_sdk(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD, REMOTE_SDK_PATH)

    @func_doc
    def testInitDefaultPort(self):
        """
        testlink tc-14
        SDK默认端口启动
        @owner: guzehao
        @reviewer: jinyifan
        """
        not_occupied = verify_port_not_occupancy(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD, SDK_HTTP_PORT, SDK_RTMP_PORT,
                                             SDK_DASHBOARD_PORT)
        self.assertTrue(not_occupied, 'port has been occupied')

        start_sdk(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD, REMOTE_SDK_PATH)
        time.sleep(2)
        occupied = verify_port_occupancy(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD, SDK_HTTP_PORT, SDK_RTMP_PORT,
                                             SDK_DASHBOARD_PORT)
        self.assertTrue(occupied, 'sdk init should occupied 32717 32718 32719')
        rsp = get_sdk_dashboard(REMOTE_SDK_IP, SDK_PORT, VERSION_DASHBOARD_URL)
        core = get_json_value(rsp, 'core')
        self.assertEqual(core, EXPECT_SDK_VERSION, 'dashboard is not addressable, sdk init failed')

    @func_doc
    def testInitSpecifiedPortNormal(self):
        """
        testlink tc-370
        SDK指定端口启动（正常范围）
        @owner: guzehao
        @reviewer: jinyifan
        """
        not_occupied = verify_port_not_occupancy(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD, '40000', '40001', '40002')
        self.assertTrue(not_occupied, 'port has been occupied')
        start_sdk(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD, REMOTE_SDK_PATH, '40000')
        time.sleep(2)
        occupied = verify_port_occupancy(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD, '40000', '40001', '40002')
        self.assertTrue(occupied, 'sdk init should occupy 40000 40001 40002')
        rsp = get_sdk_dashboard(REMOTE_SDK_IP, '40000', VERSION_DASHBOARD_URL)
        core = get_json_value(rsp, 'core')
        self.assertEqual(core, EXPECT_SDK_VERSION, 'dashboard is not addressable, sdk init failed')

    @func_doc
    def testInitSpecifiedPortPartExceed(self):
        """
        testlink tc-372
        SDK指定端口启动（部分端口超出正常范围）
        owner: guzehao
        @reviewer: jinyifan
        """
        not_occupied = verify_port_not_occupancy(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD, '65535')
        self.assertTrue(not_occupied, '65535 has been occupied')
        start_sdk(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD, REMOTE_SDK_PATH, '65535')
        time.sleep(2)
        occupied = verify_port_occupancy(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD, '65535')
        self.assertTrue(occupied, 'sdk init should occupy 65535')
        rsp = get_sdk_dashboard(REMOTE_SDK_IP, '65535', VERSION_DASHBOARD_URL)
        core = get_json_value(rsp, 'core')
        self.assertEqual(core, EXPECT_SDK_VERSION, 'dashboard is not addressable, sdk init failed')

    @func_doc
    def testInitSpecifiedPortAllExceed(self):
        """
        testlink tc-373
        SDK指定端口启动（指定端口大于65535）
        @owner: guzehao
        @reviewer: jinyifan
        """
        start_sdk(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD, REMOTE_SDK_PATH, '65536')
        occupied = verify_port_occupancy(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD, SDK_HTTP_PORT, SDK_RTMP_PORT,
                                             SDK_DASHBOARD_PORT)
        self.assertTrue(occupied, 'ys_service should occupy default port when specified port all exceed')
        rsp = get_sdk_dashboard(REMOTE_SDK_IP, SDK_PORT, VERSION_DASHBOARD_URL)
        core = get_json_value(rsp, 'core')
        self.assertEqual(core, EXPECT_SDK_VERSION, 'dashboard is not addressable, sdk init failed')

    @func_doc
    def testInitSpecifiedPortString(self):
        """
        testlink tc-375
        SDK指定端口启动（字符串）
        @owner: guzehao
        @reviewer: jinyifan
        """
        not_occupied = verify_port_not_occupancy(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD, SDK_HTTP_PORT, SDK_RTMP_PORT,
                                             SDK_DASHBOARD_PORT)
        self.assertTrue(not_occupied, 'port has been occupied')
        start_sdk(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD, REMOTE_SDK_PATH, 'abcd')
        time.sleep(2)
        occupied = verify_port_occupancy(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD, SDK_HTTP_PORT, SDK_RTMP_PORT,
                                             SDK_DASHBOARD_PORT)
        self.assertTrue(occupied, 'sdk init with string port should occupy 32717 32718 32719')
        rsp = get_sdk_dashboard(REMOTE_SDK_IP, '32717', VERSION_DASHBOARD_URL)
        core = get_json_value(rsp, 'core')
        self.assertEqual(core, EXPECT_SDK_VERSION, 'dashboard is not addressable, sdk init failed')
        stop_sdk(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD)
        start_sdk(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD, REMOTE_SDK_PATH, 'A4000')
        time.sleep(2)
        rsp = get_sdk_dashboard(REMOTE_SDK_IP, '32717', VERSION_DASHBOARD_URL)
        core = get_json_value(rsp, 'core')
        self.assertEqual(core, EXPECT_SDK_VERSION, 'dashboard is not addressable, sdk init failed')

    @func_doc
    def testInitSpecifiedPortZero(self):
        """
        testlink tc-379
        SDK指定端口启动（0）
        @owner: guzehao
        @reviewer: jinyifan
        """
        not_occupied = verify_port_not_occupancy(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD, SDK_HTTP_PORT, SDK_RTMP_PORT,
                                                SDK_DASHBOARD_PORT)
        self.assertTrue(not_occupied, '32717 32718 32719 has been occupied')
        start_sdk(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD, REMOTE_SDK_PATH, '0')
        time.sleep(2)
        occupied = verify_port_occupancy(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD, SDK_HTTP_PORT, SDK_RTMP_PORT,
                                        SDK_DASHBOARD_PORT)
        self.assertTrue(occupied, 'sdk init with zero port should occupy 32717 32718 32719')
        rsp = get_sdk_dashboard(REMOTE_SDK_IP, '32719', VERSION_DASHBOARD_URL)
        core = get_json_value(rsp, 'core')
        self.assertEqual(core, EXPECT_SDK_VERSION, 'dashboard is not addressable, sdk init failed')

    @func_doc
    def testInitSpecifiedPortNegativeNumber(self):
        """
        testlink tc-381
        SDK指定端口启动（小于0）
        @owner: guzehao
        @reviewer: jinyifan
        """
        not_occupied = verify_port_not_occupancy(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD, SDK_HTTP_PORT, SDK_RTMP_PORT,
                                             SDK_DASHBOARD_PORT)
        self.assert_(not_occupied, 'port has been occupied')
        start_sdk(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD, REMOTE_SDK_PATH, '-1')
        time.sleep(2)
        occupied = verify_port_occupancy(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD, '65535')
        self.assert_(occupied, 'init sdk with negative number should occupy (65536+port)')
        rsp = get_sdk_dashboard(REMOTE_SDK_IP, '65535', VERSION_DASHBOARD_URL)
        core = get_json_value(rsp, 'core')
        self.assertEqual(core, EXPECT_SDK_VERSION, 'dashboard is not addressable, sdk init failed')

    @func_doc
    def testInitPortOccupied(self):
        """
        testlink tc-376
        SDK端口被占用
        @owner: guzehao
        @reviewer: jinyifan
        """
        occupy_port(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD, SDK_HTTP_PORT)
        occupied = verify_port_occupancy(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD, SDK_HTTP_PORT)
        self.assertTrue(occupied, '32717 should been occupied')
        start_sdk(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD, REMOTE_SDK_PATH)
        not_occupied = verify_process_port_occupancy(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD, 'ys_service_static')
        self.assert_(not_occupied, 'ys_service_static should not occupy any port')
        release_port(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD)
        occupy_port(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD, SDK_RTMP_PORT)
        occupied = verify_port_occupancy(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD, SDK_RTMP_PORT)
        self.assertTrue(occupied, '32718 should been occupied')
        start_sdk(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD, REMOTE_SDK_PATH)
        not_occupied = verify_process_port_occupancy(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD, 'ys_service_static')
        self.assert_(not_occupied, 'ys_service_static should not occupy any port')
        release_port(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD)
        occupy_port(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD, SDK_DASHBOARD_PORT)
        occupied = verify_port_occupancy(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD, SDK_DASHBOARD_PORT)
        self.assertTrue(occupied, '32719 should been occupied')
        start_sdk(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD, REMOTE_SDK_PATH)
        not_occupied = verify_process_port_occupancy(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD, 'ys_service_static')
        self.assert_(not_occupied, 'ys_service_static should not occupy any port')
        release_port(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD)

    @func_doc
    def testInitReleasePort(self):
        """
        testlink tc-377
        SDK退出会释放端口
        @owner: guzehao
        @reviewer: jinyifan
        """
        not_occupied = verify_port_not_occupancy(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD, SDK_HTTP_PORT, SDK_RTMP_PORT,
                                             SDK_DASHBOARD_PORT)
        self.assert_(not_occupied, '32717 32718 32719 should not been occupied')
        start_sdk(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD, REMOTE_SDK_PATH)
        time.sleep(2)
        occupied = verify_port_occupancy(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD, SDK_HTTP_PORT, SDK_RTMP_PORT,
                                        SDK_DASHBOARD_PORT)
        self.assert_(occupied, 'sdk start should occupy 32717 32718 32719')
        rsp = get_sdk_dashboard(REMOTE_SDK_IP, '32719', VERSION_DASHBOARD_URL)
        core = get_json_value(rsp, 'core')
        self.assertEqual(core, EXPECT_SDK_VERSION, 'dashboard is not addressable, sdk init failed')
        stop_sdk(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD)
        time.sleep(2)
        not_occupied = verify_port_not_occupancy(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD, SDK_HTTP_PORT, SDK_RTMP_PORT,
                                             SDK_DASHBOARD_PORT)
        self.assert_(not_occupied, 'stop sdk should release 32717 32718 32719')

    @func_doc
    def testInitSpecifiedPortNumberAndString(self):
        """
        testlink tc-853
        SDK指定端口启动（数字+字符串）
        @owner: jinyfian
        """
        not_occupied = verify_port_not_occupancy(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD, SDK_HTTP_PORT, SDK_RTMP_PORT,
                                             SDK_DASHBOARD_PORT)
        self.assertTrue(not_occupied, 'port has been occupied')
        start_sdk(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD, REMOTE_SDK_PATH, '4000ab')
        time.sleep(2)
        rsp = get_sdk_dashboard(REMOTE_SDK_IP, '4000', VERSION_DASHBOARD_URL)
        core = get_json_value(rsp, 'core')
        self.assertEqual(core, EXPECT_SDK_VERSION, 'dashboard is not addressable, sdk init failed')
        stop_sdk(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD)
        start_sdk(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD, REMOTE_SDK_PATH, '4000a1')
        time.sleep(2)
        rsp = get_sdk_dashboard(REMOTE_SDK_IP, '4000', VERSION_DASHBOARD_URL)
        core = get_json_value(rsp, 'core')
        self.assertEqual(core, EXPECT_SDK_VERSION, 'dashboard is not addressable, sdk init failed')

if __name__ == '__main__':
    unittest.main()
