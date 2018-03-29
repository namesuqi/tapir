# coding=utf-8
# author: Sun XiaoLei
# review: Done
# 打印模拟器日志文件:
# 全部经过模拟器转发的协议都被记录在forward_xxx.log
# 全部关心的PENE与DCCP记录在penetrate.log


import os
import time
import global_var as glbv


class NATLogger(object):
    def __init__(self):
        self._init_log()

    def _init_log(self):
        log_path = "./log"
        all_log_name = "forward_%s" % str(int(time.time()))
        penetrate_log_name = "penetrate.log"
        if not os.path.isdir(log_path):
            os.mkdir(log_path)
        self.log_file_handle = open(os.path.join(log_path, all_log_name), "wt")
        self.log_file_penetrate = open(os.path.join(log_path, penetrate_log_name), "wt")

    def log(self, data):
        print data
        self.log_file_handle.write(data + "\n")
        self.log_file_handle.flush()

        if data.find("packet: %s" % glbv.PENE_DISTINGUISH) > -1 or data.find("packet: %s" % glbv.DCCP_DISTINGUISH) > -1:
            self.log_file_penetrate.write(data + "\n")
            self.log_file_penetrate.flush()

    def __del__(self):
        self.log_file_handle.close()
        self.log_file_penetrate.close()
