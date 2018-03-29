# coding=utf-8
"""
Login Page related Keywords

__author__ = 'zengyuetian'

"""

from selenium.webdriver.common.by import By
from time import sleep
from lib.web.boss.boss_page import BossPage
from lib.web.boss.login_page import LoginPage


class SummaryVodPage(BossPage):
    url = '/summaryvod'

    def __init__(self):
        super(SummaryVodPage, self).__init__()

    def OpenSummaryVodPage(self):
        self.Open()

if __name__ == "__main__":
    login_page = LoginPage()
    login_page.Open()
    login_page.InputUsername("wasu")
    login_page.InputPassword("wasubj")
    login_page.Submit()
    sleep(3)
    summary_page = SummaryVodPage()
    summary_page.OpenSummaryVodPage()







