# coding=utf-8
"""
mock multi lf push_session_req or hib or fin, lf => live-push server

__author__ = 'zsw'

"""
import json
import os

from creator import PEER_ID_FILE
from conf_data import *
from lib.protocol.puff.puff_factory import *
from lib.protocol.puff.puff_data import *
from lib.request.udp_request import *


def push_session_req(interval=SLEEP, peer_start_num=1, peer_stop_num=2, file_id=FILE_ID, file_url=FILE_URL,
                     port=PORT_START, peer_id_file=PEER_ID_FILE):
    # get peer id list
    with open(os.path.abspath(os.path.dirname(__file__)) + peer_id_file, "r") as f:
        peer_ids = json.load(f)

    print "push_session_req"
    print "port:", port, "file_id:", file_id, "file_url:", file_url

    # get local port
    local_port = port + peer_start_num

    # loop for each peer id
    for m in range(int(peer_start_num), int(peer_stop_num)):
        peer_id = peer_ids[m]
        if local_port >= 60000:
            local_port = m - 50000

        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind(("", int(local_port)))
        session_id = 184

        # build PUFF request data
        request_data = build_request_data(session_id, peer_id, file_url, CPPC_DEFAULT, PRIORITY_DEFAULT)
        req_data = request_data + udp_checksum(request_data).rjust(4, '0')
        s.sendto(binascii.a2b_hex(req_data), (PUSH_HOST, PUSH_PORT))

        if m % 500 == 0:
            print m, peer_id, local_port
            time.sleep(0.2)

        s.close()
        local_port += 1
        time.sleep(float(interval))


def push_session_hib(interval=SLEEP, peer_start_num=0, peer_stop_num=2, loop_times=3, file_url=FILE_URL,
                     port=PORT_START, wait_time=0, peer_id_file=PEER_ID_FILE):
    with open(os.path.abspath(os.path.dirname(__file__)) + peer_id_file, "r") as f:
        peer_ids = json.load(f)

    print "Current PUFF Heartbeat loop is: ", loop_times
    time.sleep(10)

    # time.sleep(wait_time)  # follow req
    for i in range(int(loop_times)):
        print "Start loop ", i
        time.sleep(wait_time)
        local_port = port + peer_start_num
        for m in range(int(peer_start_num), int(peer_stop_num)):

            if local_port >= 60000:
                local_port = m - 50000
            peer_id = peer_ids[m]
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            try:
                s.bind(("", int(local_port)))
            except:
                print "Port already bind: ", local_port
            session_id = 184

            # build PUFF hib data
            request_data = build_hib_data(session_id, peer_id, file_url)
            hib_data = request_data + udp_checksum(request_data).rjust(4, '0')
            s.sendto(binascii.a2b_hex(hib_data), (PUSH_HOST, PUSH_PORT))

            s.close()

            local_port += 1
            time.sleep(float(interval))