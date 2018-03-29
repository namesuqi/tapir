# coding=utf-8
# author: zengyuetian
#

from lib.ios.test_base import *


class TestInit(TestBase):

    @func_doc
    def test_app_login(self):
        """
        apk初始化测试用例
        """
        login_btns = self.app.driver.find_elements_by_class_name('UIAButton')
        print DEBUG_STRING, login_btns

        login = self.app.driver.find_element_by_xpath('//UIAApplication[1]/UIAWindow[1]/UIAButton[1]')
        login.click()
        time.sleep(10)


if __name__ == "__main__":
    unittest.main()
    # suite = unittest.TestSuite()
    # suite.addTest(TestInit("test_put_background"))
    #
    # unittest.TextTestRunner().run(suite)

