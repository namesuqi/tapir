# coding=utf-8
# author: zengyuetian

"""
Android application related operations
"""

from appium import webdriver
from lib.ios.const import *
from lib.common.trace import *


class Application(object):
    def __init__(self):
        self.driver = None

    @print_trace
    def initialize(self, device, platform, version, app_file, bundle_id):
        desired_caps = dict()
        desired_caps['deviceName'] = device
        desired_caps['platformName'] = platform
        desired_caps['platformVersion'] = version
        desired_caps['app'] = app_file
        desired_caps['bundleId'] = bundle_id
        server_url = 'http://{0}:{1}/wd/hub'.format(APPIUM_SERVER, APPIUM_PORT)
        print server_url
        self.driver = webdriver.Remote(server_url, desired_caps)
        print DEBUG_STRING, self.driver, id(self.driver)
        self.driver.implicitly_wait(10)
        return self.driver

    @print_trace
    def close(self):
        """
        Failed to start an Appium session, err was: Error: Requested a new session but one was in progress
        https://github.com/appium/appium/issues/1618
        Appium responds with an error and then you start a new session.
        You need to call driver.quit() before you start a new session.
        :return:
        """
        self.driver.close_app()
        self.driver.quit()

    @print_trace
    def start(self):
        self.driver.launch_app()

    @print_trace
    def restart(self):
        self.close()
        self.start()

    @print_trace
    def remove(self, package):
        self.driver.remove_app(package)

    @print_trace
    def launch(self):
        self.driver.launch_app()


if __name__ == "__main__":
    app = Application()
    app.initialize(IOS_DEVICE, IOS_PLATFORM, IOS_DEVICE, DEMO_APP, DEMO_BUNDLE_ID)