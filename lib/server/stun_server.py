# coding=utf-8
"""
stun related api test keyword

__author__ = 'zengyuetian'

"""
import json
import threading
import requests
from lib.common.trace import *


@print_trace
def join_leifeng(host, port, file_id, file_url, peer_ids):

    url = "http://" + host + ":" + port + "/join_lf"

    headers = dict()
    headers['content-type'] = 'application/json'
    headers['accept'] = 'application/json'

    if type(peer_ids) != list:
        peer_ids = [peer_ids]

    body_data = {
        "file_id": file_id,
        "file_url": file_url,
        "peer_ids": peer_ids
    }

    response = requests.post(url=url, headers=headers, data=json.dumps(body_data))

    print "##############  join LF  #################"
    print "status_code: {0}".format(response.status_code)
    print "url: {0}".format(url)
    print "data: {0}".format(body_data)
    print "resp: {0}".format(response.text)
    print "########################################"
    return response
