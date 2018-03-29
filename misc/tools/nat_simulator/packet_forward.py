# coding=utf-8
# author: Sun XiaoLei
# 本程序运行在NAT机器上
# 转发规则的具体实现
"""
ForwardToOutside: dst_ip(外部SDK), self.mock_ip(NAT，本机), src_ip(内部SDK), dst_port, self.mock_port, src_port
ForwardToInside: src_ip(外部SDK), dst_ip(NAT，本机), mock_ip(内部SDK), src_port, dst_port, mock_port

"""

import dpkt
import binascii
import threading
import global_var as glbv

from scapy.all import *
from nat_logger import NATLogger
from packet_catch import PacketCatch

n_logger = NATLogger()
UDP_PROTOCOL_TYPE = 17
TCP_PROTOCOL_TYPE = 6


class ForwardToOutside(PacketCatch):
    thread_name_index = 1

    def __init__(self, nat_type, thread_name, network_card_name, src_ip, dst_ip, mock_ip, src_port, dst_port,
                 mock_port):
        super(ForwardToOutside, self).__init__(thread_name, src_ip, dst_ip, mock_ip, src_port, dst_port, mock_port)
        self.nat_type = nat_type
        self.network_card_name = network_card_name
        self.protocol_type = 0
        self.out_in_route = {}          # 存放switch_params_tuple
        self.mock_ports = []            # 存放已用的mock port
        self.nat_mapping_list = []      # 存放已用路径键

    def run_task(self):
        self.packet_sniffer(self.network_card_name, is_source=True)

    def filter_packet(self, p_time, p_data, is_source):
        """
        过滤包
        :param p_time:
        :param p_data:
        :param is_source:
        :return:
        """
        # judge net mold
        if glbv.PRI_NET_MOLD == "ETH":
            unpack_data = dpkt.ethernet.Ethernet(p_data)
        elif glbv.PRI_NET_MOLD == "PPP":
            unpack_data = dpkt.ethernet.Ethernet(p_data[2:])
        else:
            raise Exception("PRI_NET_MOLD TYPE %s IS NOT SUPPORT!" % glbv.PRI_NET_MOLD)

        # 对非UDP的包不感兴趣
        if unpack_data.data.p != UDP_PROTOCOL_TYPE:
            return None
        # 设置类型为UDP
        self.protocol_type = unpack_data.data.p

        result = parse_ip_port(unpack_data.data)
        if result is None:
            return None
        else:
            src_ip, dst_ip, src_port, dst_port = result

        # 如果是本机出去的包，且端口大于1024
        if src_ip.find(self.src_ip) > -1 and dst_ip.find(self.src_ip) == -1 and src_port > 1024:
            self.src_ip = src_ip
            self.dst_ip = dst_ip
            self.dst_port = dst_port
            self.src_port = src_port
            if self.nat_type == "1" or self.nat_type == "2" or self.nat_type == "3":
                # corn nat
                nat_route_key = (src_ip, src_port)
            elif self.nat_type == "3.5":
                # 3.5 nat, present to hiwifi
                nat_route_key = (src_ip, src_port, dst_ip)
            elif self.nat_type == "4":
                # symmetric nat
                nat_route_key = (src_ip, src_port, dst_ip, dst_port)
            else:
                raise Exception("NAT TYPE %s IS NOT SUPPORT!" % self.nat_type)

            if nat_route_key not in glbv.NAT_ROUTE_DICT.keys():
                glbv.NAT_ROUTE_DICT[nat_route_key] = []
            # store info of nat 2
            if self.nat_type == "2":
                if dst_ip not in glbv.NAT_ROUTE_DICT[nat_route_key]:
                    glbv.NAT_ROUTE_DICT[nat_route_key].append(dst_ip)
            # store info of nat 3 | 3.5 | 4
            elif self.nat_type == "3" or self.nat_type == "3.5" or self.nat_type == "4":
                if (dst_ip, dst_port) not in glbv.NAT_ROUTE_DICT[nat_route_key]:
                    glbv.NAT_ROUTE_DICT[nat_route_key].append((dst_ip, dst_port))

            # switch params for receive thread
            # 等价于
            switch_params_tuple = (dst_ip, self.mock_ip, src_ip, dst_port, self.mock_port, src_port)

            # 如果还不在已经记录的路径里面，就需要新起一个线程来监听这条路径进来的数据
            if switch_params_tuple not in self.out_in_route.keys():
                if nat_route_key not in self.nat_mapping_list:
                    if self.nat_type == "4":   # 新起一个mock port，是最大的mock port+1
                        if self.mock_port in self.mock_ports:
                            self.mock_port = self.mock_ports[-1] + 1
                            self.mock_ports.append(self.mock_port)
                            switch_params_tuple = (dst_ip, self.mock_ip, src_ip, dst_port, self.mock_port, src_port)
                        else:
                            self.mock_ports.append(self.mock_port)  # 只有第一次能走到这里
                    self.out_in_route[switch_params_tuple] = p_time
                    self.nat_mapping_list.append(nat_route_key)

                    # 准备新起一个线程处理该路径进来的数据包
                    thread_name = "in_forward_" + str(self.__class__.thread_name_index)
                    self.__class__.thread_name_index += 1
                    temp_in_bridge = ForwardToInside(self.nat_type, thread_name, glbv.PUB_NET_CARD,
                                                     *switch_params_tuple)
                    temp_in_thread = threading.Thread(target=temp_in_bridge.run_task, name=temp_in_bridge.thread_name)
                    temp_in_thread.setDaemon(True)
                    temp_in_thread.start()
                    glbv.G_THREAD_POOL.append(temp_in_thread)
                    n_logger.log(
                        "%s log: create OUT_TO_IN tunnel thread, info: %s ." % (
                            self.get_log_time()[1], ", ".join([str(x) for x in switch_params_tuple]))
                    )
            return unpack_data.data
        else:
            return None

    def forward_packet(self, target_data):
        if self.t_data is None:
            if glbv.IS_MODIFY_DATA:
                print "DO NOR MODIFY DATA, SEND ORIGINAL DATA..."
            self.t_data = target_data.data.data
        if self.protocol_type == UDP_PROTOCOL_TYPE:
            tmp_protocol_str = "UDP"
            mock_packet = IP(src=self.mock_ip, dst=self.dst_ip) / UDP(sport=self.mock_port,
                                                                      dport=self.dst_port) / self.t_data
        elif self.protocol_type == TCP_PROTOCOL_TYPE:  # tcp data is not support
            tmp_protocol_str = "TCP"
            mock_packet = IP(src=self.mock_ip, dst=self.dst_ip) / TCP(sport=self.mock_port,
                                                                      dport=self.dst_port) / target_data.data.data
        send(mock_packet)
        n_logger.log(
            "%s log[protocl: %s]: forward to OUTside(src: (%s, %s)): (%s, %s) --> (%s, %s), packet: %s [after: %s]" % (
                self.get_log_time()[1], tmp_protocol_str, self.dst_ip, str(self.dst_port), self.src_ip,
                str(self.src_port), self.mock_ip, str(self.mock_port), binascii.b2a_hex(target_data.data.data),
                binascii.b2a_hex(self.t_data))
        )
        self.t_data = None


class ForwardToInside(PacketCatch):
    def __init__(self, nat_type, thread_name, network_card_name, src_ip, dst_ip, mock_ip, src_port, dst_port,
                 mock_port):
        super(ForwardToInside, self).__init__(thread_name, src_ip, dst_ip, mock_ip, src_port, dst_port, mock_port)
        self.nat_type = nat_type
        self.network_card_name = network_card_name
        self.protocol_type = 0

    def run_task(self):
        self.packet_sniffer(self.network_card_name, is_source=False)

    def filter_packet(self, p_time, p_data, is_source):
        is_forward = False
        unpack_data = dpkt.ethernet.Ethernet(p_data)
        if unpack_data.data.p != UDP_PROTOCOL_TYPE:
            return None
        # set value
        self.protocol_type = unpack_data.data.p
        result = parse_ip_port(unpack_data.data)
        if result is None:
            return None
        else:
            src_ip, dst_ip, src_port, dst_port = result

        # logic operate
        if self.nat_type == "1":
            # 如果类型1，目的IP,PORT符合，转发至SDK
            if dst_ip == self.dst_ip and dst_port == self.dst_port:
                is_forward = True
        elif self.nat_type == "2":
            # 如果类型2，目的IP,PORT符合，且源是当初被发送出去过的目的IP，转发至SDK
            if dst_ip == self.dst_ip and dst_port == self.dst_port and \
                            src_ip in glbv.NAT_ROUTE_DICT[(self.mock_ip, self.mock_port)]:
                is_forward = True
        elif self.nat_type == "3":
            # 如果类型3，目的IP,PORT符合，且源是当初被发送出去过的目的IP,PORT，转发至SDK
            if dst_ip == self.dst_ip and dst_port == self.dst_port and \
                            (src_ip, src_port) in glbv.NAT_ROUTE_DICT[(self.mock_ip, self.mock_port)]:
                is_forward = True
        elif self.nat_type == "3.5":
            if dst_ip == self.dst_ip and dst_port == self.dst_port and \
                            (src_ip, src_port) in glbv.NAT_ROUTE_DICT[(self.mock_ip, self.mock_port, src_ip)]:
                is_forward = True
        elif self.nat_type == "4":
            # 如果类型3，目的IP, PORT符合，且源是当初被发送出去过的目的IP, PORT，转发至SDK
            if dst_ip == self.dst_ip and dst_port == self.dst_port and \
                            (src_ip, src_port) in glbv.NAT_ROUTE_DICT[(self.mock_ip, self.mock_port, src_ip, src_port)]:
                is_forward = True
        else:
            raise Exception("NAT TYPE %s IS NOT SUPPORT! " % self.nat_type)
        if is_forward:
            self.src_ip = src_ip
            self.src_port = src_port
            return unpack_data.data
        else:
            return None

    def forward_packet(self, target_data):
        if self.t_data is None:
            if glbv.IS_MODIFY_DATA:
                print "no change data, send original data ......"
            self.t_data = target_data.data.data
        if self.protocol_type == UDP_PROTOCOL_TYPE:  # 现在只支持UDP
            tmp_protocol_str = "UDP"
            mock_packet = IP(src=self.src_ip, dst=self.mock_ip) / UDP(sport=self.src_port,
                                                                      dport=self.mock_port) / self.t_data
        elif self.protocol_type == TCP_PROTOCOL_TYPE:  # tcp data is not support
            tmp_protocol_str = "TCP"
            mock_packet = IP(src=self.src_ip, dst=self.mock_ip) / TCP(sport=self.src_port,
                                                                      dport=self.mock_port) / target_data.data.data
        send(mock_packet)
        n_logger.log(
            "%s log[protocl: %s]: forward to INside(src: (%s, %s)): (%s, %s) --> (%s, %s), packet: %s [after: %s]" % (
                self.get_log_time()[1], tmp_protocol_str, self.dst_ip, str(self.dst_port), self.src_ip,
                str(self.src_port), self.mock_ip, str(self.mock_port), binascii.b2a_hex(target_data.data.data),
                binascii.b2a_hex(self.t_data))
        )
        self.t_data = None


def parse_ip_port(data):
    src_ip_tuple = tuple(map(ord, list(data.src)))
    dst_ip_tuple = tuple(map(ord, list(data.dst)))
    if len(src_ip_tuple) != 4 and len(dst_ip_tuple) != 4:
        return None
    else:
        src_ip = '%d.%d.%d.%d' % src_ip_tuple
        dst_ip = '%d.%d.%d.%d' % dst_ip_tuple
        src_port = data.data.sport
        dst_port = data.data.dport
        return src_ip, dst_ip, src_port, dst_port
