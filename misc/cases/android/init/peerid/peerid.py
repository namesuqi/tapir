# coding=utf-8
# author: zengyuetian

import unittest
from lib.android.test_base import *
from lib.android.logcater import *
from lib.android.sdk import *
from lib.sdk.sdk_info import *


class PeerID(TestBase):

    def setUp(self):
        print "Test Start ...."
        logcat_clear(ANDROID_DEVICE)
        self.app = Application()
        self.app.initialize(ANDROID_DEVICE, ANDROID_PLATFORM, ANDROID_VERSION,
                                               DEMO_APK, DEMO_PACKAGE_NAME, DEMO_ACTIVITY_NAME)

    def tearDown(self):
        print "Test End ..."
        self.app.quit()

    @func_doc
    def testPeerIdFirstStart(self):
        """
        sdk create peer id file at first start
        @testlink: tc-21
        @owner: zengyuetian
        """
        # re-install app to make dir clean
        self.app.driver.remove_app(DEMO_PACKAGE_NAME)
        self.app.driver.install_app(DEMO_APK)
        self.app.restart(ANDROID_DEVICE, ANDROID_PLATFORM, ANDROID_VERSION,
                         DEMO_APK, DEMO_PACKAGE_NAME, DEMO_ACTIVITY_NAME)

        # check peer id
        peer_id_1 = get_peer_id_via_file(ANDROID_DEVICE)
        print peer_id_1
        self.assertEqual(len(peer_id_1), PEER_ID_LENGTH, "peer id length should be 32")
        self.assertTrue(is_hex_string(peer_id_1), "peer id should be hex string")

        # get peer id from dashboard
        peer_id_2 = get_peer_id_via_url(ANDROID_HOST, SDK_PORT)
        print peer_id_2
        self.assertEqual(peer_id_1, peer_id_2, "peer id 1 and 2 should be equal")

    @func_doc
    def testPeerIdDelete(self):
        """
        sdk re-create peer id file
        @testlink: tc-382
        @owner: zengyuetian
        """
        # check peer id
        peer_id_1 = get_peer_id_via_file(ANDROID_DEVICE)
        print peer_id_1

        # delete yunshang.conf
        delete_peer_id_file(ANDROID_DEVICE)

        # restart sdk
        self.app.restart(ANDROID_DEVICE, ANDROID_PLATFORM, ANDROID_VERSION,
                         DEMO_APK, DEMO_PACKAGE_NAME, DEMO_ACTIVITY_NAME)

        # get peer id
        peer_id_2 = get_peer_id_via_file(ANDROID_DEVICE)
        print peer_id_2
        self.assertNotEqual(peer_id_1, peer_id_2, "peer id 1 and 2 should not be equal")

    @func_doc
    def testPeerIdExist(self):
        """
        sdk not re-create peer id if it exists
        @testlink: tc-383
        @owner: zengyuetian
        """
        # check peer id
        peer_id_1 = get_peer_id_via_file(ANDROID_DEVICE)
        print "PEER ID in conf file:", peer_id_1

        # restart sdk
        self.app.restart(ANDROID_DEVICE, ANDROID_PLATFORM, ANDROID_VERSION,
                         DEMO_APK, DEMO_PACKAGE_NAME, DEMO_ACTIVITY_NAME)

        # get peer id
        peer_id_2 = get_peer_id_via_file(ANDROID_DEVICE)
        print "PEER ID in conf file:", peer_id_2
        self.assertEqual(peer_id_1, peer_id_2, "peer id 1 and 2 should be equal")

        # get peer id from dashboard
        peer_id_3 = get_peer_id_via_url(ANDROID_HOST, SDK_PORT)
        print "PEER ID in dashboard:", peer_id_3
        self.assertEqual(peer_id_1, peer_id_3, "peer id 1 and 3 should be equal")

    @func_doc
    def testPeerIdStopSDK(self):
        """
        sdk not re-create peer id if it exists
        @testlink: tc-385
        @owner: zengyuetian
        """
        # check peer id
        peer_id_1 = get_peer_id_via_file(ANDROID_DEVICE)
        print "PEER ID in conf file:", peer_id_1

        # quit app
        self.app.driver.close_app()

        # get peer id
        peer_id_2 = get_peer_id_via_file(ANDROID_DEVICE)
        print "PEER ID in conf file:", peer_id_2
        self.assertEqual(peer_id_1, peer_id_2, "peer id 1 and 2 should be equal")

    @func_doc
    def testPeerIdAllZero(self):
        """
        sdk could be start if peer id is all 0
        @testlink: tc-389
        @owner: zengyuetian
        """
        zero_peer_id = "0" * 32
        # create peer id
        content = '{"peer_id": "00000000000000000000000000000000","disk_quota": 100}'
        # modify_peer_id(ANDROID_DEVICE, zero_peer_id)
        modify_peer_id(ANDROID_DEVICE, content)

        # check peer id
        peer_id_1 = get_peer_id_via_file(ANDROID_DEVICE)
        print "PEER ID in conf file:", peer_id_1
        self.assertEqual(peer_id_1, zero_peer_id, "peer id should be equal")

        self.app.close()
        self.app.launch()

        # check peer id
        peer_id_2 = get_peer_id_via_file(ANDROID_DEVICE)
        print "PEER ID in conf file:", peer_id_2
        self.assertEqual(peer_id_2, zero_peer_id, "peer id should be equal")

        # get peer id
        peer_id_3 = get_peer_id_via_url(ANDROID_HOST, SDK_PORT)
        print "PEER ID in dashboard:", peer_id_3
        self.assertEqual(peer_id_3, zero_peer_id, "peer id should be equal")

    @func_doc
    def testPeerIdEmpty(self):
        """
        sdk create peer id if it is empty
        @testlink: tc-390
        @owner: zengyuetian
        """
        # empty_peer_id = None
        content = '{"peer_id": ,"disk_quota": 100}'
        self.app.close()

        # create peer id
        conf_content = modify_peer_id(ANDROID_DEVICE, content)
        print conf_content

        self.app.launch()

        # check peer id
        peer_id_1 = get_peer_id_via_file(ANDROID_DEVICE)
        print "PEER ID in conf file:", peer_id_1
        self.assertEqual(len(peer_id_1), PEER_ID_LENGTH, "peer id length should be 32")
        self.assertTrue(is_hex_string(peer_id_1), "peer id should be hex string")

        # get peer id
        peer_id_2 = get_peer_id_via_url(ANDROID_HOST, SDK_PORT)
        print "PEER ID in dashboard:", peer_id_2
        self.assertEqual(peer_id_1, peer_id_2, "peer id should be equal")

    @func_doc
    def testPeerIdEmptyString(self):
        """
        sdk create peer id if it is empty
        @testlink: tc-391
        @owner: zengyuetian
        """
        content = '{"peer_id": "","disk_quota": 100}'
        self.app.close()

        # create peer id
        conf_content = modify_peer_id(ANDROID_DEVICE, content)
        print conf_content

        self.app.launch()

        # check peer id
        peer_id_1 = get_peer_id_via_file(ANDROID_DEVICE)
        print "PEER ID in conf file:", peer_id_1
        self.assertEqual(len(peer_id_1), PEER_ID_LENGTH, "peer id length should be 32")
        self.assertTrue(is_hex_string(peer_id_1), "peer id should be hex string")

        # get peer id
        peer_id_2 = get_peer_id_via_url(ANDROID_HOST, SDK_PORT)
        print "PEER ID in dashboard:", peer_id_2
        self.assertEqual(peer_id_1, peer_id_2, "peer id should be equal")

    @func_doc
    def testPeerIdFieldMiss(self):
        """
        sdk create peer id if it is miss
        @testlink: tc-392
        @owner: zengyuetian
        """
        content = '{"disk_quota": 100}'
        self.app.close()

        # create peer id
        conf_content = modify_peer_id(ANDROID_DEVICE, content)
        print conf_content

        self.app.launch()

        # check peer id
        peer_id_1 = get_peer_id_via_file(ANDROID_DEVICE)
        print "PEER ID in conf file:", peer_id_1
        self.assertEqual(len(peer_id_1), PEER_ID_LENGTH, "peer id length should be 32")
        self.assertTrue(is_hex_string(peer_id_1), "peer id should be hex string")

        # get peer id
        peer_id_2 = get_peer_id_via_url(ANDROID_HOST, SDK_PORT)
        print "PEER ID in dashboard:", peer_id_2
        self.assertEqual(peer_id_1, peer_id_2, "peer id should be equal")

    @func_doc
    def testPeerIdMoreThan32Bits(self):
        """
        sdk peer id length more than 32
        @testlink: tc-393
        @owner: zengyuetian
        """
        peer_id = "123456789012345678901234567890123456"
        content = '{"peer_id": "123456789012345678901234567890123456","disk_quota": 100}'
        self.app.close()

        # create peer id
        conf_content = modify_peer_id(ANDROID_DEVICE, content)
        print conf_content

        self.app.launch()

        # check peer id
        peer_id_1 = get_peer_id_via_file(ANDROID_DEVICE)
        print "PEER ID in conf file:", peer_id_1
        self.assertEqual(peer_id_1, peer_id, "peer id should be equal")

        # get peer id
        peer_id_2 = get_peer_id_via_url(ANDROID_HOST, SDK_PORT)
        print "PEER ID in dashboard:", peer_id_2
        self.assertEqual(peer_id_1[:32], peer_id_2, "peer id should be equal")

    @func_doc
    def testPeerIdLessThan32Bits(self):
        """
        sdk peer id length less than 32
        @testlink: tc-395
        @owner: zengyuetian
        """
        peer_id = "123456789012345678901234567890"
        content = '{"peer_id": "123456789012345678901234567890","disk_quota": 100}'
        self.app.close()

        # create peer id
        conf_content = modify_peer_id(ANDROID_DEVICE, content)
        print conf_content

        self.app.launch()

        # check peer id
        peer_id_1 = get_peer_id_via_file(ANDROID_DEVICE)
        print "PEER ID in conf file:", peer_id_1
        self.assertNotEqual(peer_id_1, peer_id, "peer id should not be equal")
        self.assertEqual(len(peer_id_1), PEER_ID_LENGTH, "peer id length should be 32")
        self.assertTrue(is_hex_string(peer_id_1), "peer id should be hex string")

        # get peer id
        peer_id_2 = get_peer_id_via_url(ANDROID_HOST, SDK_PORT)
        print "PEER ID in dashboard:", peer_id_2
        self.assertEqual(peer_id_1, peer_id_2, "peer id should be equal")

    @func_doc
    def testPeerIdNotHexadecimalString(self):
        """
        sdk peer id is not hex string
        @testlink: tc-396
        @owner: zengyuetian
        """
        content = '{"peer_id": "123456789012345678901234567890E!","disk_quota": 100}'
        self.app.close()

        # create peer id
        conf_content = modify_peer_id(ANDROID_DEVICE, content)
        print conf_content

        self.app.launch()

        # check peer id
        peer_id_1 = get_peer_id_via_file(ANDROID_DEVICE)
        print "PEER ID in conf file:", peer_id_1
        self.assertEqual(len(peer_id_1), PEER_ID_LENGTH, "peer id length should be 32")
        self.assertTrue(is_hex_string(peer_id_1), "peer id should be hex string")

        # get peer id
        peer_id_2 = get_peer_id_via_url(ANDROID_HOST, SDK_PORT)
        print "PEER ID in dashboard:", peer_id_2
        self.assertEqual(peer_id_1, peer_id_2, "peer id should be equal")


if __name__ == "__main__":
    # unittest.main()
    suite = unittest.TestSuite()
    suite.addTest(PeerID("testPeerIdNotHexadecimalString"))
    runner = unittest.TextTestRunner()
    runner.run(suite)