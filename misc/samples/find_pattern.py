# coding=utf-8
# author: zengyuetian


import time
import re
t1 = time.time()
total = 0
num = 0
pattern = re.compile("cur_wnd.*(20|21|31)")
with open("c:/yunshang_10m_line.log", "r") as f:
    line = f.readline()
    while line:
        total += 1
        if pattern.search(line):
            num += 1
        line = f.readline()
print "find {0} match".format(num)
print "total {0} lines".format(total)
t2 = time.time()
print "cost {0} sec".format(t2-t1)




