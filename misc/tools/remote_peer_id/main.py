# coding=utf-8
# author: zengyuetian


import requests
import json
from lib.remote.const import *
from lib.common.remoter import *

BY_HTTP = True  # get peer_id from /ajax/conf or not
SDK_IP = "192.168.2.38"
SDK_NUM = 50

ROOT_USER = "root"
ROOT_PASSWORD = "root"
PORT_STEP = 10
PORT_START = 60000


def get_id_by_ajax(ip, lf_num, port):
    peer_ids = list()
    distance = 0
    for i in range(lf_num):
        url = "http://{0}:{1}{2}".format(ip, port + distance, "/ajax/conf")
        headers = dict()
        headers["accept"] = 'application/json'
        headers["content-type"] = 'application/json'
        res = requests.get(url, headers=headers)
        peer_id = json.loads(res.content).get("peer_id", None)
        peer_ids.append(peer_id)
        distance += PORT_STEP

    return peer_ids


def get_id_by_conf(ip, lf_num, user, passwd):
    ids = list()
    for i in range(lf_num):
        sdk_path = REMOTE_SDK_PATH + "/{0}".format(i)
        cmd = "cat {0}/yunshang/yunshang.conf".format(sdk_path)
        line = remote_execute_result(ip, user, passwd, cmd)
        peer_id = json.loads(line).get("peer_id", None)
        print(peer_id)
        ids.append(peer_id)
    return ids

if __name__ == "__main__":

    if BY_HTTP:
        # via ajax/conf
        print get_id_by_ajax(SDK_IP, SDK_NUM, PORT_START)
    else:
        # via yunshang.conf
        print get_id_by_conf(SDK_IP, SDK_NUM, ROOT_USER, ROOT_PASSWORD)



