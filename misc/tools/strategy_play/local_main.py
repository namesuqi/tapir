# coding=utf-8
# author: zengyuetian
# start sdk and player on local machine
# used as tool to connect specific LF nodes

import os
import time

SDK_FILE = 'ys_service_static'
SDK_PORT_STEP = 10
SDK_PORT_START = 60000

USE_LF_PREFIX = ""
# USE_LF_PREFIX = " -x 075BCE73 "

# USER_PREFIX = ""
USER_PREFIX = " -u 0x075bcfbd "

START_INTERVAL = 0.2


def stop_player():
    print "stop player"
    os.system(" ps aux | grep flv_play.py |grep -v grep |awk -F ' ' '{print $2}' | xargs kill -9")


def stop_sdk():
    print "stop sdk"
    os.system(" ps aux | grep ys_service_static |grep -v grep |awk -F ' ' '{print $2}' | xargs kill -9")


def create_folder(start, end):
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
        time.sleep(START_INTERVAL)


def start_player(start, end, url):
    print "start player for {start} to {end}".format(start=start, end=end)
    for i in range(start, end):
        port = i * SDK_PORT_STEP + SDK_PORT_START

        # url = "http://127.0.0.1:{port}/live_flv/user/wasu?url=http://test.live.entropycode.net/live/test3.flv" \
        #     .format(port=port)

        channel_url = "http://127.0.0.1:{port}/live_flv/user/xmtv?url={url}" \
            .format(port=port, url=url)
        cmd = "nohup python flv_play.py {url} > /dev/null 2>&1 &".format(url=channel_url)
        print cmd
        os.system(cmd)
        time.sleep(START_INTERVAL)


if __name__ == "__main__":

    import optparse

    parser = optparse.OptionParser(
        usage="%prog [optons] [<arg1> <arg2> ...]",
        version="1.0"
    )
    parser.add_option('-n', '--num', dest='num', type='int', default=10, help='how many sdk to start')
    parser.add_option('-l', '--url', dest='url', type='string', default="", help='channel url')
    (options, args) = parser.parse_args()
    num = options.num
    url = options.url
    print "sdk num is:", num
    print "url is:", url

    SDK_START = 0
    SDK_END = SDK_START + num

    # stop play
    stop_player()
    time.sleep(1)

    # stop sdk
    stop_sdk()
    time.sleep(1)

    # create folders
    create_folder(SDK_START, SDK_END)
    time.sleep(1)

    # start sdk
    start_sdk(SDK_START, SDK_END)
    time.sleep(1)

    start_player(SDK_START, SDK_END, url)



