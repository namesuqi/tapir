# coding=utf-8
# control the player
# author: zengyuetian

import time
from lib.common.log import *
from lib.common.remoter import *
from lib.common.trace import *
from lib.remote.const import *


@print_trace
@log_func_args
def deploy_player(ip, user, passwd):
    # create player dir
    mkdir_cmd = "mkdir -p {0}".format(REMOTE_PLAYER_PATH)
    remote_execute(ip, user, passwd, mkdir_cmd)

    # copy file to remote player dir
    copy_file_to(ip, user, passwd, LOCAL_PLAYER, REMOTE_PLAYER)
    copy_file_to(ip, user, passwd, LOCAL_FLV_PARSER, REMOTE_FLV_PARSER)

    # make sdk executable
    chmod_cmd = "chmod +x {0}".format(REMOTE_PLAYER)
    remote_execute(ip, user, passwd, chmod_cmd)


@print_trace
@log_func_args
def start_player(ip, url, num, user, passwd):
    for i in range(num):
        port = i * SDK_PORT_STEP + SDK_PORT_START
        live_url = "http://127.0.0.1:{0}/{1}".format(port, url)
        play_cmd = "cd {0} && nohup python {1} {2} > /dev/null 2>&1 &".format(REMOTE_PLAYER_PATH, REMOTE_PLAYER,
                                                                              live_url)
        remote_execute(ip, user, passwd, play_cmd)


@print_trace
@log_func_args
def count_player_process(ip, user, passwd):
    find_cmd = "ps aux|grep play.py|wc -l"
    result = remote_execute_result(ip, user, passwd, find_cmd)
    return (int(result) - 1) / 2  # ignore grep process and bash process


@print_trace
@log_func_args
def stop_player(ip, user, passwd):
    kill_cmd = "killall -9 python"
    remote_execute(ip, user, passwd, kill_cmd)
