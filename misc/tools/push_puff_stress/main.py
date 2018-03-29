# coding=utf-8
"""
create threads to request puff data
at the same time send hib to maintain connections
__author__ = 'zsw'
"""

import optparse
import threading
from push_session import *


def request_puff_data(all_nums):
    threads = list()
    threads.append(threading.Thread(target=push_session_req, args=(0.0005, 0, int(all_nums))))
    threads.append(threading.Thread(target=push_session_hib, args=(0.0005, 0, int(all_nums), 1000)))
    t1 = time.time()
    print "start send packages"
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    print "end", time.time() - t1


###################################
# Main Function
###################################
if __name__ == '__main__':
    parser = optparse.OptionParser(
        usage="%prog [optons] [<arg1> <arg2> ...]",
        version="1.0"
    )
    parser.add_option('-n', '--num', dest='lf_num',
                      type='int', default=10, help='how many leifeng to start')
    (options, args) = parser.parse_args()
    lf_num = options.lf_num

    print "lf num is:", lf_num

    request_puff_data(lf_num)
