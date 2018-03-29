# coding=utf-8
"""
TODO: Add description for file

__author__ = 'zengyuetian'

"""

import lib.web.DriverManager
from lib.web.SummaryPage import *
import unittest

class TestPage(unittest.TestCase):
    def test_login(self):
        login_page = LoginPage()
        login_page.Open()
        login_page.InputUsername("wasu")
        login_page.InputPassword("wasubj")
        login_page.Submit()
        login_page.Close()


    def test_logout(self):
        lib.web.DriverManager.CreateNewDriver()
        login_page = LoginPage()
        login_page.Open()
        login_page.InputUsername("wasu")
        login_page.InputPassword("wasubj")
        login_page.Submit()
        sleep(3)
        summary_page = SummaryPage()
        summary_page.Logout()
        sleep(3)
        summary_page.Close()


if __name__ == "__main__":
    # unittest.main()

    # suite = unittest.TestSuite()
    # suite.addTest(TestPage("test_logout"))
    # runner = unittest.TextTestRunner()
    # runner.run(suite)

    discover = unittest.defaultTestLoader.discover("./", pattern="*_test.py")
    runner = unittest.TextTestRunner()
    runner.run(discover)
