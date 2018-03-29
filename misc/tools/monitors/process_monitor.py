# coding=utf-8
# author: zengyuetian
# watch -n 1 "ps aux|grep ys_service_static"
import os

if __name__ == "__main__":
    process_name = "./ys_service_static"
    os.system("ps aux|grep {0}".format(process_name))
