# coding=utf-8
# sdk api test case
import unittest
import time
from lib.common.decorator import *
from lib.sdk.pcap_http_checker import *
from lib.sdk.pcap_controller import *
from lib.sdk.sdk_controller import *
from lib.sdk.sdk_constant import *


class TestLoginApi(unittest.TestCase):

    @func_doc
    def testGroupResultCollect(self):
        """
        deploy & run sdk & sdk_request_checker & player
        then download log file to misc/sdk/daily_sdk_api

        sdk_api
        @owner: guzehao
        """
        deploy_sdk(REMOTE_SDK_IP)
        transfer_exec_files(REMOTE_SDK_IP)
        stop_sdk(REMOTE_SDK_IP)
        start_sdk_check(960)
        start_sdk()
        time.sleep(630)
        start_sdk_live_flv(REMOTE_SDK_IP)
        time.sleep(330)
        transfer_check_log_file(REMOTE_SDK_IP)
        stop_sdk(REMOTE_SDK_IP)

    @func_doc
    def testPeerLogin(self):
        """
        verify result_log_txt has peer login topic
        sdk_api
        @owner: guzehao
        """
        result = verify_log_file_result(LOCAL_LOG_FILE, 'Peer Login')
        self.assertTrue(result, 'can not find peer login topic in result_log.txt')

    @func_doc
    def testPeerLogout(self):
        """
        verify result_log_txt has peer logout topic
        sdk_api
        @owner: guzehao
        """
        result = verify_log_file_result(LOCAL_LOG_FILE, 'Peer Logout')
        self.assertTrue(result, 'can not find peer logout topic in result_log.txt')

    @func_doc
    def testPeerHeartBeat(self):
        """
        verify result_log_txt has peer heartbeat topic
        sdk_api
        @owner: guzehao
        """
        result = verify_log_file_result(LOCAL_LOG_FILE, 'Peer Heart Beat')
        self.assertTrue(result, 'can not find peer heartbeat topic in result_log.txt')

    @func_doc
    def testPeerReportlsm(self):
        """
        verify result_log_txt has peer report lsm topic
        sdk_api
        @owner: guzehao
        """
        result = verify_log_file_result(LOCAL_LOG_FILE, 'Peer Report LSM')
        self.assertTrue(result, 'can not find peer report lsm topic in result_log.txt')

    @func_doc
    def testPeerGetTask(self):
        """
        verify result_log_txt has peer get task topic
        sdk_api
        @owner: guzehao
        """
        result = verify_log_file_result(LOCAL_LOG_FILE, 'Peer Get Task')
        self.assertTrue(result, 'can not find peer get task topic in result_log.txt')

    @func_doc
    def testPeerStartLiveFlv(self):
        """
        verify result_log_txt has peer start live topic
        sdk_api
        @owner: guzehao
        """
        result = verify_log_file_result(LOCAL_LOG_FILE, 'Peer Start Live Flv')
        self.assertTrue(result, 'can not find peer start live flv topic in result_log.txt')

    @func_doc
    def testPeerGetLiveSeeds(self):
        """
        verify result_log_txt has peer get live topic
        sdk_api
        @owner: guzehao
        """
        result = verify_log_file_result(LOCAL_LOG_FILE, 'Peer Get Live seeds')
        self.assertTrue(result, 'can not find peer get live seeds topic in result_log.txt')

    @func_doc
    def testPeerBussinessReport(self):
        """
        verify result_log_txt has peer business report topic
        sdk_api
        @owner: guzehao
        """
        result = verify_log_file_result(LOCAL_LOG_FILE, 'Peer Business Report')
        self.assertTrue(result, 'can not find peer business report topic in result_log.txt')

    @func_doc
    def testPeerControlReport(self):
        """
        verify result_log_txt has peer control report topic
        sdk_api
        @owner: guzehao
        """
        result = verify_log_file_result(LOCAL_LOG_FILE, 'Peer Control Report')
        self.assertTrue(result, 'can not find peer control report topic in result_log.txt')

    @func_doc
    def testPeerErrorReport(self):
        """
        verify result_log_txt has peer error topic
        sdk_api
        @owner: guzehao
        """
        result = verify_log_file_result(LOCAL_LOG_FILE, 'Peer Error Report')
        self.assertTrue(result, 'can not find peer error report topic in result_log.txt')

    @func_doc
    def testPeerStatisticReport(self):
        """
        verify result_log_txt has peer statistic topic
        sdk_api
        @owner:guzehao
        """
        result = verify_log_file_result(LOCAL_LOG_FILE, 'Peer Statistic Report')
        self.assertTrue(result, 'can not find peer statistic topic in result_log.txt')


if __name__ == '__main__':
    # unittest.main()
    suite = unittest.TestSuite()
    suite.addTest(TestLoginApi("testGroupResultCollect"))
    suite.addTest(TestLoginApi("testPeerLogin"))
    suite.addTest(TestLoginApi("testPeerLogout"))
    suite.addTest(TestLoginApi("testPeerHeartBeat"))
    suite.addTest(TestLoginApi("testPeerReportlsm"))
    suite.addTest(TestLoginApi("testPeerGetTask"))
    suite.addTest(TestLoginApi("testPeerStartLiveFlv"))
    suite.addTest(TestLoginApi("testPeerGetLiveSeeds"))
    suite.addTest(TestLoginApi("testPeerBussinessReport"))
    suite.addTest(TestLoginApi("testPeerControlReport"))
    suite.addTest(TestLoginApi("testPeerErrorReport"))
    suite.addTest(TestLoginApi("testPeerStatisticReport"))
    runner = unittest.TextTestRunner()
    runner.run(suite)
