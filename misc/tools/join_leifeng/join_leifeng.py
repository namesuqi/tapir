# coding=utf-8
# author: zengyuetian
# start and join lf

import time
import sys
import optparse
from lib.remote.sdk_controller import *
from lib.server.stun_server import *

if __name__ == "__main__":

    # print time
    current = time.localtime()
    time_str = time.strftime("%Y/%m/%d %H:%M:%S", current)
    print "Timestamp {0}".format(time_str)

    # get peer_ids
    ids = ["0000000237154AF481F4D727C586117C"]

    # loop to join leifeng
    while True:
        time1 = time.time()
        # join leifeng
        join_leifeng(STUN_IP, STUN_PORT, FILE_ID, FILE_URL, ids)
        # sleep
        time.sleep(10)
        # timer it
        time2 = time.time()
        print "Cost {0} seconds".format(time2 - time1)

