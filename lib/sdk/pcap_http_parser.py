# coding=utf-8
# author: zengyuetian
# Parse *.pcap file to get http request information

import dpkt


def parse_http_requests(pcap_file):
    """
    parse *.pcap file to get http requests
    :param pcap_file: pcap file
    :return: requests
    """
    parser = PcapHttpParser(pcap_file)
    http_requests = parser.get_http_requests(80)
    return http_requests


class PcapHttpParser(object):
    def __init__(self, pcap_file):
        self.f = open(pcap_file, 'rb')
        self.pcap = dpkt.pcap.Reader(self.f)

    def __del__(self):
        self.f.close()

    def get_http_requests(self, dport=80):
        """
        get http requests
        :param dport: dest port
        :return: http requests object list
        """
        http_requests = []
        for ts, buf in self.pcap:
            try:
                eth = dpkt.ethernet.Ethernet(buf)
                ip = eth.data
                tcp = ip.data

                if tcp.dport == dport and len(tcp.data) > 0:
                    http = dpkt.http.Request(tcp.data)
                    http_requests.append(http)
            except Exception:
                # print "issue", e.message
                continue
        return http_requests



