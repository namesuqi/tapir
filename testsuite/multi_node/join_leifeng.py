# coding=utf-8
# author: zengyuetian
# start and join lf

import time
import sys
import optparse
from lib.remote.sdk_controller import *
from lib.server.stun_server import *
from testsuite.linux.multi_node.const import *


if __name__ == "__main__":
    # parse options
    parser = optparse.OptionParser(
        usage="%prog [optons] [<arg1> <arg2> ...]",
        version="1.0"
    )
    parser.add_option('-n', '--num', dest='lf_num',
                      type='int', default=SDK_NUM, help='how many leifeng to join')
    (options, args) = parser.parse_args()
    lf_num = options.lf_num

    # print time
    current = time.localtime()
    time_str = time.strftime("%Y/%m/%d %H:%M:%S", current)
    print "Timestamp {0}".format(time_str)

    # get peer_ids
    peer_list = list()
    for ip in PEERS:
        ids = get_peer_ids(ip, lf_num)
        peer_list.append(ids)

    # loop to join leifeng
    while True:
        for ids in peer_list:
            time1 = time.time()
            # join leifeng
            join_leifeng(STUN_IP, STUN_PORT, FILE_ID, FILE_URL, ids)
            # sleep
            time.sleep(10)
            # timer it
            time2 = time.time()
            print "Cost {0} seconds".format(time2 - time1)
        # sleep
        time.sleep(10)
