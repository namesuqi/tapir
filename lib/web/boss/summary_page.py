# coding=utf-8
"""
Login Page related Keywords

__author__ = 'zengyuetian'

"""

from selenium.webdriver.common.by import By
from time import sleep
from lib.web.boss.boss_page import BossPage
from lib.web.boss.login_page import *


class SummaryPage(BossPage):
    url = '/summary'

    # locator
    nav_btn_loc = (By.XPATH, "/html/body/div[1]/div/div/div/button/span[1]")
    logout_btn_loc = (By.XPATH, "/html/body/div[1]/div/div/div/ul/li[2]/a/span[2]")
    flow_selector_loc = (By.CSS_SELECTOR,
                         "#content > div > div.chart-toolbar.clearfix > div.form-inline.pull-left > div > select > option:nth-child(1)")
    peer_selector_loc = (By.CSS_SELECTOR,
                         "#content > div > div.chart-toolbar.clearfix > div.form-inline.pull-left > div > select > option:nth-child(2)")
    user_selector_loc = (By.CSS_SELECTOR,
                         "#content > div > div.chart-toolbar.clearfix > div.form-inline.pull-left > div > select > option:nth-child(3)")
    online_user_selector_loc = (By.CSS_SELECTOR,
                         "#content > div > div.chart-toolbar.clearfix > div.form-inline.pull-left > div > select > option:nth-child(4)")
    band_width_selector_loc = (By.CSS_SELECTOR,
                         "#content > div > div.chart-toolbar.clearfix > div.form-inline.pull-left > div > select > option:nth-child(5)")
    grid_btn_loc = (By.XPATH,
                    '//*[@id="content"]/div/div[2]/div[2]/button[1]')
    table_btn_loc = (By.XPATH,
                     '//*[@id="content"]/div/div[2]/div[2]/button[2]')

    exit_btn_loc = (By.XPATH, "/html/body/div[3]/div/footer/ul/li[1]/a")

    # def logout(self):
    #     self.find_element(*self.nav_btn_loc).click()
    #     self.find_element(*self.logout_btn_loc).click()

    def get_login_user_name(self):
        username = self.find_element(*self.nav_btn_loc).text
        return username

    def select_flow_stastics(self):
        self.find_element(*self.flow_selector_loc).click()

    def select_peer_stastics(self):
        self.find_element(*self.peer_selector_loc).click()

    def select_user_stastics(self):
        self.find_element(*self.user_selector_loc).click()

    def select_online_user_stastics(self):
        self.find_element(*self.online_user_selector_loc).click()

    def select_band_width_stastics(self):
        self.find_element(*self.band_width_selector_loc).click()

    def switch_to_grid_report(self):
        self.find_element(*self.grid_btn_loc).click()

    def switch_to_table_report (self):
        self.find_element(*self.table_btn_loc).click()

    def logout(self):
        self.navigate("/logout")
        time.sleep(2)

    def close_exit_btn(self):
        self.find_element(*self.exit_btn_loc).click()






