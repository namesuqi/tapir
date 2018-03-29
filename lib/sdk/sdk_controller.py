# coding=utf-8
# author: zengyuetian
# lib to control sdk

from lib.sdk.sdk_constant import *
from lib.common.remoter import *


def deploy_sdk(ip):
    """
    copy sdk from robotframe machine to sdk machine
    :param ip: sdk machine
    :return: None
    """
    # kill previous processes
    kill_cmd = "killall -9 {0}".format(SDK_FILE)
    remote_execute(ip, ROOT_USER, ROOT_PASSWORD, kill_cmd)

    # create sdk dir
    mkdir_cmd = "mkdir -p {0}".format(REMOTE_SDK_PATH)
    remote_execute(ip, ROOT_USER, ROOT_PASSWORD, mkdir_cmd)

    # copy file to remote sdk dir
    copy_file_to(ip, ROOT_USER, ROOT_PASSWORD, LOCAL_SDK, REMOTE_SDK)

    # make sdk executable
    chmod_cmd = "chmod +x {0}".format(REMOTE_SDK)
    remote_execute(ip, ROOT_USER, ROOT_PASSWORD, chmod_cmd)


def start_sdk(ip=REMOTE_SDK_IP, port=SDK_PORT):
    """
    start sdk
    :param ip: sdk machine
    :param port: port to sdk startup
    :return: None
    """
    p2pclient = "ulimit -c unlimited && cd {0} && nohup ./{1}".format(REMOTE_SDK_PATH, SDK_FILE)
    cmd = "{0} -p {1}  > /dev/null 2>&1 &".format(p2pclient, port)
    remote_execute(ip, ROOT_USER, ROOT_PASSWORD, cmd)


def stop_sdk(ip=REMOTE_SDK_IP):
    """
    stop sdk process
    :param ip: sdk machine
    :return: None
    """
    kill_cmd = "killall -9 {0}".format(SDK_FILE)
    remote_execute(ip, ROOT_USER, ROOT_PASSWORD, kill_cmd)


def start_sdk_check(time_out, ip=REMOTE_SDK_IP):
    start_cmd = "nohup python %s %s > /dev/null 2>&1 &" % (REMOTE_CHECK_PYTHON_FILE, str(time_out))
    remote_execute(ip, ROOT_USER, ROOT_PASSWORD, start_cmd)


def start_sdk_live_flv(ip=REMOTE_SDK_IP):
    start_cmd = "nohup python %s http://127.0.0.1:32717/live_flv/user/wasu?" \
                "url=http://flv.srs.cloutropy.com/wasu/test.flv > /dev/null 2>&1 &" % (REMOTE_ROOT_PATH + "/play.py")
    remote_execute(ip, ROOT_USER, ROOT_PASSWORD, start_cmd)


if __name__ == '__main__':
    pass
