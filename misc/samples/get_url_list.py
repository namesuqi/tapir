# coding=utf-8
# author: zengyuetian

ip_list = ["a", "b", "c"]
sdk_num = [10, 20, 30]


def get_url_list():
    all_list = list()
    count = 0
    for index, ip in enumerate(ip_list):
        print index, ip
        num = sdk_num[index]
        for i in range(num):
            all_list.append("{0}/{1}".format(ip, count))
            count += 1

    return all_list


def get_start_end(ip):
    index = ip_list.index(ip)
    start = sum(sdk_num[:index])
    end = sum(sdk_num[:index + 1])
    return start, end


if __name__ == "__main__":
    # lsts = get_url_list()
    # print lsts
    start, end = get_start_end("c")
    print start, end
