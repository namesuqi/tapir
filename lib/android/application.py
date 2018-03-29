# coding=utf-8
# author: zengyuetian

"""
Android application related operations
"""

from appium import webdriver
from lib.android.const import *
from lib.android.adber import *
from lib.common.trace import *


# @print_trace
# def get_apk_peer_id(device):
#     """
#     Operation about get android apk peer id
#     :return peerid
#     """
#     adb_result = adb_shell(device, "cat {0}".format(YUNSHANG_CONF))
#     peer_info = adb_result[0]
#     print "yunshang.conf file content is: " + str(peer_info)
#     peer_id = json.loads(peer_info).get('peer_id', None)
#     print "Peer Id is: {0}".format(peer_id)
#     return peer_id
#
#
# @print_trace
# def remove_peer_id_file(device):
#     """
#     Operation about get android apk peer id
#     :return peerid
#     """
#     adb_shell(device, "rm -rf {0}".format(YUNSHANG_CONF))


class Application(object):
    def __init__(self):
        self.driver = None

    @print_trace
    def initialize(self, device, platform, version, app, package, activity):
        """
        start a new session to start app
        :param device:
        :param platform:
        :param version:
        :param app:
        :param package:
        :param activity:
        :return:
        """
        desired_caps = dict()
        desired_caps['platformName'] = platform
        desired_caps['platformVersion'] = version
        desired_caps['deviceName'] = device
        desired_caps['app'] = app
        desired_caps['appPackage'] = package
        desired_caps['appActivity'] = activity
        server_url = 'http://{0}:{1}/wd/hub'.format(APPIUM_SERVER, APPIUM_PORT)
        print server_url
        self.driver = webdriver.Remote(server_url, desired_caps)
        print DEBUG_STRING, self.driver, id(self.driver)
        self.driver.implicitly_wait(5)
        return self.driver

    @print_trace
    def quit(self):
        """
        close app and quit session

        Failed to start an Appium session, err was: Error: Requested a new session but one was in progress
        https://github.com/appium/appium/issues/1618
        Appium responds with an error and then you start a new session.
        You need to call driver.quit() before you start a new session.
        :return:
        """
        self.driver.close_app()
        self.driver.quit()

    @print_trace
    def launch(self):
        """
        launch app
        :return:
        """
        self.driver.launch_app()

    @print_trace
    def close(self):
        """
        only close app
        :return:
        """
        self.driver.close_app()

    @print_trace
    def start(self, device, platform, version, app, package, activity):
        """
        start a new session to start app
        :param device:
        :param platform:
        :param version:
        :param app:
        :param package:
        :param activity:
        :return:
        """
        self.initialize(device, platform, version, app, package, activity)

    @print_trace
    def restart(self, device, platform, version, app, package, activity):
        """
        close app and restart session
        :param device:
        :param platform:
        :param version:
        :param app:
        :param package:
        :param activity:
        :return:
        """
        self.quit()
        self.initialize(device, platform, version, app, package, activity)

    @print_trace
    def remove(self, package):
        """
        remove app from android device
        :param package:
        :return:
        """
        self.driver.remove_app(package)




#     @print_trace
#     def close_messages(self):
#         close_unable_play_message()
#
#
# OK_BUTTON_LOC = "android:id/button1"
# CHANNEL_1_LOC = ""


# def close_unable_play_message():
#     # btn = glob.appium_driver.find_element_by_class_name("android.widget.Button")
#     btn = appium_driver.find_element_by_id(OK_BUTTON_LOC)
#     btn.click()
#
#
# def start_channel():
#     ch1_label = appium_driver.find_element_by_id(CHANNEL_1_LOC)
#     ch1_label.click()

if __name__ == "__main__":
    app = Application()
    app.initialize(ANDROID_DEVICE, ANDROID_PLATFORM, ANDROID_VERSION, DEMO_APK, DEMO_PACKAGE_NAME, DEMO_ACTIVITY_NAME)