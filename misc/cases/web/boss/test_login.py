# coding=utf-8
# author: zengyuetian

import unittest
import time
from lib.web.boss.login_page import *
from lib.web.boss.summary_page import *
from lib.web.boss.const import *
from lib.common.HTMLTestRunner import HTMLTestRunner
from lib.common.path import *
from lib.driver import chrome_driver


class TestLogin(unittest.TestCase):
    def setUp(self):
        # global chrome_driver
        print "Test Start ...."
        opt = webdriver.ChromeOptions()
        opt.add_argument("test-type")
        self.chrome_driver = webdriver.Chrome(chrome_options=opt)
        self.chrome_driver.implicitly_wait(10)
        self.chrome_driver.maximize_window()

    def tearDown(self):
        print "Test End ..."
        self.chrome_driver.close()

    def test_login(self):
        login_page = LoginPage(self.chrome_driver)
        login_page.open()
        login_page.input_user_name(WASU_USER)
        login_page.input_password(WASU_PASSWORD)
        login_page.submit()
        time.sleep(1)

    def test_logout(self):
        login_page = LoginPage(self.chrome_driver)
        login_page.open()
        login_page.input_user_name(WASU_USER)
        login_page.input_password(WASU_PASSWORD)
        login_page.submit()
        time.sleep(1)
        summary_page = SummaryPage(self.chrome_driver)
        # time.sleep(5)
        summary_page.close_exit_btn()
        summary_page.logout()


if __name__ == "__main__":
    # unittest.main()
    suite = unittest.TestSuite()
    suite.addTest(TestLogin("test_logout"))
    runner = unittest.TextTestRunner()
    runner.run(suite)

    #
    # testunit.addTest(TestLogin("testLogout"))
    #
    # fp = open(RESULT_PATH + '/result.html', 'wb')
    # runner = HTMLTestRunner(stream=fp,
    #                         title='boss report')
    #
    # runner.run(testunit)
    # fp.close()





