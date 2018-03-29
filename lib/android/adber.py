# coding=utf-8
# author: zengyuetian
# adb command wrapper

"""
Access android via adb
"""

import os
import subprocess
import multiprocessing
import json
from lib.common.trace import *
from lib.android.const import *


@print_trace
def get_current_dir(apk_location):
    script_dir = os.getcwd()
    actual_dir = script_dir + apk_location
    return actual_dir


@print_trace
def adb_push(device, src, dest):
    """
    push file from local to target
    """
    command = "adb -s {0} push {1} {2}".format(device, src, dest)
    print "adb command is: " + str(command)
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    return process.stdout.readlines()

@print_trace
def adb_shell(device, cmd):
    """
    adb shell operation about android devices file
    :adb -s <android device uuid> cat /sdcard/yunshang/yunshang.conf
    """
    command = "adb -s {0} shell {1}".format(device, cmd)
    print "adb command is: " + str(command)
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    return process.stdout.readlines()


def adb_shell_root(device, cmd):
    """
    run command on android with su
    echo touch 1 | adb shell su
    """
    command = "echo {0} ".format(cmd) + " | adb -s {0} shell su".format(device)
    print command
    subprocess.Popen(command, shell=True)


@print_trace
def get_by_url(device, path, file_name, url):
    """
    Operation about get android apk status or version from web
    """
    command = "adb -s {0} shell busybox wget -O {1}/{2} {3}".format(device, path, file_name, url)
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    print command
    process.stdout.readlines()


@print_trace
def get_apk_status(adb_result):
    """
    Operation about get android apk login status
    :return status
    """
    status = adb_result[0]
    print "login file content is: " + str(status)
    return json.loads(status).get('status', None)


@print_trace
def get_apk_version(adb_result):
    """
    Operation about get android apk vesion
    :return vesion
    """
    version = adb_result[0]
    print "version file content is: " + str(version)
    return json.loads(version).get('core', None)


@print_trace
def delete_file(device, path, file_name):
    """
    Operation about delete file
    """
    command = "adb -s {0} shell rm -rf {1}/{2}".format(device, path, file_name)
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    print command
    process.stdout.readlines()