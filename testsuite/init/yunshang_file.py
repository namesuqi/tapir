# coding=utf-8
# __author__ = 'jinyifan'
# linux sdk init - yunshang file

import unittest
from lib.sdk.common_tool.sdk_handle import *
from lib.sdk.common_tool.specific_handle import *
from lib.sdk.common_tool.verify_handle import *
from lib.sdk.sdk_constant import *
from lib.common.decorator import *


class TestYunshangFile(unittest.TestCase):
    @func_doc
    def setUp(self):
        """
        上传sdk，使用ys_service_static版本
        """
        remove_sdk(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD, REMOTE_SDK_PATH)
        upload_sdk(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD, REMOTE_SDK_PATH)

    @func_doc
    def tearDown(self):
        """
        移除sdk
        """
        stop_sdk(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD)
        remove_sdk(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD, REMOTE_SDK_PATH)

    @func_doc
    def testInitYunshangFile(self):
        """
        testlink tc-572
        SDK启动时能生产yunshang文件夹，配置，数据文件
        @owner: jinyifan
        """
        start_sdk(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD, REMOTE_SDK_PATH)
        time.sleep(2)
        # 检查文件夹
        exists = verify_file_is_exist(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD, REMOTE_SDK_PATH, 'yunshang')
        self.assertTrue(exists, "yunshang folder not exist")

        # 检查配置文件和数据文件
        exists = verify_file_is_exist(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD, REMOTE_SDK_PATH,
                                      'yunshang.conf', 'yunshang.meta')
        self.assertTrue(exists, "conf or meta file is not in yunshang folder")

    @func_doc
    def testDeleteYunshangFile(self):
        """
        testlink tc-573
        SDK运行过程中删除yunshang文件夹，再启动SDK能重新生成yunshang文件夹
        @owner: jinyifan
        """
        start_sdk(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD, REMOTE_SDK_PATH)
        time.sleep(2)
        # 删除文件夹，验证文件夹不存在
        remove_sdk(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD, REMOTE_SDK_PATH, 'yunshang')
        exists = verify_file_is_exist(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD, REMOTE_SDK_PATH, 'yunshang')
        self.assertFalse(exists, "yunshang folder is still exist")

        # 重新启动SDK，验证文件夹重新生成
        stop_sdk(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD)
        start_sdk(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD, REMOTE_SDK_PATH)
        exists = verify_file_is_exist(REMOTE_SDK_IP, ROOT_USER, ROOT_PASSWORD, REMOTE_SDK_PATH, 'yunshang')
        self.assertTrue(exists, "yunshang folder should rebuild")


if __name__ == '__main__':
    unittest.main()
