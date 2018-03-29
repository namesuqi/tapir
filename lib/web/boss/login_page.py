# coding=utf-8
"""
Login Page related operations

__author__ = 'zengyuetian'

"""

from selenium.webdriver.common.by import By
from lib.web.boss.boss_page import *


class LoginPage(BossPage):
    url = '/'

    # locator
    username_loc = (By.ID, "username")
    password_loc = (By.ID, "password")
    submit_loc = (By.ID, "submit")


    # action
    def input_user_name(self, username):
        self.find_element(*self.username_loc).send_keys(username)

    def input_password(self, password):
        self.find_element(*self.password_loc).send_keys(password)

    def submit(self):
        self.find_element(*self.submit_loc).click()


if __name__ == "__main__":
    option = webdriver.ChromeOptions()
    option.add_argument("test-type")
    driver = webdriver.Chrome(chrome_options=option)
    driver.implicitly_wait(10)
    driver.maximize_window()

    login_page = LoginPage(driver)
    login_page.open()
    login_page.input_user_name("wasu")
    login_page.input_password("wasu1234")
    login_page.submit()



