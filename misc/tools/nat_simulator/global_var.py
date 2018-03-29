# coding=utf-8
# author: Sun XiaoLei
# 定义全局变量


# switch global variables
IS_MODIFY_DATA = False
G_IS_EXIT = False

# modify_packet_data.py
MODIFY_DATA_NOT_RANDOM = True
MODIFY_DATA_POSITION = 1
MODIFY_DATA_OPERATOR = "&"
MODIFY_DATA_OPERATE_DATA = 15
MODIFY_DATA_COUNT = 1
MODIFY_DATA_CONTAIN = []

# record info global variables
# file packet_forward.py
PRI_NET_MOLD = "ETH"

NAT_ROUTE_DICT = {}
G_THREAD_POOL = []

# file nat_simulator.py
MOCK_GW_PORT = 12321
# default nat type
DUMMY_NAT_TYPE = "1"
G_COUNT_INDEX = 0

# PRI_NET_RANGE just use once time
PRI_NET_RANGE = "192.168.201."
PRI_NET_CARD = "eth2"

# PUB_GW_HOST_IP -> NAT ip
# 网关机器, 做NAT机器的IP地址, PEER和SEED机器上的这个配置是不同的
PUB_GW_HOST_IP = "192.168.4.196"
# PUB_GW_HOST_IP = "192.168.4.197"


# PUB_NET_CARD -> NAT network card
PUB_NET_CARD = "eth1"

PENE_DISTINGUISH = 'a1'
DCCP_DISTINGUISH = 'd1'
