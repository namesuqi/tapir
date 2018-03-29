# coding=utf-8
# author: zengyuetian
import unittest
from lib.common.HTMLTestRunner import HTMLTestRunner
from lib.android.appiumer import *
from lib.android.application import *
from lib.common.decorator import *
from lib.sdk.dash_board import *
from lib.common.result import *
from lib.request.resp_parser import *
from lib.android.logcater import *


class TestBase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print "Appium Start ...."
        start_appium(ANDROID_DEVICE, ANDROID_PLATFORM)

    @classmethod
    def tearDownClass(cls):
        print "Appium End ..."
        stop_appium()


