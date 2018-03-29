# coding=utf-8
# author: zengyuetian

import unittest
from lib.android.test_base import *
from lib.android.logcater import *
from lib.android.sdk import *


class InitCore1(TestBase):

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
    def testInitCoreRight(self):
        """
        sdk init core
        @testlink: tc-399
        @owner: zengyuetian
        @reviewer: jinyifan
        """
        # find init successfully string via logcat
        lines = logcat_filter(ANDROID_DEVICE, "ysboot")
        p2p_core_init_successfully = False
        for line in lines:
            if line.find("p2p_core_init successfully") >= 0:
                p2p_core_init_successfully = True
                print(line)
        self.assertTrue(p2p_core_init_successfully)

        # check dashboard
        data = get_version(ANDROID_HOST, SDK_PORT)
        version = get_response_data_by_path(data, "/core")
        print version
        self.assertEqual(version, SDK_VERION)


if __name__ == "__main__":
    # unittest.main()
    suite = unittest.TestSuite()
    suite.addTest(InitCore1("testInitCoreRight"))
    runner = unittest.TextTestRunner()
    runner.run(suite)