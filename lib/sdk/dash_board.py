# coding=utf-8
"""
通过SDK的dashboard获得SDK相关信息

__author__ = 'zengyuetian'

"""

from lib.request.http_request import *
import time

max_try = 5

login_url = "/ajax/login"
version_url = "/ajax/version"
index_url = "/dashboard/index"
httpd_url = "/ajax/httpd"
vod_core_url = "/ajax/vod_core"
chunk_buffer_url = "/dashboard/chunk_buffer"
chunk_pool_url = "/ajax/chunk_pool"
distribute_url = "/ajax/distribute"
meminfo_url = "/dashboard/meminfo"
profiling_url = "/ajax/profiling"
timer_url = "/dashboard/timer"
sched_url = "/dashboard/sched"
seeds_url = "/ajax/seeder"
offer_url = "/ajax/offer"
peers_url = "/dashboard/peers"
dccp_url = "/dashboard/dccp"
lsm_url = "/ajax/lsm"
help_url = "/ajax/help"
report_url = "/ajax/report"
conf_url = "/ajax/conf"

    
def get_login(host, port):
    response = None
    for i in range(max_try):
        try:
            response = http_request('GET', host, port, login_url)
            break
        except:
            time.sleep(0.1)
    return response


def get_version(host, port):
    response = None
    print host, port
    for i in range(max_try):
        try:
            response = http_request('GET', host, port, version_url)
            break
        except:
            time.sleep(0.1)
    return response


def get_httpd(host, port):
    response = None
    for i in range(max_try):
        try:
            response = http_request('GET', host, port, httpd_url)
            break
        except:
            time.sleep(0.1)
    return response


def get_vod_core(host, port):
    response = None
    for i in range(max_try):
        try:
            response = http_request('GET', host, port, vod_core_url)
            break
        except:
            time.sleep(0.1)
    return response


def get_chunk_buffer(host, port):
    response = None
    for i in range(max_try):
        try:
            response = http_request('GET', host, port, chunk_buffer_url)
            break
        except:
            time.sleep(0.1)
    return response


def get_chunk_pool(host, port):
    response = None
    for i in range(max_try):
        try:
            response = http_request('GET', host, port, chunk_pool_url)
            break
        except:
            time.sleep(0.1)
    return response


def get_distribute(host, port):
    response = None
    for i in range(max_try):
        try:
            response = http_request('GET', host, port, distribute_url)
            break
        except:
            time.sleep(0.1)
    return response


def get_meminfo(host, port):
    response = None
    for i in range(max_try):
        try:
            response = http_request('GET', host, port, meminfo_url)
            break
        except:
            time.sleep(0.1)
    return response


def get_profiling(host, port):
    response = None
    for i in range(max_try):
        try:
            response = http_request('GET', host, port, profiling_url)
            break
        except:
            time.sleep(0.1)
    return response


def get_timer(host, port):
    response = None
    for i in range(max_try):
        try:
            response = http_request('GET', host, port, timer_url)
            break
        except:
            time.sleep(0.1)
    return response


def get_sched(host, port):
    response = None
    for i in range(max_try):
        try:
            response = http_request('GET', host, port, sched_url)
            break
        except:
            time.sleep(0.1)
    return response


def get_seeds(host, port):
    response = None
    for i in range(max_try):
        try:
            response = http_request('GET', host, port, seeds_url)
            break
        except:
            time.sleep(0.1)
    return response


def get_offer(host, port):
    response = None
    for i in range(max_try):
        try:
            response = http_request('GET', host, port, offer_url)
            break
        except:
            time.sleep(0.1)
    return response


def get_peers(host, port):
    response = None
    for i in range(max_try):
        try:
            response = http_request('GET', host, port, peers_url)
            break
        except:
            time.sleep(0.1)
    return response


def get_dccp(host, port):
    response = None
    for i in range(max_try):
        try:
            response = http_request('GET', host, port, dccp_url)
            break
        except:
            time.sleep(0.1)
    return response


def get_lsm(host, port):
    response = None
    for i in range(max_try):
        try:
            response = http_request('GET', host, port, lsm_url)
            break
        except:
            time.sleep(0.1)
    return response


def get_help(host, port):
    response = None
    for i in range(max_try):
        try:
            response = http_request('GET', host, port, help_url)
            break
        except:
            time.sleep(0.1)
    return response


def get_report(host, port):
    response = None
    for i in range(max_try):
        try:
            response = http_request('GET', host, port, report_url)
            break
        except:
            time.sleep(0.1)
    return response


def get_conf(host, port):
    response = None
    for i in range(max_try):
        try:
            response = http_request('GET', host, port, conf_url)
            break
        except:
            time.sleep(0.1)
    return response







###############################
# 调试用
###############################
if __name__ == "__main__":
    pass





