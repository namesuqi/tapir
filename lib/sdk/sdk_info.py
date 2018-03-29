# coding=utf-8
# author: zengyuetian

from lib.sdk.dash_board import *
from lib.request.resp_parser import *


def get_peer_id_via_url(host, port):
    """
    get sdk peer id from dashboard
    :param host: sdk host
    :param port: sdk port
    :return: peer id string
    """
    data = get_conf(host, port)
    peer_id = get_response_data_by_path(data, "/peer_id")
    return peer_id


if __name__ == "__main__":
    print get_peer_id_via_url("192.168.124.36", "32719")