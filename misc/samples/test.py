# coding=utf-8
# author: zengyuetian
import random

# print_str = "{print $2}"
# SDK_FILE = "ys_service_static"
# kill_cmd = "ps aux | grep {0} |grep -v grep |awk -F ' ' '{1}' | xargs kill -9".format(SDK_FILE, print_str)
# print kill_cmd


def dynamic_adjust(total, now):
    print "total, now is: ", total, now
    # calc operation
    if now < (total/10):
        increase = True
    elif now > (total/10*9):
        increase = False
    else:
        increase = random.choice([True, False])

    # calc num
    rest = total - now
    if increase:
        num = random.choice(range(1, rest))
        now = now + num
    else:
        num = random.choice(range(1, now))
        now = now - num

    print increase, num, now
    return increase, num, now


total = 100
now = 20
for i in range(0, 100):
    increase, num, now = dynamic_adjust(total, now)

# my_dict = {"name":"hello",
#            "age": 10}
#
# for k, v in my_dict.items():
#     print k, v
