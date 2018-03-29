# coding=utf-8
# author: zengyuetian

import os
import subprocess
import time
from lib.common.host import *
from lib.common.trace import *
from lib.ios.const import *


@print_trace
def start_appium(device, no_reset=None, ip=None, port=None):
    """
    appium -a 127.0.0.1 -p 4723  –U  4ca1558c  --no-reset
    use different variable to running appium
    :param device: device id
    :param no_reset:
    :param ip: appium server ip
    :param port: appium server port
    :return:
    """

    # stop it firstly
    stop_appium()

    if ip is None:
        ip = APPIUM_SERVER
    if port is None:
        port = APPIUM_PORT
    if no_reset is None:
        no_reset = ""
    else:
        no_reset = "--no-reset"

    command = "appium -a {0} -p {1} -U {2} {3}".format(ip, port, device, no_reset)
    print command
    subprocess.Popen(command, shell=True)
    # wait appium launched
    time.sleep(10)


@print_trace
def stop_appium():
    if host_type == "Windows":
        command = "taskkill /F /IM node.exe"
    else:
        command = "killall -9 node"
    print command
    os.system(command)


@print_trace
def restart_appium(device, ip=None, port=None, no_reset=None):
    stop_appium()
    start_appium(device, ip, port, no_reset)

if __name__ == "__main__":
    start_appium(IOS_DEVICE, IOS_PLATFORM)
    stop_appium()

