# coding=utf-8
# author: zengyuetian


import threading
import time
import requests
import json
import unittest
from lib.common.log import *
from lib.common.decorator import *
from lib.remote.const import *
from lib.remote.player_controller import *
from lib.remote.sdk_controller import *
from testsuite.linux.multi_node.const import *

mutex = threading.Lock()
p2p_list = []
download_rate_list = []


def send_request(host_ip, host_port, url):
    url = "http://{0}:{1}{2}".format(host_ip, host_port, url)
    headers = dict()
    headers["accept"] = 'application/json'
    resp = requests.get(url, headers=headers, timeout=5)
    return resp


def get_sdk_data(host_ip, host_port):
    try:
        res = send_request(host_ip, host_port, "/ajax/report")
        p2p_percent = json.loads(res.content).get("p2p_percent", None)
        download_rate = json.loads(res.content).get("download_rate", None)
        if mutex.acquire(1):
            p2p_list.append(p2p_percent)
            download_rate_list.append(download_rate)
            mutex.release()
    except Exception as e:
        if mutex.acquire(1):
            p2p_list.append(0)
            download_rate_list.append(0)
            mutex.release()


class GetP2P(unittest.TestCase):
    @func_doc
    def testGetP2P(self):
        """
        verify p2p percentage
        @owner: zengyuetian
        @reviewer: jinyifan
        :return:
        """
        for ip in PEERS:
            for i in range(SDK_NUM):
                port = i * SDK_PORT_STEP + SDK_PORT_START
                t = threading.Thread(target=get_sdk_data, args=(ip, port))
                t.start()
                # print "Thread name is", t.getName()

        main_thread = threading.currentThread()
        for t in threading.enumerate():
            if t is not main_thread:
                t.join()

        sdk_count = len(p2p_list)
        total_p2p = sum(p2p_list)
        print("Total SDK num is {0}".format(sdk_count))
        print "P2P percent:"
        print p2p_list
        print "Download rate:"
        print download_rate_list

        average_p2p = total_p2p*1.0/sdk_count
        print "Average p2p percentage is ", average_p2p, "%"

        total_download_rate = sum(download_rate_list)
        average_download = total_download_rate * 1.0 / sdk_count
        print "Average download rate is ", average_download

        # we expect average p2p > 80%
        self.assertTrue(average_p2p > 80)

        # we expect average download rage > 500 bps
        self.assertTrue(average_download > 500)


if __name__ == "__main__":
    unittest.main()