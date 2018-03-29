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

def stop_play(ip):
    """
    live play on one machine
    :param ip:
    :return:
    """
    stop_sdk(ip)
    stop_player(ip)


class StopPlay(unittest.TestCase):

    @func_doc
    def testStopPlay(self):
        """
        stop live play
        @owner: zengyuetian
        @reviewer: jinyifan
        """
        # stop sdk
        for ip in PEERS:
            t = threading.Thread(target=stop_play, args=(ip,))
            t.start()
            print "Thread name is", t.getName()
            time.sleep(1)

        main_thread = threading.currentThread()
        for t in threading.enumerate():
            if t is not main_thread:
                t.join()


if __name__ == "__main__":
    unittest.main()