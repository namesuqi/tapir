# coding=utf-8
# DCCP protocol

PROTOCOL_HEAD_DCCP = "d1"

PROTOCOL_DCCP_SYNC = 1
PROTOCOL_DCCP_SYNACK = 2
PROTOCOL_DCCP_DATA = 3
PROTOCOL_DCCP_ACK = 4
PROTOCOL_DCCP_FIN = 5


class PROTOCOL_DCCP_HEAD_STRUCT():
    def __init__(self):
        self.protocol_type = ""
        self.protocol_opt = 0
        self.protocol_iack = 0
        self.protocol_rsv = 0
        self.protocol_sub_type = 0
        self.protocol_win_size = ""
        self.protocol_timestamp = 0
        self.protocol_time_delay = 0
        self.protocol_seqno = 0
        self.protocol_ackno = 0
        self.protocol_data = None


class PROTOCOL_DCCP_SYNC_STRUCT():
    def __init__(self):
        self.data_peerid = ""


class PROTOCOL_DCCP_SYNACK_STRUCT():
    def __init__(self):
        self.data_peerid = ""
        self.data_code = 0


class PROTOCOL_DCCP_DATA_STRUCT():
    def __init__(self):
        self.data_cccp_obj = None


class PROTOCOL_DCCP_ACK_STRUCT():
    def __init__(self):
        self.data_whyack = 0


class PROTOCOL_DCCP_FIN_STRUCT():
    def __init__(self):
        self.data_code = 0

