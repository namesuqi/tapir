# coding=utf-8
# author: zengyuetian

import unittest

from testsuite.linux.multi_node.get_p2p import *
from testsuite.linux.multi_node.player_process import *
from testsuite.linux.multi_node.sdk_crash import *
from testsuite.linux.multi_node.sdk_process import *
from testsuite.linux.multi_node.stop_play import *


if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(GetP2P("testGetP2P"))
    suite.addTest(PlayerProcess("testPlayerProcess"))
    suite.addTest(SdkCrash("testFindCrash"))
    suite.addTest(SdkProcess("testSDKProcess"))
    suite.addTest(StopPlay("testStopPlay"))
    runner = unittest.TextTestRunner()
    runner.run(suite)

