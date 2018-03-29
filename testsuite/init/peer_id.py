# coding=utf-8
# linux sdk init core auto testcase
import unittest
from lib.sdk.common_tool.sdk_handle import *
from lib.sdk.common_tool.specific_handle import *
from lib.sdk.common_tool.verify_handle import *
from lib.sdk.sdk_constant import *
from lib.common.decorator import *


class TestPeerId(unittest.TestCase):

    @func_doc
    def setUp(self):
        """
        上传sdk，使用ys_service_static版本
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
    def testInitPeerIdFirstStart(self):
        """
        testlink tc-21
        SDK首次启动生成peer信息文件
        @owner: guzehao
        @reviewer: jinyifan
        """
        start_sdk(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD, REMOTE_SDK_PATH)
        time.sleep(2)
        conf_text = get_sdk_conf_file(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD, REMOTE_SDK_PATH)
        conf_peer_id = get_json_value(conf_text, 'peer_id')
        response_text = get_sdk_dashboard(REMOTE_SDK_IP, SDK_PORT, CONF_DASHBOARD_URL)
        dashboard_peer_id = get_json_value(response_text, 'peer_id')
        stop_sdk(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD)
        is_legal = verify_peer_id_legal(conf_peer_id)

        print "-------------------------------------------------------------------"
        print 'peer_id of dashboard: {0}'.format(dashboard_peer_id)
        print 'peer_id of config file: {0}'.format(conf_peer_id)
        print "-------------------------------------------------------------------"

        self.assertTrue(is_legal, 'peer_id is not legal')
        self.assertEqual(conf_peer_id, dashboard_peer_id, 'peer_id of conf file is different from peer_id of dashboard')

    @func_doc
    def testInitPeerIdDelete(self):
        """
        testlink tc-382
        peer_id被删除，SDK再次启动时重新生成peer_id
        @owner: guzehao
        @reviewer: jinyifan
        """
        start_sdk(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD, REMOTE_SDK_PATH)
        time.sleep(2)
        conf_text_1 = get_sdk_conf_file(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD, REMOTE_SDK_PATH)
        conf_peer_id_1 = get_json_value(conf_text_1, 'peer_id')
        stop_sdk(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD)
        time.sleep(2)
        remove_sdk(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD, REMOTE_SDK_PATH, 'yunshang/yunshang.conf')
        start_sdk(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD, REMOTE_SDK_PATH)
        time.sleep(2)
        conf_text_2 = get_sdk_conf_file(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD, REMOTE_SDK_PATH)
        conf_peer_id_2 = get_json_value(conf_text_2, 'peer_id')
        response_text = get_sdk_dashboard(REMOTE_SDK_IP, SDK_PORT, CONF_DASHBOARD_URL)
        dashboard_peer_id = get_json_value(response_text, 'peer_id')
        stop_sdk(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD)
        is_legal_conf1 = verify_peer_id_legal(conf_peer_id_1)
        is_legal_conf2 = verify_peer_id_legal(conf_peer_id_2)
        is_legal_dashboard = verify_peer_id_legal(dashboard_peer_id)

        print "-------------------------------------------------------------------"
        print "the first time's peer_id: {0}".format(conf_peer_id_1)
        print "the second time's peer_id: {0}".format(conf_peer_id_2)
        print "the peer_id of dashboard: {0}".format(dashboard_peer_id)
        print "-------------------------------------------------------------------"

        self.assertTrue(is_legal_conf1, 'peer_id of config file is not legal')
        self.assertTrue(is_legal_conf2, 'peer_id of config file is not legal')
        self.assertTrue(is_legal_dashboard, 'peer_id of dashboard is not legal')
        self.assertNotEquals(conf_peer_id_1, conf_peer_id_2, "first time's peer id should be different from the second "
                                                             "time")
        self.assertEqual(conf_peer_id_2, dashboard_peer_id, 'peer_id of config file should be the same as peer_id of '
                                                            'dashboard')

    @func_doc
    def testInitPeerIdExist(self):
        """
        testlink tc-383
        Peer信息存在 SDK启动不重新生成
        @owner: guzehao
        @reviewer: jinyifan
        """
        start_sdk(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD, REMOTE_SDK_PATH)
        time.sleep(2)
        conf_text_1 = get_sdk_conf_file(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD, REMOTE_SDK_PATH)
        conf_peer_id_1 = get_json_value(conf_text_1, 'peer_id')
        stop_sdk(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD)
        time.sleep(2)
        start_sdk(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD, REMOTE_SDK_PATH)
        time.sleep(2)
        conf_text_2 = get_sdk_conf_file(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD, REMOTE_SDK_PATH)
        conf_peer_id_2 = get_json_value(conf_text_2, 'peer_id')
        response_text = get_sdk_dashboard(REMOTE_SDK_IP, SDK_PORT, '/ajax/conf')
        dashboard_peer_id = get_json_value(response_text, 'peer_id')
        stop_sdk(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD)
        is_legal_conf1 = verify_peer_id_legal(conf_peer_id_1)
        is_legal_conf2 = verify_peer_id_legal(conf_peer_id_2)
        is_legal_dashboard = verify_peer_id_legal(dashboard_peer_id)

        print "-------------------------------------------------------------------"
        print "the first time's peer_id: {0}".format(conf_peer_id_1)
        print "the second time's peer_id: {0}".format(conf_peer_id_2)
        print "the peer_id of dashboard: {0}".format(dashboard_peer_id)
        print "-------------------------------------------------------------------"

        self.assertTrue(is_legal_conf1, 'peer_id of config file is not legal')
        self.assertTrue(is_legal_conf2, 'peer_id of config file is not legal')
        self.assertTrue(is_legal_dashboard, 'peer_id of dashboard is not legal')
        self.assertEqual(conf_peer_id_1, conf_peer_id_2, "first time's peer id should be the same as the second time")
        self.assertEqual(dashboard_peer_id, conf_peer_id_2, 'peer_id of config file should be the same as peer_id of '
                                                            'dashboard')

    @func_doc
    def testInitPeerIdStopSDK(self):
        """
        testlink tc-385
        停止SDK，peer信息仍存在
        @owner: guzehao
        @reviewer: jinyifan
        """
        start_sdk(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD, REMOTE_SDK_PATH)
        time.sleep(2)
        conf_text_1 = get_sdk_conf_file(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD, REMOTE_SDK_PATH)
        conf_peer_id_1 = get_json_value(conf_text_1, 'peer_id')
        stop_sdk(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD)
        time.sleep(2)
        conf_text_2 = get_sdk_conf_file(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD, REMOTE_SDK_PATH)
        conf_peer_id_2 = get_json_value(conf_text_2, 'peer_id')
        is_legal_conf1 = verify_peer_id_legal(conf_peer_id_1)
        is_legal_conf2 = verify_peer_id_legal(conf_peer_id_2)

        print "-------------------------------------------------------------------"
        print "the peer_id when sdk run: {0}".format(conf_peer_id_1)
        print "the peer_id after sdk run: {0}".format(conf_peer_id_2)
        print "-------------------------------------------------------------------"

        self.assertTrue(is_legal_conf1, 'peer_id of config file is not legal')
        self.assertTrue(is_legal_conf2, 'peer_id of config file is not legal')
        self.assertEqual(conf_peer_id_1, conf_peer_id_2, 'peer_id should not change after run')

    @func_doc
    def testInitPeerIdAllZero(self):
        """
        testlink tc-389
        peer_id全0时能正常登录
        @owner: guzehao
        @reviewer: jinyifan
        """
        start_sdk(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD, REMOTE_SDK_PATH)
        time.sleep(2)
        stop_sdk(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD)
        modify_conf_file(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD, REMOTE_SDK_PATH, 'peer_id', PEER_ID_ALL_ZERO)
        start_sdk(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD, REMOTE_SDK_PATH)
        time.sleep(2)
        conf_text = get_sdk_conf_file(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD, REMOTE_SDK_PATH)
        conf_peer_id = get_json_value(conf_text, 'peer_id')
        response_text = get_sdk_dashboard(REMOTE_SDK_IP, SDK_PORT, CONF_DASHBOARD_URL)
        dashboard_peer_id = get_json_value(response_text, 'peer_id')

        print "-------------------------------------------------------------------"
        print "the peer_id when sdk run: {0}".format(conf_peer_id)
        print "the peer_id after sdk run: {0}".format(dashboard_peer_id)
        print "-------------------------------------------------------------------"

        self.assertEqual(conf_peer_id, PEER_ID_ALL_ZERO, 'peer_id of config file should be all zero')
        self.assertEqual(dashboard_peer_id, PEER_ID_ALL_ZERO, 'peer_id of dashboard should be all zero')

    @func_doc
    def testInitPeerIdEmpty(self):
        """
        testlink tc-390
        peer_id为空
        @owner: guzehao
        @reviewer: jinyifan
        """
        start_sdk(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD, REMOTE_SDK_PATH)
        time.sleep(2)
        stop_sdk(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD)
        modify_conf_file(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD, REMOTE_SDK_PATH, 'peer_id', 'null')
        start_sdk(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD, REMOTE_SDK_PATH)
        time.sleep(2)
        conf_text = get_sdk_conf_file(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD, REMOTE_SDK_PATH)
        conf_peer_id = get_json_value(conf_text, 'peer_id')
        response_text = get_sdk_dashboard(REMOTE_SDK_IP, SDK_PORT, CONF_DASHBOARD_URL)
        dashboard_peer_id = get_json_value(response_text, 'peer_id')
        stop_sdk(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD)
        is_legal_conf1 = verify_peer_id_legal(conf_peer_id)
        is_legal_conf2 = verify_peer_id_legal(dashboard_peer_id)

        print "-------------------------------------------------------------------"
        print "peer_id of config file: {0}".format(conf_peer_id)
        print "peer_id of dashboard: {0}".format(dashboard_peer_id)
        print "-------------------------------------------------------------------"

        self.assertTrue(is_legal_conf1, 'peer_id of config file is not legal')
        self.assertTrue(is_legal_conf2, 'peer_id of dashboard is not legal')
        self.assertEqual(conf_peer_id, dashboard_peer_id, 'peer_id of config file and peer_id of dashboard should be '
                                                          'equal')

    @func_doc
    def testInitPeerEmptyString(self):
        """
        testlink tc-391
        peer_id为空字符串
        @owner: guzehao
        """
        start_sdk(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD, REMOTE_SDK_PATH)
        time.sleep(2)
        stop_sdk(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD)
        modify_conf_file(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD, REMOTE_SDK_PATH, 'peer_id', '')
        start_sdk(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD, REMOTE_SDK_PATH)
        time.sleep(2)
        conf_text = get_sdk_conf_file(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD, REMOTE_SDK_PATH)
        conf_peer_id = get_json_value(conf_text, 'peer_id')
        response_text = get_sdk_dashboard(REMOTE_SDK_IP, SDK_PORT, CONF_DASHBOARD_URL)
        dashboard_peer_id = get_json_value(response_text, 'peer_id')
        stop_sdk(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD)
        is_legal_conf1 = verify_peer_id_legal(conf_peer_id)
        is_legal_conf2 = verify_peer_id_legal(dashboard_peer_id)

        print "-------------------------------------------------------------------"
        print "peer_id of config file: {0}".format(conf_peer_id)
        print "peer_id of dashboard: {0}".format(dashboard_peer_id)
        print "-------------------------------------------------------------------"

        self.assertTrue(is_legal_conf1, 'peer_id of config file is not legal')
        self.assertTrue(is_legal_conf2, 'peer_id of dashboard is not legal')
        self.assertEqual(conf_peer_id, dashboard_peer_id, 'peer_id of config file and peer_id of dashboard should be '
                                                          'equal')

    @func_doc
    def testPeerIdFieldMiss(self):
        """
        testlink tc-392
        peer_id字段缺失
        owner: guzehao
        @reviewer: jinyifan
        """
        start_sdk(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD, REMOTE_SDK_PATH)
        time.sleep(2)
        stop_sdk(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD)
        modify_conf_file(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD, REMOTE_SDK_PATH, 'peer_id', 'delete field')
        start_sdk(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD, REMOTE_SDK_PATH)
        time.sleep(2)
        conf_text = get_sdk_conf_file(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD, REMOTE_SDK_PATH)
        conf_peer_id = get_json_value(conf_text, 'peer_id')
        response_text = get_sdk_dashboard(REMOTE_SDK_IP, SDK_PORT, CONF_DASHBOARD_URL)
        dashboard_peer_id = get_json_value(response_text, 'peer_id')
        stop_sdk(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD)
        is_legal_conf1 = verify_peer_id_legal(conf_peer_id)
        is_legal_conf2 = verify_peer_id_legal(dashboard_peer_id)

        print "-------------------------------------------------------------------"
        print "peer_id of config file: {0}".format(conf_peer_id)
        print "peer_id of dashboard: {0}".format(dashboard_peer_id)
        print "-------------------------------------------------------------------"

        self.assertTrue(is_legal_conf1, 'peer_id of config file is not legal')
        self.assertTrue(is_legal_conf2, 'peer_id of dashboard is not legal')
        self.assertEqual(conf_peer_id, dashboard_peer_id, 'peer_id of config file and peer_id of dashboard should be '
                                                          'equal')

    @func_doc
    def testInitPeerIdMoreThan32Bits(self):
        """
        testlink tc-393
        peer_id超过32位
        @owner: guzehao
        @reviewer: jinyifan
        """
        start_sdk(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD, REMOTE_SDK_PATH)
        time.sleep(2)
        stop_sdk(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD)
        modify_conf_file(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD, REMOTE_SDK_PATH, 'peer_id', PEER_ID_MORE_THAN_32BITS)
        start_sdk(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD, REMOTE_SDK_PATH)
        conf_text = get_sdk_conf_file(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD, REMOTE_SDK_PATH)
        conf_peer_id = get_json_value(conf_text, 'peer_id')
        response_text = get_sdk_dashboard(REMOTE_SDK_IP, SDK_PORT, CONF_DASHBOARD_URL)
        dashboard_peer_id = get_json_value(response_text, 'peer_id')
        stop_sdk(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD)
        is_legal_conf = verify_peer_id_legal(dashboard_peer_id)

        print "-------------------------------------------------------------------"
        print "peer_id of config file: {0}".format(conf_peer_id)
        print "peer_id of dashboard: {0}".format(dashboard_peer_id)
        print "-------------------------------------------------------------------"

        self.assertTrue(is_legal_conf, 'peer_id of dashboard is not legal')
        self.assertEqual(conf_peer_id, PEER_ID_MORE_THAN_32BITS, 'peer_id of config file should be the same')
        self.assertEqual(dashboard_peer_id, PEER_ID_MORE_THAN_32BITS[:32], 'peer_id of config file should be same as top 32 of'
                                                                            ' PEER_ID_MORE_THAN_32BITS')

    @func_doc
    def testInitPeerIdLessThen32Bits(self):
        """
        testlink tc-395
        peer_id小于32位
        @owner: guzehao
        @reviewer: jinyifan
        """
        start_sdk(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD, REMOTE_SDK_PATH)
        time.sleep(2)
        stop_sdk(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD)
        modify_conf_file(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD, REMOTE_SDK_PATH, 'peer_id', PEER_ID_LESS_THAN_32_BITS)
        start_sdk(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD, REMOTE_SDK_PATH)
        time.sleep(2)
        conf_text = get_sdk_conf_file(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD, REMOTE_SDK_PATH)
        conf_peer_id = get_json_value(conf_text, 'peer_id')
        response_text = get_sdk_dashboard(REMOTE_SDK_IP, SDK_PORT, CONF_DASHBOARD_URL)
        dashboard_peer_id = get_json_value(response_text, 'peer_id')
        stop_sdk(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD)
        is_legal_conf1 = verify_peer_id_legal(conf_peer_id)
        is_legal_conf2 = verify_peer_id_legal(dashboard_peer_id)

        print "-------------------------------------------------------------------"
        print "peer_id of config file: {0}".format(conf_peer_id)
        print "peer_id of dashboard: {0}".format(dashboard_peer_id)
        print "-------------------------------------------------------------------"

        self.assertTrue(is_legal_conf1, 'peer_id of config file is not legal')
        self.assertTrue(is_legal_conf2, 'peer_id of dashboard is not legal')
        self.assertNotEquals(conf_peer_id, PEER_ID_LESS_THAN_32_BITS, 'peer_id should rebuild')
        self.assertEqual(conf_peer_id, dashboard_peer_id, 'peer_id of config file should be same as peer_id of '
                                                          'dashboard')

    @func_doc
    def testInitPeerIdNotHexadecimalString(self):
        """
        testlink tc-396
        peer_id为非16进制字符串
        @owner: guzehao
        @reviewer: jinyifan
        """
        start_sdk(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD, REMOTE_SDK_PATH)
        time.sleep(2)
        stop_sdk(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD)
        modify_conf_file(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD, REMOTE_SDK_PATH, 'peer_id', PEER_ID_NOT_HEX_STRING)
        start_sdk(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD, REMOTE_SDK_PATH)
        time.sleep(2)
        conf_text = get_sdk_conf_file(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD, REMOTE_SDK_PATH)
        conf_peer_id = get_json_value(conf_text, 'peer_id')
        response_text = get_sdk_dashboard(REMOTE_SDK_IP, SDK_PORT, CONF_DASHBOARD_URL)
        dashboard_peer_id = get_json_value(response_text, 'peer_id')
        stop_sdk(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD)
        is_legal_conf1 = verify_peer_id_legal(conf_peer_id)
        is_legal_conf2 = verify_peer_id_legal(dashboard_peer_id)

        print "-------------------------------------------------------------------"
        print "peer_id of config file: {0}".format(conf_peer_id)
        print "peer_id of dashboard: {0}".format(dashboard_peer_id)
        print "-------------------------------------------------------------------"

        self.assertTrue(is_legal_conf1, 'peer_id of config file is not legal')
        self.assertTrue(is_legal_conf2, 'peer_id of dashboard is not legal')
        self.assertNotEquals(conf_peer_id, PEER_ID_NOT_HEX_STRING, 'peer_id should rebuild')
        self.assertEqual(conf_peer_id, dashboard_peer_id, 'peer_id of config file should be same as peer_id of '
                                                          'dashboard')

    @func_doc
    def testInitPeerIdSpecifyUserPerfix(self):
        """
        testlink tc-397
        peer_id指定user perfix(前八位)
        @owner: guzehao
        @reviewer: jinyifan
        """
        start_sdk(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD, REMOTE_SDK_PATH)
        time.sleep(2)
        stop_sdk(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD)
        conf_text1 = get_sdk_conf_file(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD, REMOTE_SDK_PATH)
        conf_peer_id_1 = get_json_value(conf_text1, 'peer_id')
        remove_sdk(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD, REMOTE_SDK_PATH, 'yunshang/yunshang.conf')
        start_sdk(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD, REMOTE_SDK_PATH, user_prefix=USER_PREFIX)
        time.sleep(2)
        conf_text2 = get_sdk_conf_file(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD, REMOTE_SDK_PATH)
        conf_peer_id_2 = get_json_value(conf_text2, 'peer_id')
        user_prefix_2 = get_json_value(conf_text2, 'peer_id', '8')
        response_text = get_sdk_dashboard(REMOTE_SDK_IP, SDK_PORT, CONF_DASHBOARD_URL)
        dashboard_peer_id = get_json_value(response_text, 'peer_id')
        stop_sdk(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD)
        is_legal_conf1 = verify_peer_id_legal(conf_peer_id_1)
        is_legal_conf2 = verify_peer_id_legal(conf_peer_id_2)
        is_legal_dashboard = verify_peer_id_legal(dashboard_peer_id)

        print "-------------------------------------------------------------------"
        print 'peer_id of config file first time: {0}'.format(conf_peer_id_1)
        print 'peer_id of config file second time: {0}'.format(conf_peer_id_2)
        print 'peer_id of dashboard: {0}'.format(dashboard_peer_id)
        print "-------------------------------------------------------------------"

        self.assertTrue(is_legal_conf1, 'peer_id is not legal')
        self.assertTrue(is_legal_conf2, 'peer_id is not legal')
        self.assertTrue(is_legal_dashboard, 'peer_id is not legal')
        self.assertEqual(user_prefix_2, USER_PREFIX, 'prefix should be same as assign')
        self.assertNotEqual(conf_peer_id_1, conf_peer_id_2, "first time's peer id should be same as the second time")
        self.assertEqual(conf_peer_id_2, dashboard_peer_id, 'peer_id of config file and peer_id of dashboard should be '
                                                            'equal')


if __name__ == '__main__':
        unittest.main()