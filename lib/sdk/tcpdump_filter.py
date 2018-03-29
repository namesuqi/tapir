#! /usr/bin/python

import subprocess
import fcntl
import os
import select


def tcpdump_filter():
    cmd1 = ['tcpdump', '-i', 'eth0', '-A', '-n', '-B', '4096', '-s', '0', '-w', '-']
    # cmd2 = ['grep', '--line-buffered', '-a', '-o', '-E', 'POST /.*|GET /.*|DELETE /.*|^{.*}']
    cmd2 = ['grep', '--line-buffered', '-a', '-o', '-E', 'POST .*|GET .*|DELETE .*|{.*}']
    p1 = subprocess.Popen(cmd1, stdout=subprocess.PIPE)
    p2 = subprocess.Popen(cmd2, stdout=subprocess.PIPE, stdin=p1.stdout)

    flags = fcntl.fcntl(p2.stdout.fileno(), fcntl.F_GETFL)
    fcntl.fcntl(p2.stdout.fileno(), fcntl.F_SETFL, (flags | os.O_NDELAY | os.O_NONBLOCK))
    return p2


def read_tcpdump_filter(p_fd):
    txt = ''
    read_ready, _, _ = select.select([p_fd.stdout.fileno()], [], [], 1)
    if len(read_ready):
        try:
            for line in iter(p_fd.stdout.readline, ""):
                txt += line
        except IOError:
            # print 'no data ...'
            pass
    print txt
    return txt

