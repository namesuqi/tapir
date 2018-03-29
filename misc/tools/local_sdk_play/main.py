# coding=utf-8
# author: zengyuetian
# start sdk and player on local machine
# used as tool to connect specific LF nodes

import os
import time
import sys

SDK_NUM = 100
URL = "http://test.live.entropycode.net/live/test3.flv"
START_PLAYER = False

SDK_FILE = 'ys_service_static'
SDK_PORT_STEP = 10
SDK_PORT_START = 60000

USE_LF_PREFIX = ""
# USE_LF_PREFIX = " -x 075BCE73 "

# USER_PREFIX = ""
USER_PREFIX = " -u 2 "

SDK_START = 0
# port = SDK_PORT_START + (SDK_END-SDK_START)*SDK_PORT_STEP
SDK_END = SDK_START + SDK_NUM


def print_help():
    print("")
    print "please use following format"
    print "******************************************************"
    print "python main.py [start|stop]"
    print "******************************************************"
    print("")
    exit(1)

def stop_player():
    print "stop player"
    os.system(" ps aux | grep flv_play.py |grep -v grep |awk -F ' ' '{print $2}' | xargs kill -9")


def stop_sdk():
    print "stop sdk"
    os.system(" ps aux | grep ys_service_static |grep -v grep |awk -F ' ' '{print $2}' | xargs kill -9")
    # os.system("killall -9 {proc}".format(proc=SDK_FILE))


def recreate_sdk_folder(start, end):
    print "recreate_sdk_folder from {start} to {end}".format(start=start, end=end)
    os.system("chmod +x ./{sdk}".format(sdk=SDK_FILE))
    for i in range(start, end):
        os.system("rm -rf ./{dir}".format(dir=i))
        os.system("mkdir -p ./{dir}".format(dir=i))
        os.system("cp ./{sdk}  ./{dir}/".format(sdk=SDK_FILE, dir=i))
        os.system("cp -r ./conf  ./{dir}/".format(dir=i))


def start_sdk(start, end):
    print "start sdk for {start} to {end}".format(start=start, end=end)
    for i in range(start, end):
        port = i * SDK_PORT_STEP + SDK_PORT_START
        p2pclient = "ulimit -c unlimited && cd {dir} && nohup ./{sdk}".format(dir=i, sdk=SDK_FILE)
        cmd = "{command} -p {port} {use_lf} {peer_user} > /dev/null 2>&1 &".format(
            command=p2pclient, port=port, use_lf=USE_LF_PREFIX, peer_user=USER_PREFIX)
        print cmd
        os.system(cmd)
        time.sleep(0.1)


def start_player(start, end):
    print "start player for {start} to {end}".format(start=start, end=end)
    for i in range(start, end):
        port = i * SDK_PORT_STEP + SDK_PORT_START
        url = "http://127.0.0.1:{port}/live_flv/user/xmtv?url={url}" \
            .format(port=port, url=URL)

        cmd = "nohup python flv_play.py {url} > /dev/null 2>&1 &".format(url=url)
        print cmd
        os.system(cmd)
        time.sleep(0.1)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print_help()
    else:
        action = sys.argv[1]
        if not (action == "start" or action == "stop"):
            print_help()
        # start sdk
        if action == "start":
            # stop play
            stop_player()
            time.sleep(1)

            # stop sdk
            stop_sdk()
            time.sleep(1)

            # re-create folders
            recreate_sdk_folder(SDK_START, SDK_END)
            time.sleep(1)

            # start sdk
            start_sdk(SDK_START, SDK_END)
            time.sleep(1)

            # start player
            if START_PLAYER:
                start_player(SDK_START, SDK_END)
        elif action == "stop":
            stop_player()
            time.sleep(1)

            # stop sdk
            stop_sdk()




