import api_format
import tcpdump_filter
import time
import re
import sys


def sdk_check_report(result_list, log_fd):
    ret_val = True
    for r_key in result_list:
        if not result_list[r_key][0]:
            ret_val = result_list[r_key][0]
            log_fd.write("%s Topic request string not found\n" % r_key)
        if not result_list[r_key][1]:
            ret_val = result_list[r_key][1]
            log_fd.write("%s Topic response string not found\n" % r_key)
        if result_list[r_key][0] and result_list[r_key][1]:
            log_fd.write("%s Topic check is OK\n" % r_key)
    return ret_val


def sdk_check_request(pattern_dict, time_out):
    p_fd = tcpdump_filter.tcpdump_filter()
    res_list = {}
    for p_key in pattern_dict.keys():
        res_list[api_format.PATTERN_NAME[p_key]] = [False, False]
    time_start = time.time()
    while True:
        ret_txt = tcpdump_filter.read_tcpdump_filter(p_fd)
        if time.time() - time_start >= time_out:
            break
        if ret_txt == '':
            continue
        txt_array = ret_txt.split("\n")
        for ret_text in txt_array:
            for pattern_key in pattern_dict.keys():
                m = re.match(pattern_key, ret_text)
                if m:
                    res_list[api_format.PATTERN_NAME[pattern_key]][0] = True
                    break
                m = re.match(pattern_dict[pattern_key], ret_text)
                if m:
                    if res_list[api_format.PATTERN_NAME[pattern_key]][0]:
                        res_list[api_format.PATTERN_NAME[pattern_key]][1] = True  # pattern '' match always OK
                        del pattern_dict[pattern_key]
                        break
        if len(pattern_dict) == 0:
            print "check finish ..."
            break
    p_fd.kill()
    return res_list


if __name__ == "__main__":
    log_file = open(api_format.LOG_FILE, "w")
    timeout = 660
    if len(sys.argv) > 1:
        timeout = int(sys.argv[1])
    r_list = sdk_check_request(api_format.PATTERN_DICT, timeout)
    r_val = sdk_check_report(r_list, log_file)
    log_file.write("test result: %s\n" % str(r_val))
    log_file.flush()
    log_file.close()
