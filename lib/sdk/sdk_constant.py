#coding=utf-8
import re
from lib.common.path import get_root_path
# from lib.sdk.common_tool.verify_handle import verify_port_occupancy


# 当前测试SDK版本号
EXPECT_SDK_VERSION = u'3.19.6'

# root_path = PathController.get_root_path()
root_path = get_root_path()
SDK_PORT = 32717

# port
SDK_HTTP_PORT = '32717'
SDK_RTMP_PORT = '32718'
SDK_DASHBOARD_PORT = '32719'


# ROOT_USER = "root"
# ROOT_PASSWD = "Yunshang2014"
ROOT_USER = 'root'
ROOT_PASSWORD = 'root'

SDK_FILE = "ys_service_static"
PCAP_FILE = "sdk.pcap"
LOG_FILE = "result_log.txt"
LOG_FILE = 'NetworkMonitor.log'
CORE_FILE = 'core.*'


LOCAL_SDK = root_path + "/misc/sdk/daily_sdk_api/{0}".format(SDK_FILE)
LOCAL_PCAP = root_path + "/misc/sdk/daily_sdk_api/{0}".format(PCAP_FILE)
LOCAL_LOG_FILE = root_path + "/misc/sdk/daily_sdk_api/{0}".format(LOG_FILE)
RESULT_PATH = root_path + "/result/"

REMOTE_ETH = "eth0"
REMOTE_ROOT_PATH = "/root"
REMOTE_CHECK_PYTHON_FILE = REMOTE_ROOT_PATH + "/sdk_request_check.py"
REMOTE_SDK_API_PATH = "/root/sdk_api"
REMOTE_SDK_PATH = REMOTE_SDK_API_PATH + "/sdk"
REMOTE_SDK = REMOTE_SDK_PATH + "/{0}".format(SDK_FILE)
REMOTE_PCAP = REMOTE_SDK_API_PATH + "/" + PCAP_FILE
REMOTE_LOG_FILE = REMOTE_ROOT_PATH + "/" + LOG_FILE

# REMOTE_SDK_IP = "10.6.3.28"
REMOTE_SDK_IP = '192.168.4.195'
# REMOTE_SDK_IP = '192.168.2.59'

LOGIN_REQUEST_PATTERN = re.compile('/session/peers/[0123456789ABCDEF]{32}$')

# dashboard url
VERSION_DASHBOARD_URL = '/ajax/version'
LOGIN_DASHBOARD_URL = '/ajax/login'
CONF_DASHBOARD_URL = '/ajax/conf'

# peer_id
PEER_ID_MORE_THAN_32BITS = '00000004C10F48719E4A207D2CDA06C0A3432'
PEER_ID_LESS_THAN_32_BITS = '00000004C10F48719E4A2'
PEER_ID_NOT_HEX_STRING = 'W0000000SSXABDD10F48719E4A2DCFE1'
PEER_ID_ALL_ZERO = '0'*32
USER_PREFIX = '00001234'

# login
EXPECT_STUN_IP = u'192.168.3.201'
EXPECT_NATTYPE = 3
EXPECT_PUBLICIP = u"192.168.3.1"
EXPECT_PRIVATEIP = u"192.168.121.14"
EXPECT_DEVICEINFO = {}
DROP_TCP = 'iptables -I OUTPUT -d ts.cloutropy.com -j DROP'
RECOVER_TCP = 'iptables -F'

# play_live
PLAY_URL = 'live_flv/user/xmtv?url=http://pl8.live.panda.tv/live_panda/a81147d7f2f1cf8d46a7daef1e636fc5.flv'
PLAY_URL_1 = 'live_flv/user/xmtv?url=http://pl8.live.panda.tv/live_panda/012192e6277f7da070480d8ee32648fd.flv'
PLAY_URL_CHANNEL_NOT_EXIST = 'live_flv/user/xmtv?url=http://pl8.live.panda.tv/live_panda/012192e6277f113dfadfaff.flv'
PLAY_URL_INVALID_PREFIX_AND_USER = 'live_flv/user/xm?url=http://pl8.live.tv/live_panda/012192e6277f113dfadfaff.flv'
PLAY_URL_DOMAIN_NOT_EXIST = 'live_flv/user/xmtv?url=http://pl8.live.tv/live_panda/012192e6277f7da070480d8ee32648fd.flv'
PLAY_URL_INVALID_USER = 'live_flv/user/xm?url=http://pl8.live.panda.tv/live_panda/012192e6277f7da070480d8ee32648fd.flv'

CHECK_CORE_DUMP_TIME = 30
