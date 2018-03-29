# coding=utf-8
# author: zengyuetian


import platform
import os

# get the os name

host_type = platform.system()
if host_type != "Windows" and host_type != "Linux":
    host_type = "Mac"

