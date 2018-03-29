from lib.common.path import get_root_path

SEND_SDK_IP = "192.168.201.3"
SEND_NAT_IP = "192.168.4.196"
RECEIVE_SDK_IP = "192.168.202.3"
RECEIVE_NAT_IP = "192.168.4.197"

# for simulator
ROOT_USERNAME = "root"
ROOT_PWD = "root"

# for sdk
ADMIN_USERNAME = "admin"
ADMIN_PWD = "admin"

REMOTE_SDK_PATH = "/home/admin/yssdk"
REMOTE_SDK_DIR_PATH = REMOTE_SDK_PATH + "/yunshang"

# control test command
root_path = get_root_path()
LOCAL_SIMULATOR_PATH = root_path + "/misc/tools/nat_simulator/"

REMOTE_SIMULATOR_PATH = "/home/admin/nat_simulator"
REMOTE_SIMULATOR = REMOTE_SIMULATOR_PATH + "/nat_simulator.py"
REMOTE_PENETRATE_LOG_PATH = REMOTE_SIMULATOR_PATH + "/log/penetrate.log"

START_SIMULATOR_CMD = "cd {0}; nohup python {1} %s > /dev/null 2>&1 &".format(REMOTE_SIMULATOR_PATH, REMOTE_SIMULATOR)
STOP_SIMULATOR_CMD = "ps aux | grep python | grep nat_simulator.py | grep -v grep | awk '{print $2}' | xargs kill"

# LIVE CHANNEL
CHANNEL = 'http://pl8.live.panda.tv/live_panda/012192e6277f7da070480d8ee32648fd.flv'
START_PLAY_CMD = 'nohup curl  --header "Range: bytes=0-335928740" -o vod.file ' \
                 '"http://127.0.0.1:32717/live_flv/user/xmtv?url=' \
                 '{0}" > /dev/null 2>&1 &'.format(CHANNEL)

# VOD CHANNEL
# CHANNEL = 'http://vodtest.crazycdn.com:8088/4k/4k_timer.flv'
# START_PLAY_CMD = 'nohup curl  --header "Range: bytes=0-335928740" -o vod.file ' \
#                  '"http://127.0.0.1:32717/vod/user/demo?url=' \
#                  '{0}" > /dev/null 2>&1 &'.format(CHANNEL)

# mock ts information
MOCK_TS_IP = "192.168.4.196"
MOCK_TS_FILE = "/home/admin/mock_ts/jsontext.txt"
GET_SEED_RSP_FORMAT = '{"seeds":[{"stunIP":"%s","version":"%s","natType":%s,"publicIP":"%s","publicPort":%s,' \
                      '"privateIP":"%s","privatePort":%s,"isp_id":"100017","ppc":304,"peer_id":"%s","cppc":1}]}'

# log keywords for check

#######################################
# PENEv1
# distinguish          = 0xa1
# C_PENE_PENETRATE_REQ = 0x03 --> a103
# C_PENE_PENETRATE_RSP = 0x04 --> a104
# C_PENE_PENETRATE_ACK = 0x05 --> a105
# C_PENE_REVERSING_REQ = 0x06 --> a106
#######################################

OUT_REVERSING = ([".*OUTside.*packet: a106.*", False], [".*INside.*packet: a103.*", False],
                 [".*OUTside.*packet: a104.*", False], [".*INside.*packet: a105.*", False])
OUT_NO_REVERSING = ([".*OUTside.*packet: a103.*", False], [".*INside.*packet: a104.*", False],
                    [".*OUTside.*packet: a105.*", False])
IN_REVERSING = ([".*INside.*packet: a106.*", False], [".*OUTside.*packet: a103.*", False],
                [".*INside.*packet: a104.*", False], [".*OUTside.*packet: a105.*", False])
IN_NO_REVERSING = ([".*INside.*packet: a103.*", False], [".*OUTside.*packet: a104.*", False],
                   [".*INside.*packet: a105.*", False])

#######################################
# DCCPv1
# distinguish = d1
#######################################
DCCP_DISTINGUISH = 'd1'
