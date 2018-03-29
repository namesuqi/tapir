# coding=utf-8
# author: zengyuetian

import unittest
import threading
from lib.common.log import *
from lib.common.decorator import *
from lib.remote.const import *
from lib.remote.player_controller import *
from lib.remote.sdk_controller import *
from testsuite.linux.multi_node.const import *

class SdkProcess(unittest.TestCase):
    @func_doc
    def testSDKProcess(self):
        """
        verify sdk process not stop
        @owner: zengyuetian
        @reviewer: jinyifan
        :return:
        """
        process_count = 0

        for ip in PEERS:
            process_count += count_sdk_process(ip)

        print "**** Find {0} sdk process".format(process_count)
        self.assertEqual(process_count, SDK_NUM * len(PEERS))


if __name__ == "__main__":
    unittest.main()