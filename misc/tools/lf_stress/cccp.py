# coding=utf-8
# CCCP protocol definition

PROTOCOL_CCCP_PUSH_STREAM_REQ = 20
PROTOCOL_CCCP_PUSH_STREAM_RSP = 21
PROTOCOL_CCCP_PUSH_PIECE_DATA = 22
PROTOCOL_CCCP_PUSH_STREAM_FIN = 23

class PROTOCOL_CCCP_HEAD_STRURCT():
    def __init__(self):
        self.protocol_type = 0
        self.protocol_data = None


class PROTOCOL_CCCP_PUSH_STREAM_REQ_STRUCT():
    def __init__(self):
        self.request_id = 0
        self.peer_id = ""
        self.file_id = ""
        self.file_url = ""
        self.cppc_number = 0


class PROTOCOL_CCCP_PUSH_STREAM_RSP_STRUCT():
    def __init__(self):
        self.request_id = 0
        self.status = 0


class PROTOCOL_CCCP_PUSH_PIECE_DATA_STRUCT():
    def __init__(self):
        self.request_id = 0
        self.chuck_id = 0
        self.piece_index = 0
        self.piece_data = 0


class PROTOCOL_CCCP_PUSH_STREAM_FIN_STRUCT():
    def __init__(self):
        self.request_id = 0
        self.file_id = ""
        self.status = 0
