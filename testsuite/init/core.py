# coding=utf-8
# author: guzehao
# linux SDK init core auto testcase
import unittest
from lib.sdk.common_tool.sdk_handle import *
from lib.sdk.common_tool.specific_handle import *
from lib.sdk.common_tool.verify_handle import *
from lib.sdk.sdk_constant import *
from lib.common.decorator import *


class TestCore(unittest.TestCase):

    @func_doc
    def setUp(self):
        """
        上传sdk
        """
        remove_sdk(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD, REMOTE_SDK_PATH)
        upload_full_sdk(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD, REMOTE_SDK_PATH)

    @func_doc
    def tearDown(self):
        """
        移除sdk
        """
        remove_sdk(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD, REMOTE_SDK_PATH)

    @func_doc
    def testInitCoreRight(self):
        """
        testlink tc-399

        @owner: guzehao
        @reviewer: jinyifan
        """
        start_sdk_ys_service(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD, REMOTE_SDK_PATH, save_log=True)
        time.sleep(5)

        rsp = get_sdk_dashboard(REMOTE_SDK_IP, SDK_PORT, VERSION_DASHBOARD_URL)
        core = get_json_value(rsp, 'core')
        stop_sdk_kill_all(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD)
        time.sleep(2)

        version = get_sdk_version_by_run_log(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD, REMOTE_SDK_PATH)

        print 'dashboard version: {0}'.format(core)
        print 'run log version: {0}'.format(version)

        self.assertEqual(core, EXPECT_SDK_VERSION, 'version of dashboard wrong')
        self.assertEqual(version, EXPECT_SDK_VERSION, 'version of sdk run log wrong')

    @func_doc
    def testInitCoreMiss(self):
        """
        testlink tc-361
        @owner: guzehao
        @reviewer: jinyifan
        """
        remove_sdk(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD, REMOTE_SDK_PATH, '*core*')

        start_sdk_ys_service(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD, REMOTE_SDK_PATH, save_log=True)
        time.sleep(5)

        response_text = get_sdk_dashboard(REMOTE_SDK_IP, SDK_PORT, LOGIN_DASHBOARD_URL)

        stop_sdk_kill_all(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD)

        print 'dashboard content: {0}'.format(response_text)

        self.failIf(response_text, 'dashboard should not be addressable')

    @func_doc
    def testInitCoreReplaceByOtherFile(self):
        """
        testlink tc-360
        @owner: guzehao
        @reviewer: zengyuetian
        """
        replace_core_so_by_other_file(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD, REMOTE_SDK_PATH)

        start_sdk_ys_service(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD, REMOTE_SDK_PATH, save_log=True)
        time.sleep(5)

        response_text = get_sdk_dashboard(REMOTE_SDK_IP, SDK_PORT, LOGIN_DASHBOARD_URL)

        stop_sdk_kill_all(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD)

        print 'dashboard content: {0}'.format(response_text)

        self.failIf(response_text, 'dashboard should not be addressable')

    @func_doc
    def testCoreChangeFile(self):
        """
        testlink tc-398
        @owner: guzehao
        @reviewer: zengyuetian
        """
        modify_core_so_file(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD, REMOTE_SDK_PATH)

        start_sdk_ys_service(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD, REMOTE_SDK_PATH, save_log=True)
        time.sleep(5)

        response_text = get_sdk_dashboard(REMOTE_SDK_IP, SDK_PORT, LOGIN_DASHBOARD_URL)

        stop_sdk_kill_all(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD)
        print 'dashboard content: {0}'.format(response_text)

        self.failIf(response_text, 'dashboard should not be addressable')

    @func_doc
    def testCoreDelete(self):
        """
        testlink tc-400
        @owner: guzehao
        @reviewer: zengyuetian
        """
        start_sdk_ys_service(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD, REMOTE_SDK_PATH, save_log=True)
        remove_sdk(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD, REMOTE_SDK_PATH, '*core.so*')
        time.sleep(1)
        response_text = get_sdk_dashboard(REMOTE_SDK_IP, SDK_PORT, VERSION_DASHBOARD_URL)
        core = get_json_value(response_text, 'core')
        stop_sdk_kill_all(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD)
        time.sleep(2)
        version = get_sdk_version_by_run_log(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD, REMOTE_SDK_PATH)

        print 'version of dashboard: {0}'.format(core)
        print 'version of sdk run log: {0}'.format(version)

        self.assertEqual(core, EXPECT_SDK_VERSION, 'version of dashboard should be correct')
        self.assertEqual(version, EXPECT_SDK_VERSION, 'version of sdk run log should be correct')

    @func_doc
    def testInitCoreMultiFile(self):
        """
        testlink tc-401
        @owner: guzehao
        @reviewer: zengyuetian
        """
        upload_old_version_sdk(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD, REMOTE_SDK_PATH)
        max_version = get_max_core_version(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD, REMOTE_SDK_PATH)
        start_sdk_ys_service(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD, REMOTE_SDK_PATH, save_log=True)
        is_exist = verify_file_is_exist(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD, REMOTE_SDK_PATH, 'core.so|grep -v md5')
        response_text = get_sdk_dashboard(REMOTE_SDK_IP, SDK_PORT, VERSION_DASHBOARD_URL)
        stop_sdk_kill_all(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD)
        core = get_json_value(response_text, 'core')

        print 'max core version: {0}'.format(max_version)
        print 'version of dashboard: {0}'.format(core)

        self.assertEqual(core, EXPECT_SDK_VERSION, 'version of dashboard should be correct')
        self.assertEqual(max_version, EXPECT_SDK_VERSION, 'max core version should be correct')
        self.assert_(is_exist, 'core.so should be exist')

    @func_doc
    def testInitCoreNoMd5File(self):
        """
        testlink tc-402
        @owner: guzehao
        @reviewer: zengyuetian
        """
        start_sdk_ys_service(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD, REMOTE_SDK_PATH, save_log=True)
        time.sleep(2)
        stop_sdk_kill_all(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD)
        time.sleep(2)
        remove_sdk(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD, REMOTE_SDK_PATH, '/yunshang/*md5')
        start_sdk_ys_service(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD, REMOTE_SDK_PATH, save_log=True)
        time.sleep(1)
        response_text = get_sdk_dashboard(REMOTE_SDK_IP, SDK_PORT, VERSION_DASHBOARD_URL)
        time.sleep(1)
        is_exist = verify_file_is_exist(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD, REMOTE_SDK_PATH, 'core.so|grep -v md5',
                                        '\'md5$\'')
        stop_sdk_kill_all(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD)

        print "MD5 exists: ", is_exist
        print "Response is: ", response_text

        self.failIf(is_exist, 'md5 file should be exist')
        self.failIf(response_text, 'dashboard should not be addressable')


if __name__ == '__main__':
    unittest.main()
    # suite = unittest.TestSuite()
    # suite.addTest(TestCore("testInitCoreReplaceByOtherFile"))
    # runner = unittest.TextTestRunner()
    # runner.run(suite)

