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


class PlayerProcess(unittest.TestCase):
    @func_doc
    def testPlayerProcess(self):
        """
        verify player process not stop
        @owner: zengyuetian
        @reviewer: jinyifan
        :return:
        """
        process_count = 0

        for ip in PEERS:
            process_num = count_player_process(ip)
            print("player number: {0}".format(process_num))
            process_count += process_num

        print "**** Find {0} player process".format(process_count)
        self.assertEqual(process_count, SDK_NUM * len(PEERS))


if __name__ == "__main__":
    unittest.main()