# coding=utf-8
# author: zengyuetian
# start and join lf


import time
import sys
from lib.remote.const import *
from lib.remote.sdk_controller import *

SDK_IP = "192.168.4.239"
SDK_NUM = 10

ROOT_USER = "root"
ROOT_PASSWD = "root"
REMOTE_SDK_PATH = REMOTE_MULTI_NODE_PATH + "/sdk"


def print_help():
    print("")
    print "please use following format"
    print "******************************************************"
    print "python main.py [start|stop]"
    print "******************************************************"
    print("")
    exit(1)


if __name__ == "__main__":
    time1 = time.time()

    if len(sys.argv) != 2:
        print_help()
    else:
        action = sys.argv[1]
        if not (action == "start" or action == "stop"):
            print_help()

        # start leifeng
        if action == "start":
            # stop sdk
            print("Stop sdk for {0}".format(SDK_IP))
            stop_sdk(SDK_IP, user=ROOT_USER, passwd=ROOT_PASSWD)

            # deploy sdk
            print("Deploy sdk for {0}".format(SDK_IP))
            deploy_sdk(SDK_IP, user=ROOT_USER, passwd=ROOT_PASSWD)

            # start sdk
            print("Start sdk for {0}".format(SDK_IP))
            start_sdk(SDK_IP, SDK_NUM, user=ROOT_USER, passwd=ROOT_PASSWD)
        elif action == "stop":
            print("Stop sdk for {0}".format(SDK_IP))
            stop_sdk(SDK_IP, user=ROOT_USER, passwd=ROOT_PASSWD)

        # timer it
        time2 = time.time()
        print "Cost {0} seconds to {1}".format(time2 - time1, action)
