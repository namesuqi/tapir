import unittest
import time

from lib.sdk.penetrate.pene_constant import *
from lib.sdk.common_tool.sdk_handle import upload_sdk, start_sdk, stop_sdk
from lib.sdk.penetrate.pene_lib import start_nat_simulator, stop_nat_simulator, check_sdk_login, check_sdk_nat_type, \
    mock_ts_info, start_sdk_play, check_penetrate_log_steps, remove_sdk_yunshang

WAIT_TIME = 3
PLAY_TIME = 15


class TestPenetrate(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """
        upload new sdk of misc/sdk/daily_routine/
        :return:
        """
        upload_sdk(SEND_SDK_IP, ADMIN_USERNAME, ADMIN_PWD, REMOTE_SDK_PATH)
        upload_sdk(RECEIVE_SDK_IP, ADMIN_USERNAME, ADMIN_PWD, REMOTE_SDK_PATH)

        # upload to update nat_simulator then manual modify global_var.py
        # upload_nat_simulator(SEND_NAT_IP, REMOTE_SIMULATOR_PATH)
        # upload_nat_simulator(RECEIVE_NAT_IP, REMOTE_SIMULATOR_PATH)

    def setUp(self):
        """
        remove dir yunshang to change peer_id
        :return:
        """
        remove_sdk_yunshang(SEND_SDK_IP)
        remove_sdk_yunshang(RECEIVE_SDK_IP)

    def tearDown(self):
        """
        stop sdk & simulator
        :return:
        """
        stop_sdk(SEND_SDK_IP, ADMIN_USERNAME, ADMIN_PWD)
        stop_sdk(RECEIVE_SDK_IP, ADMIN_USERNAME, ADMIN_PWD)
        stop_nat_simulator(SEND_NAT_IP)
        stop_nat_simulator(RECEIVE_NAT_IP)
        time.sleep(WAIT_TIME)

    def test_nat_1to1(self):
        self._penetrate_test_process(send_nat_type='1', receive_nat_type='1')

    def test_nat_1to2(self):
        self._penetrate_test_process(send_nat_type='1', receive_nat_type='2')

    def test_nat_1to3(self):
        self._penetrate_test_process(send_nat_type='1', receive_nat_type='3')

    def test_nat_1to4(self):
        self._penetrate_test_process(send_nat_type='1', receive_nat_type='4')

    def test_nat_2to1(self):
        self._penetrate_test_process(send_nat_type='2', receive_nat_type='1')

    def test_nat_2to2(self):
        self._penetrate_test_process(send_nat_type='2', receive_nat_type='2')

    def test_nat_2to3(self):
        self._penetrate_test_process(send_nat_type='2', receive_nat_type='3')

    def test_nat_2to4(self):
        self._penetrate_test_process(send_nat_type='2', receive_nat_type='4')

    def test_nat_3to1(self):
        self._penetrate_test_process(send_nat_type='3', receive_nat_type='1')

    def test_nat_3to2(self):
        self._penetrate_test_process(send_nat_type='3', receive_nat_type='2')

    def test_nat_3to3(self):
        self._penetrate_test_process(send_nat_type='3', receive_nat_type='3')

    @unittest.expectedFailure
    def test_nat_3to4(self):
        self._penetrate_test_process(send_nat_type='3', receive_nat_type='4')

    def test_nat_4to1(self):
        self._penetrate_test_process(send_nat_type='4', receive_nat_type='1')

    def test_nat_4to2(self):
        self._penetrate_test_process(send_nat_type='4', receive_nat_type='2')

    @unittest.expectedFailure
    def test_nat_4to3(self):
        self._penetrate_test_process(send_nat_type='4', receive_nat_type='3')

    @unittest.expectedFailure
    def test_nat_4to4(self):
        self._penetrate_test_process(send_nat_type='4', receive_nat_type='4')

    def _penetrate_test_process(self, send_nat_type, receive_nat_type):
        """
        penetrate test common steps
        :param send_nat_type: play sdk NAT type
        :param receive_nat_type: seed sdk NAT type
        :return: PASS or FAIL
        """
        start_nat_simulator(SEND_NAT_IP, send_nat_type)
        start_nat_simulator(RECEIVE_NAT_IP, receive_nat_type)
        time.sleep(WAIT_TIME)
        start_sdk(SEND_SDK_IP, ADMIN_USERNAME, ADMIN_PWD, REMOTE_SDK_PATH)
        start_sdk(RECEIVE_SDK_IP, ADMIN_USERNAME, ADMIN_PWD, REMOTE_SDK_PATH)
        self.assertTrue(check_sdk_login(SEND_SDK_IP), "send sdk login fail")
        self.assertTrue(check_sdk_login(RECEIVE_SDK_IP), "receive sdk login fail")
        self.assertTrue(check_sdk_nat_type(SEND_SDK_IP, send_nat_type), "send sdk nat type error")
        self.assertTrue(check_sdk_nat_type(RECEIVE_SDK_IP, receive_nat_type), "receive sdk nat type error")
        self.assertTrue(mock_ts_info(RECEIVE_SDK_IP), "mock get seeds fail")
        time.sleep(WAIT_TIME)
        self.assertTrue(start_sdk_play(SEND_SDK_IP), "sdk play fail")
        time.sleep(PLAY_TIME)
        self.assertTrue(
            check_penetrate_log_steps(send_nat_ip=SEND_NAT_IP, receive_nat_ip=RECEIVE_NAT_IP, send_nat_type=send_nat_type),
            "check log fail")


if __name__ == '__main__':
    # test_suite = unittest.TestSuite()
    # tc = ['test_nat_1to3', 'test_nat_1to4']
    # test_suite.addTests(map(TestPenetrate, tc))
    # runner = unittest.TextTestRunner(verbosity=2)
    # runner.run(test_suite)
    unittest.main()
