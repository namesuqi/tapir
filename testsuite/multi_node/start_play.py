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


def live_play(ip):
    """
    live play on one machine
    :param ip:
    :return:
    """
    stop_sdk(ip)
    stop_player(ip)
    deploy_sdk(ip)
    deploy_player(ip)
    start_sdk(ip, SDK_NUM)
    start_player(ip, TEST_URL, SDK_NUM)


class StartPlay(unittest.TestCase):
    @func_doc
    def setUp(self):
        pass

    @func_doc
    def tearDown(self):
        pass

    @func_doc
    def testMultiPlay(self):
        """
        play live url on multi hosts with threads
        @owner: zengyuetian
        @reviewer: jinyifan
        """
        # stop sdk
        for ip in PEERS:
            t = threading.Thread(target=live_play, args=(ip,))
            t.start()
            print "Thread name is", t.getName()
            time.sleep(1)

        main_thread = threading.currentThread()
        for t in threading.enumerate():
            if t is not main_thread:
                t.join()


if __name__ == "__main__":
    unittest.main()