# coding=utf-8
# author: zengyuetian

from lib.common.path import *
from lib.common.helper import *
from lib.remote.const import *

root_path = get_root_path()

USE_LF_PREFIX = "-x 00000002 "

ROOT_USER = "root"
ROOT_PASSWD = "root"

SDK_NUM = 50

FLV_PARSER = "flv_parse.py"
PLAYER = "play.py"

# sdk location on control machine
LOCAL_SDK = root_path + "/misc/sdk/linux/{0}".format(SDK_FILE)
LOCAL_FLV_PARSER = root_path + "/misc/pyplayer/{0}".format(FLV_PARSER)
LOCAL_PLAYER = root_path + "/misc/pyplayer/{0}".format(PLAYER)

# sdk location on peer machine
REMOTE_MN_PATH = "/root/multi_node"
REMOTE_SDK_PATH = REMOTE_MN_PATH + "/sdk"
REMOTE_SDK = REMOTE_SDK_PATH + "/{0}".format(SDK_FILE)

# player on peer machine
REMOTE_PLAYER_PATH = REMOTE_MN_PATH + "/pyplayer"
REMOTE_PLAYER = REMOTE_PLAYER_PATH + "/" + PLAYER
REMOTE_FLV_PARSER = REMOTE_PLAYER_PATH + "/" + FLV_PARSER

# channel url for udp and http
FILE_URL = "http://flv.srs.cloutropy.com/live/livestreamtest.flv"
FILE_ID = md5(FILE_URL).upper()
TEST_URL = "live_flv/user/wasu?url={0}".format(FILE_URL)

PEERS = ["192.168.4.236", "192.168.4.237", "192.168.4.238", "192.168.4.239",
         "192.168.4.243", "192.168.4.244", "192.168.4.245", "192.168.4.246"]
# PEERS = ["192.168.4.236"]
STUN_IP = "192.168.3.203"
STUN_PORT = "8000"

