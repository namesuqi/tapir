# coding=utf-8
# author: zengyuetian
#

import threading
import time
from lib.sdk.dash_board import *
from lib.android.const import *
from lib.android.test_base import *
from lib.player.play import thread_play


class TestPlay(TestBase):

    @func_doc
    def testPlay(self):
        """
        apk初始化测试用例
        """
        pass
        channel_url = "http://{0}:{1}/{2}".format(ANDROID_HOST, SDK_PORT, CHANNEL1)
        print DEBUG_STRING, channel_url
        time.sleep(10)
        thread_play(channel_url)
        main_thread = threading.currentThread()
        for thread in threading.enumerate():
            if thread is main_thread:
                while True:
                    time.sleep(5)
                    data = get_report(ANDROID_HOST, SDK_PORT)
                    p2p = get_response_data_by_path(data, "/p2p_percent")
                    print DEBUG_STRING, "P2P", p2p


if __name__ == "__main__":
    unittest.main()
    # suite = unittest.TestSuite()
    # suite.addTest(TestInit("test_put_background"))
    #
    # unittest.TextTestRunner().run(suite)

