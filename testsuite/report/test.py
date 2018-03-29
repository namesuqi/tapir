import datetime
import dpkt

path = 'D:/test.pcap'
# path = '/business_report.pcap'


def parse_pcap(pcap):
    for timestamp, buf in pcap:

        # Unpack the Ethernet frame (mac src/dst, ethertype)
        eth = dpkt.ethernet.Ethernet(buf)

        # Make sure the Ethernet data contains an IP packet
        if not isinstance(eth.data, dpkt.ip.IP):
            print 'Non IP Packet type not supported %s\n' % eth.data.__class__.__name__
            continue

        # Now grab the data within the Ethernet frame (the IP packet)
        ip = eth.data

        # Check for TCP in the transport layer
        if isinstance(ip.data, dpkt.tcp.TCP):

            # Set the TCP data
            tcp = ip.data

            # Now see if we can parse the contents as a HTTP request
            try:
                request = dpkt.http.Request(tcp.data)
            except (dpkt.dpkt.NeedData, dpkt.dpkt.UnpackError):
                continue

            # Pull out fragment information (flags and offset all packed into off field, so use bitmasks)
            do_not_fragment = bool(ip.off & dpkt.ip.IP_DF)
            more_fragments = bool(ip.off & dpkt.ip.IP_MF)
            fragment_offset = ip.off & dpkt.ip.IP_OFFMASK

            # Print out the info
            print 'Timestamp: ', str(datetime.datetime.utcfromtimestamp(timestamp))
            # print 'Ethernet Frame: ', mac_addr(eth.src), mac_addr(eth.dst), eth.type
            # print 'IP: %s -> %s   (len=%d ttl=%d DF=%d MF=%d offset=%d)' % \
            #       (inet_to_str(ip.src), inet_to_str(ip.dst), ip.len, ip.ttl, do_not_fragment, more_fragments,
            #        fragment_offset)
            print 'HTTP request: %s\n' % repr(request)


