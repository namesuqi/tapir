# coding=utf-8
# author: zengyuetian

import unittest
from lib.android.test_base import *
from lib.android.logcater import *
from lib.android.sdk import *


class InitCore2(TestBase):

    def setUp(self):
        print "Test Start ...."
        logcat_clear(ANDROID_DEVICE)
        self.app = Application()
        self.app.initialize(ANDROID_DEVICE, ANDROID_PLATFORM, ANDROID_VERSION,
                            DEMO_APK, DEMO_PACKAGE_NAME, DEMO_ACTIVITY_NAME)

    def tearDown(self):
        print "Test End ..."

    @func_doc
    def testInitCoreMiss(self):
        """
        sdk init core
        @testlink: tc-361
        @owner: zengyuetian
        """
        # reinstall and remove core files
        self.app.driver.remove_app(DEMO_PACKAGE_NAME)
        self.app.driver.install_app(DEMO_APK)
        self.app.restart(ANDROID_DEVICE, ANDROID_PLATFORM, ANDROID_VERSION,
                         DEMO_APK, DEMO_PACKAGE_NAME, DEMO_ACTIVITY_NAME)
        remove_file(ANDROID_DEVICE, "/data/data/com.cloutropy.bplayer/files/libys-core.so.{0}".format(SDK_VERION))
        remove_file(ANDROID_DEVICE, "/data/data/com.cloutropy.bplayer/files/libys-core.so.{0}.md5".format(SDK_VERION))
        remove_file(ANDROID_DEVICE, "/data/data/com.cloutropy.bplayer/lib/libys-core.{0}.so".format(SDK_VERION))

        # clear log
        logcat_clear(ANDROID_DEVICE)
        self.app.restart(ANDROID_DEVICE, ANDROID_PLATFORM, ANDROID_VERSION,
                         DEMO_APK, DEMO_PACKAGE_NAME, DEMO_ACTIVITY_NAME)

        # find init successfully string via logcat, expect not found
        lines = logcat_filter(ANDROID_DEVICE, "ysboot")
        print lines
        p2p_core_init_successfully = False
        for line in lines:
            if line.find("p2p_core_init successfully") >= 0:
                p2p_core_init_successfully = True
                print(line)
        self.assertFalse(p2p_core_init_successfully)

        # check login status
        login = get_login(ANDROID_HOST, SDK_PORT)
        print login.text
        self.failIf(login.text, "SDK should not be login without core")













if __name__ == "__main__":
    # unittest.main()
    suite = unittest.TestSuite()
    suite.addTest(InitCore2("testInitCoreMiss"))
    runner = unittest.TextTestRunner()
    runner.run(suite)