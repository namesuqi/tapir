# coding=utf-8
# author = zengyuetian

import json
import time
from lib.common.log import *
from lib.common.remoter import *
from lib.remote.const import *
from lib.common.trace import *


@print_trace
@log_func_args
def deploy_sdk(ip, user, passwd):
    # delete previous sdk
    rm_cmd = "rm -rf {0}".format(REMOTE_SDK_PATH)
    remote_execute(ip, user, passwd, rm_cmd)
    time.sleep(2)

    # create sdk dir
    mkdir_cmd = "mkdir -p {0}".format(REMOTE_SDK_PATH)
    remote_execute(ip, user, passwd, mkdir_cmd)

    # create sdk dir
    mkdir_cmd = "mkdir -p {0}".format(REMOTE_SDK_PATH+"/conf")
    remote_execute(ip, user, passwd, mkdir_cmd)

    # copy file to remote sdk dir
    copy_file_to(ip, user, passwd, LOCAL_SDK, REMOTE_SDK)
    copy_file_to(ip, user, passwd, LOCAL_LOG_CONF, REMOTE_LOG_CONF)

    # make sdk executable
    chmod_cmd = "chmod +x {0}".format(REMOTE_SDK)
    remote_execute(ip, user, passwd, chmod_cmd)


@print_trace
@log_func_args
def start_sdk(ip, num, user, passwd):
    for i in range(num):
        mkdir_cmd = "cd {0} && mkdir {1} && cp {2} {1}".format(REMOTE_SDK_PATH, i, SDK_FILE)
        remote_execute(ip, user, passwd, mkdir_cmd)

        port = i * SDK_PORT_STEP + SDK_PORT_START

        cmd = "ulimit -c unlimited && cd {0}/{1} && nohup ./{2}".format(REMOTE_SDK_PATH, i, SDK_FILE)
        start_cmd = "{0} -p {1} {2} > /dev/null 2>&1 &".format(cmd, port, USE_LF_PREFIX)
        remote_execute(ip, user, passwd, start_cmd)


@print_trace
@log_func_args
def get_peer_ids(ip, num, user, passwd):
    ids = list()
    for i in range(num):
        lf_path = "{0}/{1}".format(REMOTE_SDK_PATH, i)
        cmd = "cat {0}/yunshang/yunshang.conf".format(lf_path)
        line = remote_execute_result(ip, user, passwd, cmd)
        peer_id = json.loads(line).get("peer_id", None)
        print(peer_id)
        ids.append(peer_id)
    return ids


@print_trace
@log_func_args
def stop_sdk(ip, user, passwd):
    kill_cmd = "killall -9 {0}".format(SDK_FILE)
    remote_execute(ip, user, passwd, kill_cmd)


@print_trace
@log_func_args
def find_crash(ip, user, passwd):
    """
    find how many sdk gets crashed
    """
    find_cmd = "find {0} -name core.* |wc -l".format(REMOTE_SDK_PATH)
    result = remote_execute_result(ip, user, passwd, find_cmd)
    return int(result)


@print_trace
@log_func_args
def count_sdk_process(ip, user, passwd):
    find_cmd = "ps aux|grep {0}|wc -l".format(SDK_FILE)
    result = remote_execute_result(ip, user, passwd, find_cmd)
    return (int(result) - 1) / 2         # ignore grep process and bash process


@print_trace
@log_func_args
def get_sdk_version(ip, port, user, passwd):
    cmd = "curl http://{0}:{1}{2}".format(ip, port, "/ajax/version")
    result = remote_execute_result(ip, user, passwd, cmd)
    return json.loads(result).get("core", None)



