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

class SdkCrash(unittest.TestCase):
    @func_doc
    def testFindCrash(self):
        """
        verify no core dump file
        @owner: zengyuetian
        @reviewer: jinyifan
        :return:
        """
        core_dump_num = 0

        for ip in PEERS:
            core_dump_num += find_crash(ip)

        print "**** Find {0} core dump files".format(core_dump_num)
        self.assertEqual(core_dump_num, 0)


if __name__ == "__main__":
    unittest.main()