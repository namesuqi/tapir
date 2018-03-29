#!/usr/bin/env python
# coding: utf-8
import pcapy
import socket
import binascii
import dpkt
import sys


class NetworkMonitor:
    def __init__(self, dev):
        self._dev = dev
        pass

    def start(self, capture_tcp=False, capture_udp=False, time_out=10000):
        """Start Capture network packet
        Args:
            capture_tcp (boolean): If True, TCP Protocols packet will be capture
            capture_udp (boolean): If True, UDP Protocols packet will be capture
            time_out (int):
        Returns:
            None
        """
        p = pcapy.open_live(self._dev, 65536, True, time_out)
        local_ips = get_local_ip()
        http_100_continue = {}
        with open('NetworkMonitor.log', 'w') as writer:
            while True:
                header, data = p.next()
                eth = dpkt.ethernet.Ethernet(data)
                if not isinstance(eth.data, dpkt.ip.IP):
                    # print 'Non IP Packet type not supported %s\n' % eth.data.__class__.__name__
                    continue
                ip = eth.data
                if isinstance(ip.data, dpkt.tcp.TCP) and capture_tcp:
                    tcp = ip.data
                    try:
                        if inet_to_str(ip.src) in local_ips:
                            capture_data = dpkt.http.Request(tcp.data)
                        else:
                            capture_data = dpkt.http.Response(tcp.data)
                    except dpkt.dpkt.UnpackError:
                        # 处理 http 100 continue 的情况（分两个包发送，一包含头，一包含body）
                        eth = dpkt.ethernet.Ethernet(data)
                        ip = eth.data
                        tcp = ip.data
                        data_direction = inet_to_str(ip.src) + ' -> ' + inet_to_str(ip.dst)

                        if str(tcp.data).startswith('POST') or str(tcp.data).startswith('{"'):
                            # print tcp.data
                            if data_direction not in http_100_continue:
                                http_100_continue[data_direction] = list()
                            http_100_continue[data_direction].append(tcp.data)

                            if len(http_100_continue[data_direction]) == 2:
                                head = http_100_continue[data_direction][0].split('\r\n')
                                headers = {}
                                for i in xrange(1, len(head) - 2):
                                    key, value = head[i].split(': ')
                                    headers[key] = value
                                method = head[0].split(' ')[0]
                                uri = head[0].split(' ')[1]
                                version = head[0].split(' ')[2].split('/')[-1]
                                # print method, uri, version, headers
                                log_line = "HTTP data %s: Request(body='%s', uri='%s', headers=%s," \
                                           " version='%s', method='%s')" % (
                                                data_direction,
                                                http_100_continue[data_direction][1],
                                                uri,
                                                headers,
                                                version,
                                                method
                                            )
                                print log_line
                                writer.write(log_line)
                                writer.flush()
                                http_100_continue[data_direction] = list()
                        continue
                    except Exception:
                        # print "ERROR!"
                        continue

                    log_line = 'HTTP data %s -> %s: %s\n' % (inet_to_str(ip.src), inet_to_str(ip.dst), repr(capture_data))
                    print log_line
                    writer.write(log_line)
                    writer.flush()
                elif isinstance(ip.data, dpkt.udp.UDP) and capture_udp:
                    udp = ip.data
                    try:
                        if len(udp.data) > 0:
                            capture_udp_data = dpkt.udp.UDP(udp.data)
                        else:
                            continue
                    except (dpkt.dpkt.NeedData, dpkt.dpkt.UnpackError):
                        continue
                    log_line = "UDP data %s -> %s: sport:%s dport:%s data:%s" % (inet_to_str(ip.src),
                                                                                 inet_to_str(ip.dst),
                                                                                 capture_udp_data.sport,
                                                                                 capture_udp_data.dport,
                                                                                 binascii.b2a_hex(capture_udp_data.data))
                    print log_line
                    writer.write(log_line)
                    writer.flush()


def mac_addr(address):
    """Convert a MAC address to a readable/printable string
    Args:
       address (str): a MAC address in hex form (e.g. '\x01\x02\x03\x04\x05\x06')
    Returns:
           str: Printable/readable MAC address
    """
    return ':'.join('%02x' % ord(b) for b in address)


def inet_to_str(inet):
    """Convert inet object to a string
    Args:
        inet (inet struct): inet network address
    Returns:
        str: Printable/readable IP address
    """
    ip_info = tuple(map(ord, list(inet)))
    ip = '%d.%d.%d.%d' % ip_info
    return ip


def get_local_ip():
    """Get local ips to a list
    Returns:
        list: all IPs
    """
    myname = socket.getfqdn(socket.gethostname())
    # myaddr = socket.gethostbyname(myname)
    # print myname
    # print myaddr
    # print socket.gethostbyname_ex(myname)[2]
    ip_list = socket.gethostbyname_ex(myname)[2]
    return ip_list


if __name__ == "__main__":
    if len(sys.argv) == 2:
        arg_dev = sys.argv[1]
        eg = NetworkMonitor(arg_dev)
        eg.start(capture_tcp=True, capture_udp=False)
    elif len(sys.argv) == 4:
        arg_dev = sys.argv[1]
        arg_capture_tcp = sys.argv[2]
        arg_capture_udp = sys.argv[3]
        eg = NetworkMonitor(arg_dev)
        eg.start(capture_tcp=int(arg_capture_tcp), capture_udp=int(arg_capture_udp))
    elif len(sys.argv) == 5:
        arg_dev = sys.argv[1]
        arg_capture_tcp = sys.argv[2]
        arg_capture_udp = sys.argv[3]
        arg_time_out = sys.argv[4]
        eg = NetworkMonitor(arg_dev)
        eg.start(capture_tcp=int(arg_capture_tcp), capture_udp=int(arg_capture_udp), time_out=int(arg_time_out))
    else:
        print "params invalid!"

    # dev = pcapy.findalldevs()[2]
    # # dev = pcapy.lookupdev()
    # # dev = 'en1'
    # eg = NetworkMonitor(dev)
    # eg.start(capture_tcp=False, capture_udp=True)


