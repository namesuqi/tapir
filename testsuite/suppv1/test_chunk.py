# coding=utf-8
import unittest
from lib.protocol.supp.supp_request import *
from lib.protocol.udp_tools import *
from lib.common.decorator import *


class TestChunk(unittest.TestCase):

    def tearDown(self):
        time.sleep(1)

    @func_doc
    def testChunkReqWrongChecksum(self):
        """
        checksum错误的chunk请求不会被处理
        """
        channel_id = get_random_channel_id()
        response = supp_chunk_req(channel_id, CHUNK_ID, FILE_URL_DEFAULT, SDK_VERSION_DEFAULT, WRONG_CHECKSUM)
        self.failIf(response, 'checksum错误的chunk req 不应被处理')

    @func_doc
    def testChunkReqWrongUrl(self):
        """
        file url错误的chunk请求能被正确处理
        """
        channel_id = get_random_channel_id()
        response = SUPPChunkRspStruct(supp_chunk_req(channel_id, CHUNK_ID, FILE_URL_NOT_EXIST))
        split_udp_data(response)
        self.assertEqual(response.protocol, SUPP_PROTOCOL, 'chunk rsp中的protocol字段错误')
        self.assertEqual(response.suppType, CHUNK_RSP_TYPE, 'chunk rsp中的supp type字段错误')
        self.assertEqual(response.channelId, str(hex(channel_id))[2:].rjust(4, '0'), 'chunk rsp中的channel id字段错误')
        self.assertEqual(response.chunkId, CHUNK_ID_HEX, 'chunk rsp中的channel id字段错误')
        self.assertEqual(response.code, CODE_FILE_NOT_EXIST, 'chunk rsp中的code字段错误')
        self.assertEqual(get_udp_check_sum(response), udp_checksum(response.data[0:-4]).rjust(4, '0'), 'chunk rsp中的'
                                                                                                       'checksum字段错误')
        self.assertEqual(response.length, len(response.data)*2, '长度错误')


if __name__ == '__main__':
    unittest.main()

