# coding=utf-8
# author: zengyuetian

# 导入Fabric API:
from fabric.api import *


# 用户为root:
env.user = 'root'
# 服务器登录密码:
env.password = 'Yunshang2014'
# 服务器地址，可以有多个，依次部署:
env.hosts = ['123.56.30.115']

REMOTE_BASE_DIR = '/root/zyt/live_play'


def deploy():
    # 运行本地命令
    local("echo start")
    # 删除已有的tar文件:
    run('rm -rf %s' % REMOTE_BASE_DIR)
    run('mkdir {dir}'.format(dir=REMOTE_BASE_DIR))
    # 上传新的tar文件:
    put('./*', REMOTE_BASE_DIR)


