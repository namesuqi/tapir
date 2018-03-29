# coding=utf-8
# author: Sun XiaoLei
# 本程序运行在NAT机器上
# 主要用来获取指定网卡上的报文包
# 是转发包ForwardToOutside ForwardToInside类的父类

import pcapy
import time
import threading
import global_var as glbv

from event import Event
from modify_packet_data import ModifyPacketData


class PacketCatch(Event):
    def __init__(self, thread_name, src_ip, dst_ip, mock_ip, src_port, dst_port, mock_port):
        super(Event, self).__init__()
        self.src_ip = src_ip
        self.dst_ip = dst_ip
        self.mock_ip = mock_ip
        self.src_port = src_port
        self.dst_port = dst_port
        self.mock_port = mock_port
        self.thread_name = thread_name
        self.t_data = None
        # self._set_modify_data_event()

    def packet_sniffer(self, sniffer_card, is_source):
        """
        抓包方法，供子类调用
        :param sniffer_card:
        :param is_source: 对于子类ForwardToInside是False，对于子类ForwardToOutside是True
        :return:
        """
        # open_live方法第一个参数是要打开的设备，第二个参数是捕获数据包的大小，
        # 第三个参数是否打开混杂模式，第四个参数是等待数据包的延迟时间，该方法返回一个 pcapy对象。
        pc = pcapy.open_live(sniffer_card, 10240, True, 5000)
        while True:
            try:
                if glbv.G_IS_EXIT:
                    print "exit thread loop... sub thread %s will be exit." % threading.currentThread().getName()
                    break
                packet_time, packet_data = pc.next()
                # 如果找到满足条件的数据包，那么就进行转发
                target_data = self.filter_packet(packet_time, packet_data, is_source)
                if target_data is not None:
                    if glbv.IS_MODIFY_DATA:
                        self.notify("modify_packet_data_%s" % self.thread_name, target_data)
                    self.forward_packet(target_data)
            except Exception, e:
                # print 'packet_sniffer:', e.message
                continue

    def filter_packet(self, p_time, p_data, is_source):
        pass

    def forward_packet(self, target_data):
        pass

    def _set_modify_data_event(self):
        event_handle_obj = ModifyPacketData("modify_packet_data_%s" % self.thread_name, self)
        self.register("modify_packet_data_%s" % self.thread_name, event_handle_obj.event_handle)

    @staticmethod
    def get_log_time():
        temp_timestamp = time.time()
        ret_str = time.strftime("%H:%M:%S", time.localtime(temp_timestamp))
        ret_str += str("%.3f" % temp_timestamp)[-4:]
        return int(temp_timestamp * 1000), ret_str
