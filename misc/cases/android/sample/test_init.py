# coding=utf-8
# author: zengyuetian
#

from lib.android.test_base import *


class TestInit(TestBase):

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
    def test_apk_init(self):
        """
        apk初始化测试用例
        """
        activity = self.app.driver.current_activity
        self.assertEquals('.MainActivity', activity)

    @func_doc
    def test_get_sdk_version(self):
        """
        get version info of sdk
        """
        data = get_version(ANDROID_HOST, SDK_PORT)
        version = get_response_data_by_path(data, "/core")
        print version

    @func_doc
    def test_put_background(self):
        """
        put app to background
        """
        el = self.app.driver.find_element_by_name('livestream live_flv')
        print "****", el
        self.assertIsNotNone(el)
        self.app.driver.background_app(1)
        time.sleep(2)
        el = self.app.driver.find_element_by_name('livestream live_flv')
        print "****", el
        self.assertIsNotNone(el)


if __name__ == "__main__":
    unittest.main()
    # suite = unittest.TestSuite()
    # suite.addTest(TestInit("test_put_background"))
    #
    # unittest.TextTestRunner().run(suite)

