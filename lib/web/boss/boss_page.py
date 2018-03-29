# coding=utf-8
"""
base class for pages

__author__ = 'zengyuetian'

"""
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from lib.driver import chrome_driver


class BossPage(object):
    """
    base class
    """

    login_url = 'http://panel.shangcdn.com'

    def __init__(self, selenium_driver, base_url=login_url):

        self.base_url = base_url
        self.driver = selenium_driver

    def on_page(self):
        return self.driver.current_url == (self.base_url + self.url)

    def _open(self, url):
        url = self.base_url + url
        self.driver.get(url)
        print url
        # assert self.on_page(), 'Did not land on %s' % url

    def open(self):
        self._open(self.url)

    def navigate(self, url):
        self._open(url)

    def close(self):
        self.driver.close()

    def find_element(self, *loc):
        return self.driver.find_element(*loc)



