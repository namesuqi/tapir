# coding=utf-8
# author: zengyuetian
# sdk related operations

import json
import time
from lib.common.path import *
from lib.android.adber import *


conf_in_data = "/data/data/com.cloutropy.bplayer/files/yunshang.conf"
conf_in_sdcard = "/sdcard/yunshang/yunshang.conf"
temp_in_sdcard = "/sdcard/temp"
conf_in_sdcard_temp = temp_in_sdcard + "/yunshang.conf"
temp_in_local = MISC_PATH + "/temp"
conf_in_local = temp_in_local + "/yunshang.conf"


@print_trace
def remove_file(device, file_name):
    """
    remove file on android device
    :param device: target device
    :param file_name: file name
    :return: N.A.
    """
    cmd = "rm -rf {0}".format(file_name)
    # cmd = "ls"
    adb_shell_root(device, cmd)


@print_trace
def get_peer_id_via_file(device):
    """
    get peer id via yunshang.conf
    :param device: target device
    :return: peer id string
    """
    # create yunshang dir
    cmd = "mkdir /sdcard/yunshang"
    adb_shell(device, cmd)

    # copy yunshang.conf to sdcard
    cmd = "cp {0} {1}".format(conf_in_data, conf_in_sdcard)
    adb_shell_root(device, cmd)

    time.sleep(2)
    # get peer id from sdcard
    cmd = "cat {0}".format(conf_in_sdcard)
    conf = adb_shell(device, cmd)[0]
    # {"peer_id": "075BCE399554441885B49170BA0EC2D2","disk_quota": 100}
    print conf
    return eval(conf).get("peer_id")


@print_trace
def get_conf_via_file(device):
    """
    get content of yunshang.conf
    :param device: target device
    :return: content
    """
    # create yunshang dir
    cmd = "mkdir /sdcard/yunshang"
    adb_shell(device, cmd)

    # copy yunshang.conf to sdcard
    cmd = "cp {0} {1}".format(conf_in_data, conf_in_sdcard)
    adb_shell_root(device, cmd)
    time.sleep(2)
    # get peer id from sdcard
    cmd = "cat {0}".format(conf_in_sdcard)
    conf = adb_shell(device, cmd)[0]
    print "CONF file content", conf
    # {"peer_id": "075BCE399554441885B49170BA0EC2D2","disk_quota": 100}
    return conf


@print_trace
def delete_peer_id_file(device):
    """
    delete yunshang.conf
    :param device: target device
    :return: N.A.
    """
    remove_file(device, conf_in_data)
    remove_file(device, conf_in_sdcard)


@print_trace
def is_hex_string(target_string):
    """
    check if a string is hex string
    :param target_string: target
    :return: Bool
    """
    ret = True
    for c in target_string:
        c = c.upper()
        if c not in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "A", "B", "C", "D", "E", "F"]:
            ret = False
            break
    return ret


@print_trace
# def modify_peer_id(device, pid=None, disk_quota=100):
def modify_peer_id(device, content):
    # content = '{"peer_id": "pi","disk_quota": dq}'
    #
    # if pid is not None:
    #     content = content.replace("pi", pid)
    # else:
    #     content = content.replace('"pi"', "")
    # content = content.replace("dq", str(disk_quota))

    # create yunshang.conf
    cmd = "echo {0} > {1}".format(content, temp_in_local + "/yunshang.conf")
    os.system(cmd)

    # push yunshang.conf to sdcard temp folder
    cmd = "mkdir {0}".format(temp_in_sdcard)
    adb_shell_root(device, cmd)
    adb_push(device, conf_in_local, conf_in_sdcard_temp)

    # copy yunshang.conf to data
    cmd = "cp {0} {1}".format(conf_in_sdcard_temp, conf_in_data)
    adb_shell_root(device, cmd)
    return content



if __name__ == "__main__":
    # peer_id = get_peer_id_via_file(ANDROID_DEVICE)
    # print peer_id
    # print is_hex_string(peer_id)
    # print is_hex_string("075BCE399554441885B49170BA0EG2D2")
    modify_peer_id(ANDROID_DEVICE, "")







