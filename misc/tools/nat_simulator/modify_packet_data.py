# coding=utf-8
# author: Sun XiaoLei
# 此文件用于修改模拟器转发内容，未用，可忽略

import random
import struct

import binascii
import global_var as glbv


class ModifyPacketData(object):
    def __init__(self, subject, effect_obj):
        self.position = -1
        self.operator = None
        self.data = None
        self.subject = subject
        self.obj = effect_obj

    def set_operate_type(self, byte_position, operator, operate_data):
        self.position = byte_position
        self.operator = operator
        self.data = operate_data

    def filter_event_condition(self, data_str):
        ret_val = False
        if glbv.MODIFY_DATA_COUNT == 0:
            glbv.MODIFY_DATA_COUNT = random.randint(1, 100)
        if glbv.MODIFY_DATA_NOT_RANDOM:
            self.set_operate_type(glbv.MODIFY_DATA_POSITION, glbv.MODIFY_DATA_OPERATOR, glbv.MODIFY_DATA_OPERATE_DATA)
            if len(glbv.MODIFY_DATA_CONTAIN) > 0:
                for tmp_contain in glbv.MODIFY_DATA_CONTAIN:
                    if data_str.find(tmp_contain) > -1:
                        glbv.G_COUNT_INDEX += 1
                        break
            else:
                glbv.G_COUNT_INDEX += 1
            if glbv.G_COUNT_INDEX == glbv.MODIFY_DATA_COUNT:
                ret_val = True
                glbv.G_COUNT_INDEX = 0
        else:
            if len(glbv.MODIFY_DATA_CONTAIN) > 0:
                for tmp_contain in glbv.MODIFY_DATA_CONTAIN:
                    if data_str.find(tmp_contain) > -1:
                        glbv.G_COUNT_INDEX += 1
                        break
            else:
                glbv.G_COUNT_INDEX += 1
            if glbv.G_COUNT_INDEX == glbv.MODIFY_DATA_COUNT:
                if glbv.MODIFY_DATA_POSITION == 0:
                    tmp_position = random.randint(1, len(data_str) / 2)
                else:
                    tmp_position = glbv.MODIFY_DATA_POSITION
                tmp_operator = random.choice(("&", "|", "^"))
                tmp_operate_data = random.randint(1, 255)
                self.set_operate_type(tmp_position, tmp_operator, tmp_operate_data)
                ret_val = True
                glbv.G_COUNT_INDEX = 0
        return ret_val

    def event_handle(self, event):
        ret_data = event.param.data.data
        if self.filter_event_condition(binascii.b2a_hex(ret_data)):
            tmp_index = -1
            data_array = bytes(ret_data)
            if self.position > 0:
                if self.position <= len(data_array):
                    tmp_index = self.position - 1
                    tmp_data = data_array[tmp_index]
            else:
                if abs(self.position) <= len(data_array):
                    tmp_index = len(data_array) + self.position
                    tmp_data = data_array[tmp_index]
            if self.operator == "&" and tmp_index > -1 and self.subject == event.subject:
                tmp_data = struct.pack("!B", int(binascii.b2a_hex(tmp_data), 16) & self.data)
                ret_data = ret_data[:tmp_index] + tmp_data + ret_data[tmp_index + 1:]
            elif self.operator == "|" and tmp_index > -1 and self.subject == event.subject:
                tmp_data = struct.pack("!B", int(binascii.b2a_hex(tmp_data), 16) | self.data)
                ret_data = ret_data[:tmp_index] + tmp_data + ret_data[tmp_index + 1:]
            elif self.operator == "^" and tmp_index > -1 and self.subject == event.subject:
                tmp_data = struct.pack("!B", int(binascii.b2a_hex(tmp_data), 16) ^ self.data)
                ret_data = ret_data[:tmp_index] + tmp_data + ret_data[tmp_index + 1:]
        self.obj.t_data = ret_data
