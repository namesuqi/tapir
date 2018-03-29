# coding=utf-8
# author: zengyuetian
# test case for installation

from lib.android.test_base import *


class TestInstall(TestBase):
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
    def testInstall(self):
        """
        apk安装测试
        验证apk可以被正确的安装
        """
        print DEBUG_STRING, self.app.driver.is_app_installed('asdkf1111')
        demo_installed = self.app.driver.is_app_installed(DEMO_PACKAGE_NAME)
        print DEBUG_STRING, demo_installed
        self.assertTrue(demo_installed)

        self.app.driver.install_app(DEMO_APK)
        demo_installed = self.app.driver.is_app_installed(DEMO_PACKAGE_NAME)
        print DEBUG_STRING, demo_installed
        self.assertTrue(demo_installed)

    @func_doc
    def testUninstall(self):
        """
        apk卸载测试
        验证apk可以被正确的安装
        """
        self.app.driver.remove_app(DEMO_PACKAGE_NAME)
        demo_installed = self.app.driver.is_app_installed(DEMO_PACKAGE_NAME)
        print DEBUG_STRING, demo_installed
        self.assertFalse(demo_installed)

        self.app.driver.install_app(DEMO_APK)
        demo_installed = self.app.driver.is_app_installed(DEMO_PACKAGE_NAME)
        print DEBUG_STRING, demo_installed
        self.assertTrue(demo_installed)

        self.app.driver.remove_app(DEMO_PACKAGE_NAME)
        demo_installed = self.app.driver.is_app_installed(DEMO_PACKAGE_NAME)
        print DEBUG_STRING, demo_installed
        self.assertFalse(demo_installed)


if __name__ == "__main__":
    # unittest.main()
    suite = unittest.TestSuite()
    suite.addTest(TestInstall("testInstall"))
    unittest.TextTestRunner().run(suite)


