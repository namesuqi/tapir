

import unittest
from lib.sdk.sdk_controller import *
from lib.sdk.pcap_http_parser import *

class TestBusinessReport(unittest.TestCase):

    def setUp(self):
        # deploy_sdk(REMOTE_SDK_IP)
        pass


    def tearDown(self):
        pass

    def testControlPlaneHttpDns(self):
        copy_file_from('192.168.4.195', 'root', 'root', '/root/sdk_api/sdk/business_report.pcap', 'E:/git_code/tapir/misc/business_report.pcap')
        print len(parse_http_requests('E:/git_code/tapir/misc/business_report.pcap'))


if __name__ == '__main__':
    unittest.main()
