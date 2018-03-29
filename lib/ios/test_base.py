# coding=utf-8
# author: zengyuetian
import unittest
from lib.common.HTMLTestRunner import HTMLTestRunner
from lib.ios.appiumer import *
from lib.ios.application import *
from lib.common.decorator import *
# from lib.sdk.dash_board import *
from lib.common.result import *
# from lib.request.resp_parser import *


class TestBase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print "Appium Start ...."
        start_appium(IOS_DEVICE, IOS_PLATFORM)

    @classmethod
    def tearDownClass(cls):
        print "Appium End ..."
        stop_appium()

    def setUp(self):
        print "Test Start ...."
        self.app = Application()
        self.app.initialize(IOS_DEVICE, IOS_PLATFORM, IOS_DEVICE, DEMO_APP, DEMO_BUNDLE_ID)

    def tearDown(self):
        print "Test End ..."
        self.app.close()
