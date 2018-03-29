# coding=utf-8
# linux sdk play_live testcase

import unittest
from lib.sdk.common_tool.sdk_handle import *
from lib.sdk.sdk_constant import *
from lib.common.decorator import *
from lib.sdk.common_tool.specific_handle import *


class TestPlayLive(unittest.TestCase):
    @func_doc
    def setUp(self):
        """
        上传sdk，使用ys_service_static版本
        """
        remove_file(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD, REMOTE_SDK_API_PATH, LOG_FILE)
        upload_sdk(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD, REMOTE_SDK_PATH)

    @func_doc
    def tearDown(self):
        """
        移除sdk
        """
        stop_sdk(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD)
        remove_sdk(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD, REMOTE_SDK_PATH)

    @func_doc
    def test_Play_Multi_Channel(self):
        """
        testlink tc-631
        摘要
        使用一个SDK播放两个以上不同的频道，播放三个小时，SDK不会crash
        @owner: jinyifan
        """
        start_sdk(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD, REMOTE_SDK_PATH)
        time.sleep(3)
        play(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD, REMOTE_SDK_API_PATH, PLAY_URL)
        play(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD, REMOTE_SDK_API_PATH, PLAY_URL_1)

        # check if core.* file exists
        time.sleep(3 * 60 * 60)
        result = find_coredump(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD, REMOTE_SDK_API_PATH)
        self.assertEqual(result, -1, "SDK crash")

    @func_doc
    def test_Play_LiveChannel_DomainNotExist(self):
        """
        testlink tc-610
        摘要
        SDK请求播放域名不存在的频道时，不会crash
        @owner: jinyifan
        """
        start_sdk(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD, REMOTE_SDK_PATH)
        time.sleep(3)
        play(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD, REMOTE_SDK_API_PATH, PLAY_URL_DOMAIN_NOT_EXIST)

        # check if core.* file exists
        time.sleep(CHECK_CORE_DUMP_TIME)
        result = find_coredump(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD, REMOTE_SDK_API_PATH)
        self.assertEqual(result, -1, "SDK crash")

    @func_doc
    def test_Play_LiveChannel_InvalidUser(self):
        """
        testlink tc-170
        摘要
        SDK请求播放用户名无效的频道时，不会crash
        @owner: jinyifan
        """
        start_sdk(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD, REMOTE_SDK_PATH)
        time.sleep(3)
        play(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD, REMOTE_SDK_API_PATH, PLAY_URL_INVALID_USER)

        # check if core.* file exists
        time.sleep(CHECK_CORE_DUMP_TIME)
        result = find_coredump(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD, REMOTE_SDK_API_PATH)
        self.assertEqual(result, -1, "SDK crash")

    @func_doc
    def test_Play_LiveChannel_ChannelNotExist(self):
        """
        testlink tc-172
        摘要
        SDK请求播放不存在的频道时，不会crash
        @owner: jinyifan
        """
        start_sdk(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD, REMOTE_SDK_PATH)
        time.sleep(3)
        play(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD, REMOTE_SDK_API_PATH, PLAY_URL_CHANNEL_NOT_EXIST)

        # check if core.* file exists
        time.sleep(CHECK_CORE_DUMP_TIME)
        result = find_coredump(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD, REMOTE_SDK_API_PATH)
        self.assertEqual(result, -1, "SDK crash")

    @func_doc
    def test_Play_LiveChannel_InvalidPrefixAndUser(self):
        """
        testlink tc-174
        摘要
        SDK请求播放用户名和url_perfix均无效的频道时，不会crash
        @owner: jinyifan
        """
        start_sdk(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD, REMOTE_SDK_PATH)
        time.sleep(3)
        play(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD, REMOTE_SDK_API_PATH, PLAY_URL_INVALID_PREFIX_AND_USER)

        # check if core.* file exists
        time.sleep(CHECK_CORE_DUMP_TIME)
        result = find_coredump(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD, REMOTE_SDK_API_PATH)
        self.assertEqual(result, -1, "SDK crash")


if __name__ == '__main__':
    unittest.main()
