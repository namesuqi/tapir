#!/usr/bin/env python
# coding=utf-8
# author: pan pan
# 本程序运行在NAT机器上
import os
import sys
import time
import signal
import threading

import global_var as glbv

from packet_forward import ForwardToOutside, n_logger


class NatSimulator(object):
    def __init__(self):
        pass

    @staticmethod
    def start(type_number):
        # 第一次启动时的线程名
        thread_name = "out_forward_0"
        out_bridgehead = ForwardToOutside(nat_type=type_number, thread_name=thread_name,
                                          network_card_name=glbv.PRI_NET_CARD, src_ip=glbv.PRI_NET_RANGE, dst_ip="",
                                          mock_ip=glbv.PUB_GW_HOST_IP, src_port=0, dst_port=0,
                                          mock_port=glbv.MOCK_GW_PORT)
        out_thread = threading.Thread(target=out_bridgehead.run_task, name=out_bridgehead.thread_name)
        out_thread.setDaemon(True)
        out_thread.start()
        glbv.G_THREAD_POOL.append(out_thread)
        return out_thread


def sig_handler(signum, frame):
    # 本函数仅仅用于标志退出位，具体的退出动作由子线程处理
    if not glbv.G_IS_EXIT:
        print "process begin to exit, please wait ..."
    glbv.G_IS_EXIT = True


if __name__ == '__main__':
    # 设置信号处理函数
    signal.signal(signal.SIGTERM, sig_handler)
    signal.signal(signal.SIGINT, sig_handler)

    nat_simulator = NatSimulator()

    # 存储线程索引号的列表
    index_list = list()

    # NAT type - 1, 2, 3, 4
    nat_type_num = glbv.DUMMY_NAT_TYPE
    if len(sys.argv) > 1:
        nat_type_num = sys.argv[1]

    # 启动指定类型的nat模拟器，并循环着将全局线程池G_THREAD_POOL中的不活跃线程删除。
    try:
        nat_simulator.start(nat_type_num)
        while len(glbv.G_THREAD_POOL) > 0:
            time.sleep(3)
            for i in range(len(glbv.G_THREAD_POOL)):
                if not glbv.G_THREAD_POOL[i].isAlive():
                    index_list.append(i)
            # 从后往前删，确保总能删掉
            index_list.reverse()
            for j in index_list:
                del glbv.G_THREAD_POOL[j]
            # 清空index_list
            del index_list[:]
    except KeyboardInterrupt:
        stop_command = "ps -ef | grep %s | grep -v grep | cut -c 9-15 | xargs kill -s 9" % os.path.basename(__file__)
        os.system(stop_command)
    except Exception, e:
        print "exception in running, error message: %s ." % e.message
    finally:
        del n_logger
    print "THE PROCESS EXIT DONE!"
