# coding=utf-8
# author: zengyuetian

from lib.sdk.pcap_http_parser import *
import re
from lib.sdk.sdk_constant import *


def has_login_request(http_requests, req_pat):
    for http in http_requests:
        if re.match(req_pat, http.uri) is not None:
            print http.uri
            print http.headers
            print http.body
            return True
    return False


def get_request(http_requests, req_pat, sect="body"):
    """
    get
    :param http_requests:
    :param req_pat:
    :param sect:
    :return:
    """
    for http in http_requests:
        if re.match(req_pat, http.uri) is not None:
            if sect == "body":
                print http.body
                return http.body
            if sect == "headers":
                print http.headers
                return http.headers
    return None


def verify_login_request(http_requests, req_pat):
    """
    verify that login request in requests list
    :param http_requests:
    :param req_pat:
    :return:
    """
    content = get_request(http_requests, req_pat)
    print type(content)
    content_dict = eval(content)
    # print type(content_dict)
    fields = [
        "version",
        "natType",
        "publicIP",
        "publicPort",
        "privateIP",
        "privatePort",
        "stunIP",
        "macs",
        "deviceInfo"]
    for field in fields:
        if field not in content_dict:
            raise AssertionError("field {0} is not in request".format(field))
        elif content_dict[field] is None:
            raise AssertionError("field {0} is empty".format(field))
    return content_dict


def verify_log_file_result(log_file_path, api_name=None):
    if api_name is None:
        ret_val = False
        with open(log_file_path, "r") as fd:
            for line in fd:
                if line.find("test result:") > -1:
                    if line.split(":")[1].replace("\n", "").strip() == "True":
                        ret_val = True
                        break
                else:
                    print line
        return ret_val
    else:
        right_log = '{} Topic check is OK'.format(api_name)
        ret_val = False
        with open(log_file_path, 'r') as fd:
            fd_lines = fd.readlines()
        for result_line in fd_lines:
            if result_line.find(right_log) >= 0:
                ret_val = True
                break
            else:
                continue
        return ret_val


if __name__ == "__main__":
    # parser = PcapHttpParser("e:/tmp/sdk.pcap")
    # requests = parser.get_http_requests(80)
    #
    # print has_login_request(requests, LOGIN_REQUEST_PATTERN)
    # text = "/session/peers/0123456789ABCDEF0123456789ABCDEF"
    # print re.match(login_request_pattern, text)

    print verify_log_file_result('result_log.txt', 'Peer Get Live seeds')
